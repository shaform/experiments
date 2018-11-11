import os

import zarr
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from tqdm import tqdm, trange


class FaceDataset(Dataset):
    def __init__(self, path, transforms=None):
        self.path = path
        self.keys = ('images', 'labels')
        assert os.path.exists(path), 'file `{}` not exists!'.format(path)

        root = zarr.open(path, mode='r')
        self.num_examples = root['labels'].shape[0]
        self.datasets = None

        if transforms is None:
            transforms = {
                'labels': lambda v: torch.tensor(v, dtype=torch.long),
                'images': lambda v: torch.tensor((v - 127.5)/127.5, dtype=torch.float32)
            }
        self.transforms = transforms

    def __len__(self):
        return self.num_examples

    def __getitem__(self, idx):
        if self.datasets is None:
            root = zarr.open(self.path, mode='r')
            self.datasets = {key: root[key] for key in self.keys}

        items = []
        for key in self.keys:
            item = self.datasets[key][idx]
            if key in self.transforms:
                item = self.transforms[key](item)
            items.append(item)
        return items


class Model(nn.Module):
    def __init__(self, input_size=96 * 96 * 3, output_size=126,
                 hidden_size=25):
        super().__init__()

        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, output_size)
        self.criteria = nn.CrossEntropyLoss()

    def forward(self, inputs):
        inputs = inputs.view(inputs.size()[0], -1)
        outputs = self.layer1(inputs)
        outputs = self.layer2(outputs)
        return outputs


def main(batch_size=30, epochs=1):
    data_train = FaceDataset('data/anime_faces/train')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    loader = DataLoader(
        data_train, batch_size=batch_size, shuffle=True, num_workers=5)
    model = Model()
    model.to(device)
    model.train()
    optim = torch.optim.Adam(model.parameters(), lr=0.001)
    for epoch in trange(epochs):
        t = tqdm(loader)
        for i, (images, labels) in enumerate(t):
            images = images.to(device)
            labels = labels.to(device)

            optim.zero_grad()
            logits = model(images)
            loss = model.criteria(logits, labels)
            loss.backward()
            optim.step()

            predicts = torch.argmax(F.softmax(logits, dim=1), dim=1)
            accuracy = (predicts == labels).to(torch.float32).mean()
            t.set_postfix(
                epoch=epoch, i=i, loss=loss.item(), accuracy=accuracy.item())

    data_val = FaceDataset('data/anime_faces/val')
    val_loader = DataLoader(data_val, batch_size=batch_size, num_workers=0)
    total = len(data_val)
    total_correct = 0
    model.eval()
    for images, labels in val_loader:
        images = images.to(device)
        labels = labels.to(device)
        logits = model(images)
        predicts = torch.argmax(F.softmax(logits, dim=1), dim=1)
        correct = (predicts == labels).sum()
        total_correct += correct.item()
    print('Val accuracy = {}'.format(total_correct / total))


if __name__ == '__main__':
    main()

# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--input-file', default='data/test.lmdb')
#     parser.add_argument('--batch-size', type=int, default=10)
#     parser.add_argument('--cuda', action='store_true')
#     return parser.parse_args()

# def main():
#     args = parse_args()
#     train(**vars(args))

# if __name__ == '__main__':
#     main()
