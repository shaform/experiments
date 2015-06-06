#!/usr/bin/env python
import argparse
import random

import lmdb
import numpy as np
from caffe.io import array_to_datum

num_of_dims = 100


def load_data(path):
    items = []
    with open(path) as f:
        for l in f:
            tokens = l.rstrip().split()
            label = int(tokens[0])
            # change label `-1' to `0'
            if label == -1:
                label = 0
            # ignore the index since we already know the format
            arr = [float(dim.split(':')[1]) for dim in tokens[1:]]
            items.append((label, arr))

    random.shuffle(items)

    Y = np.array([y for y, _ in items])
    X = np.array([x for _, x in items])
    X = X.reshape((len(Y), 1, 1, num_of_dims))

    return X, Y


def save_data(path, X, Y):
    num = np.prod(X.shape)
    itemsize = np.dtype(X.dtype).itemsize
    # set a reasonable upper limit for database size
    map_size = 10240 * 1024 + num * itemsize * 2
    print 'save {} instances...'.format(num)

    env = lmdb.open(path, map_size=map_size)

    for i, (x, y) in enumerate(zip(X, Y)):
        datum = array_to_datum(x, y)
        str_id = '{:08}'.format(i)

        with env.begin(write=True) as txn:
            txn.put(str_id, datum.SerializeToString())


def process_commands():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')

    return parser.parse_args()


def main():
    args = process_commands()
    X, Y = load_data(args.input)
    save_data(args.output, X, Y)

if __name__ == '__main__':
    main()
