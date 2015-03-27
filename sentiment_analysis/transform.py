import argparse


def process_commands():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)

    return parser.parse_args()


if __name__ == '__main__':
    args = process_commands()

    with open(args.input, 'r') as ifile, open(args.output, 'w') as ofile:
        for l in ifile:
            label, *features = l.strip().split()
            vector = ['{}:{}'.format(i + 1, v) for i, v in enumerate(features)]
            ofile.write('{} {}\n'.format(label, ' '.join(vector)))
