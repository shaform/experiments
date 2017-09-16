import argparse
import hashlib
import logging
import os
import shutil
import random

logger = logging.Logger(__name__)


def prepare(input_dir, output_dir, web_root, num_outputs, names, seed):
    random.seed(seed)
    image_dir = os.path.join(output_dir, 'images')
    os.makedirs(image_dir, exist_ok=True)

    # load choices for each question
    choices = []
    for name in names:
        named_images = []
        # write hashes of this name to a file
        # so we can analyse results later
        id_path = os.path.join(output_dir, name + '.txt')
        with open(id_path, 'w') as id_file:
            for i in range(1, num_outputs + 1):
                fname = os.path.join(input_dir, '{}.{}.jpg'.format(name, i))
                h = md5(fname)
                named_images.append(h)
                id_file.write(h + '\n')
                # put images to a separate directory
                outpath = os.path.join(image_dir, '{}.jpg'.format(h))
                shutil.copyfile(fname, outpath)

        choices.append(named_images)

    # output url for each image
    url_path = os.path.join(output_dir, 'urls.tsv')
    with open(url_path, 'w') as outfile:
        outfile.write('h\turl\n')
        for named_images in choices:
            for h in named_images:
                outfile.write('{}\t{}/images/{}.jpg\n'.format(h, web_root, h))

    # output survey file
    survey_path = os.path.join(output_dir, 'survey.tsv')
    with open(survey_path, 'w') as outfile:
        header = '\t'.join([str(n) for n in range(1, len(names) + 1)])
        outfile.write('num\t' + header + '\n')
        for n in range(num_outputs):
            options = [named_images[n] for named_images in choices]
            random.shuffle(options)
            outfile.write('{}\t{}\n'.format(n + 1, '\t'.join(options)))


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, 'rb') as infile:
        for chunk in iter(lambda: infile.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')
    parser.add_argument('--web-root', default='')
    parser.add_argument('--num-outputs', type=int, default=10)
    parser.add_argument('--names', nargs='+', default=('cat', 'dog'))
    parser.add_argument('--seed', type=int, default=1126)
    return parser.parse_args()


def main():
    args = parse_args()
    prepare(**vars(args))


if __name__ == '__main__':
    main()
