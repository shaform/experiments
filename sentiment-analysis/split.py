import argparse
import random


def process_commands():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--train_pos', required=True)
    parser.add_argument('--train_neg', required=True)
    parser.add_argument('--test_pos', required=True)
    parser.add_argument('--test_neg', required=True)

    return parser.parse_args()


def output(path, sents):
    with open(path, 'w') as f:
        f.writelines(sents)

if __name__ == '__main__':
    args = process_commands()

    pos = []
    neg = []

    with open(args.input, 'r') as f:
        for l in f:
            label, sent = l.split(' ', 1)
            if label == '1':
                pos.append(sent)
            else:
                neg.append(sent)

    random.shuffle(pos)
    tlen = len(pos) // 10
    output(args.test_pos, pos[:tlen])
    output(args.train_pos, pos[tlen:])

    random.shuffle(neg)
    tlen = len(neg) // 10
    output(args.test_neg, neg[:tlen])
    output(args.train_neg, neg[tlen:])
