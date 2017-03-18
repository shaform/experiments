#!/bin/bash

for clf in svc xgb softmax;
do
  for sample_size in 500 1000 1500;
  do
    for seed in 1 2 3 4 5 6 7 8 9 10;
    do
      python mnist.py with classifier=$clf sample_size=$sample_size seed=$seed -m sacred || exit 1
    done
  done
done
