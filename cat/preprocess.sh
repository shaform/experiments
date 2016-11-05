#!/bin/bash
mkdir -p data/train
mkdir -p data/test
python3 crop.py --indir cats/catmapper --outdir data/train
python3 crop.py --indir cats/cat_photos --outdir data/test
