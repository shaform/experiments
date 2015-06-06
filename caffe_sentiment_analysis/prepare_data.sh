# get mesnilgr/iclr15
git clone https://github.com/mesnilgr/iclr15

mkdir -p iclr15_run
cd iclr15_run

# get data
../iclr15/scripts/data.sh

# extract the part to create paragraph vectors from iclr15 scripts
sed -e '/liblinear/,$d' ../iclr15/scripts/paragraph.sh > paragraph.sh

# start creating the vectors
chmod +x paragraph.sh
./paragraph.sh

# copy the vectors
cd word2vec
cp full-train.txt test.txt ../../
