import argparse

from collections import defaultdict


def process_commands():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)

    return parser.parse_args()


def load_file(path):
    with open(path, 'r') as f:
        for l in f:
            yield l.strip().split()

if __name__ == '__main__':
    args = process_commands()

    d = defaultdict(int)
    vocab = {}
    for tokens in load_file(args.input):
        for t in tokens:
            if t not in vocab:
                vocab[t] = len(vocab) + 1
            d[vocab[t]] += 1

        for t in zip(tokens, tokens[1:]):
            if t not in vocab:
                vocab[t] = len(vocab) + 1
            d[vocab[t]] += 1

    with open(args.output, 'w') as f:
        for tokens in load_file(args.input):
            features = defaultdict(int)
            for t in tokens:
                features[vocab[t]] += 1
            for t in zip(tokens, tokens[1:]):
                features[vocab[t]] += 1

            vector = ['{}:{}'.format(k, v / d[k])
                      for k, v in sorted(features.items())]
            f.write('x {}\n'.format(' '.join(vector)))
