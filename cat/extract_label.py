import argparse
import json
import os
import random
import xml.etree.ElementTree as ET


def main(indir, outdir, name, seed):
    random.seed(seed)
    if name is None:
        name = os.path.basename(indir)

    entries = []

    for path in sorted(os.listdir(indir)):
        if path.endswith('.xml'):
            tree = ET.parse(os.path.join(indir, path))
            root = tree.getroot()

            img_path = root.findtext('path')
            rects = []

            for obj in root.iter('object'):
                x1 = float(obj.find('bndbox').findtext('xmin'))
                y1 = float(obj.find('bndbox').findtext('ymin'))
                x2 = float(obj.find('bndbox').findtext('xmax'))
                y2 = float(obj.find('bndbox').findtext('ymax'))

                rects.append({'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2})

            entry = {'image_path': img_path, 'rects': rects}
            entries.append(entry)

    random.shuffle(entries)

    train_offset = int(len(entries) * 0.8)

    train = entries[:train_offset]
    val = entries[train_offset:]

    datasets = [('train', train), ('val', val)]

    for prefix_name, dataset in datasets:
        with open(
                os.path.join(outdir, '{}_{}_boxes.json'.format(
                    name, prefix_name)), 'w') as f:
            json.dump(dataset, f, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--indir', required=True)
    parser.add_argument('--outdir', required=True)

    parser.add_argument('--name')
    parser.add_argument('--seed', type=int, default=633)

    args = parser.parse_args()

    main(indir=args.indir, outdir=args.outdir, name=args.name, seed=args.seed)
