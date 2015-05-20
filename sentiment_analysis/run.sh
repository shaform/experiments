# -- preprocess -- #
# You'll need 207884_hotel_training.txt & CKIP segmenter to run preprocess.py
#python3 preprocess.py --server $SERVER --port $PORT --user $USER --password $PASS --output data.txt --input 207884_hotel_training.txt
python3 split.py --input data/data.txt --train_pos data/train_pos.txt --train_neg data/train_neg.txt --test_pos data/test_pos.txt --test_neg data/test_neg.txt

# -- rnnlm -- #
mkdir rnnlm
cd rnnlm
wget https://f25ea9ccb7d3346ce6891573d543960492b92c30.googledrive.com/host/0ByxdPXuxLPS5RFM5dVNvWVhTd0U/rnnlm-0.4b.tgz
tar -xvf rnnlm-0.4b.tgz
g++ -lm -O3 -march=native -Wall -funroll-loops -ffast-math -c rnnlm-0.4b/rnnlmlib.cpp
g++ -lm -O3 -march=native -Wall -funroll-loops -ffast-math rnnlm-0.4b/rnnlm.cpp rnnlmlib.o -o rnnlm


# construct positive language model
head -n 200 ../data/train_pos.txt > val.txt
cat ../data/train_pos.txt | sed '1,200d' > train.txt
./rnnlm -rnnlm pos.model -train train.txt -valid val.txt -hidden 50 -direct-order 3 -direct 200 -class 100 -debug 2 -bptt 4 -bptt-block 10 -binary

# construct negative language model
head -n 200 ../data/train_neg.txt > val.txt
cat ../data/train_neg.txt | sed '1,200d' > train.txt
./rnnlm -rnnlm neg.model -train train.txt -valid val.txt -hidden 50 -direct-order 3 -direct 200 -class 100 -debug 2 -bptt 4 -bptt-block 10 -binary

cat ../data/test_pos.txt ../data/test_neg.txt | nl -v0 -s' ' -w1 > test.txt
./rnnlm -rnnlm pos.model -test test.txt -debug 0 -nbest > model_pos_score.txt
./rnnlm -rnnlm neg.model -test test.txt -debug 0 -nbest > model_neg_score.txt

mkdir ../scores
paste model_pos_score.txt model_neg_score.txt | awk '{print $1/$2;}' > ../scores/RNNLM
cd ..
python3 normalize.py --input scores/RNNLM --output scores/RNNLM --type rnnlm

python3 evaluate.py --test_pos data/test_pos.txt --scores scores/RNNLM

# -- word2vec - sentence vectors -- #
git clone https://github.com/shaform/word2vec.git
cd word2vec
git checkout doc2vec
make

cat ../data/train_pos.txt ../data/train_neg.txt ../data/test_pos.txt ../data/test_neg.txt | nl -v0 -s' ' -w1 | sed 's/^/@@SS-/' | shuf > all.txt
time ./word2vec -train all.txt -output vectors.txt -cbow 0 -size 400 -window 10 -negative 5 -hs 1 -sample 1e-3 -threads 24 -binary 0 -iter 20 -min-count 1 -sentence-vectors 1
grep '@@SS-' vectors.txt | sed -e 's/^@@SS-//' | sort -n > sentence_vectors.txt

mkdir ../liblinear
cd ../liblinear
wget -O liblinear.zip http://www.csie.ntu.edu.tw/~cjlin/cgi-bin/liblinear.cgi?+http://www.csie.ntu.edu.tw/~cjlin/liblinear+zip
unzip liblinear.zip
cd *
make
cp train predict ..
cd ../../word2vec

python3 ../transform.py --input sentence_vectors.txt --output sentence_features.txt
python3 ../train.py --features sentence_features.txt --train_pos ../data/train_pos.txt --train_neg ../data/train_neg.txt --test_pos ../data/test_pos.txt --output_train train.txt --output_test test.txt

../liblinear/train -s 0 train.txt model.logreg
../liblinear/predict -b 1 test.txt model.logreg out.logreg

sed '1d' out.logreg | cut -d' ' -f3 > ../scores/DOC2VEC
cd ..
python3 normalize.py --input scores/DOC2VEC --output scores/DOC2VEC --type logreg

python3 evaluate.py --test_pos data/test_pos.txt --scores scores/DOC2VEC

# -- TF-IDF -- #
mkdir tfidf
cd tfidf
cat ../data/train_pos.txt ../data/train_neg.txt ../data/test_pos.txt ../data/test_neg.txt > all.txt
python3 ../tfidf.py --input all.txt --output features.txt
python3 ../train.py --features features.txt --train_pos ../data/train_pos.txt --train_neg ../data/train_neg.txt --test_pos ../data/test_pos.txt --output_train train.txt --output_test test.txt

../liblinear/train -s 0 train.txt model.logreg
../liblinear/predict -b 1 test.txt model.logreg out.logreg

sed '1d' out.logreg | cut -d' ' -f3 > ../scores/TFIDF
cd ..
python3 normalize.py --input scores/TFIDF --output scores/TFIDF --type logreg

python3 evaluate.py --test_pos data/test_pos.txt --scores scores/TFIDF

# -- TOTAL -- #

paste scores/RNNLM scores/DOC2VEC scores/TFIDF | awk '{print ($1+$2+$3)/3;}' > scores/TOTAL
python3 evaluate.py --test_pos data/test_pos.txt --scores scores/TOTAL
