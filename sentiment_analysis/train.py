import argparse


def process_commands():
    parser = argparse.ArgumentParser()
    parser.add_argument('--features', required=True)
    parser.add_argument('--train_pos', required=True)
    parser.add_argument('--train_neg', required=True)
    parser.add_argument('--test_pos', required=True)
    parser.add_argument('--output_train', required=True)
    parser.add_argument('--output_test', required=True)

    return parser.parse_args()


if __name__ == '__main__':
    args = process_commands()

    with open(args.train_pos, 'r') as pos:
        plen = len([1 for l in pos])

    with open(args.train_neg, 'r') as neg:
        nlen = len([1 for l in neg]) + plen

    with open(args.test_pos, 'r') as pos:
        tplen = len([1 for l in pos]) + nlen

    with open(args.features, 'r') as f, open(args.output_train, 'w') as train, open(args.output_test, 'w') as test:
        for i, l in enumerate(f):
            _, features = l.split(' ', 1)
            if i < plen:
                train.write('0 ' + features)
            elif i < nlen:
                train.write('1 ' + features)
            elif i < tplen:
                test.write('0 ' + features)
            else:
                test.write('1 ' + features)
