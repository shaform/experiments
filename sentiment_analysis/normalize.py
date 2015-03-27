import argparse
import math


def process_commands():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--type', required=True,
                        choices=('rnnlm', 'logreg'))

    return parser.parse_args()


def load_data(path):
    with open(path, 'r') as f:
        return [float(l) for l in f]


def save_data(path, data):
    with open(path, 'w') as f:
        for n in data:
            f.write('{}\n'.format(n))


def norm(data):
    mean = math.sqrt(sum(n * n for n in data))
    return [n / mean for n in data]

if __name__ == '__main__':
    args = process_commands()

    data = load_data(args.input)

    if args.type == 'rnnlm':
        data = [n - 1 for n in data]
    elif args.type == 'logreg':
        data = [n - 0.5 for n in data]
    else:
        raise

    data = norm(data)

    save_data(args.output, data)
