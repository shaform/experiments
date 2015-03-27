import argparse
import os


def process_commands():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scores', required=True)
    parser.add_argument('--test_pos', required=True)

    return parser.parse_args()


if __name__ == '__main__':
    args = process_commands()

    with open(args.test_pos, 'r') as pos:
        plen = len([1 for l in pos])

    with open(args.scores, 'r') as s:
        correct = total = 0
        for i, v in enumerate(s):
            if i < plen:
                if float(v) < 0:
                    correct += 1
            else:
                if float(v) > 0:
                    correct += 1
            total += 1
    print('{} accuracy: {:.4f}%'.format(
        os.path.basename(args.scores), correct / total * 100))
