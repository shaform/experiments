# get moedict data
if [ ! -d moedict-data ]; then
    git clone --depth 1 https://github.com/g0v/moedict-data.git
fi
# get json2unicode.pl
if [ ! -d moedict-epub ]; then
    git clone --depth 1 https://github.com/g0v/moedict-epub.git
fi
# get jieba segmentation
if [ ! -d jieba ]; then
    git clone --depth 1 https://github.com/fxsjy/jieba.git
fi
# get word2vec
if [ ! -d word2vec ]; then
    git clone --depth 1 https://github.com/svn2github/word2vec.git
    cd word2vec
    make
    cd ..
fi
# convert to unicode
if [ ! -e dict-revised.unicode.json ]; then
    cp -v moedict-data/dict-revised.json moedict-epub/
    cd moedict-epub
    perl json2unicode.pl > dict-revised.unicode.json
    cp -v dict-revised.unicode.json ../
    cd ..
fi
# extract corpus
if [ ! -e sentences.txt ]; then
    python3 extract_json.py < dict-revised.unicode.json > sentences.txt
fi
# segment it
if [ ! -e sentences.segged.txt ]; then
    cp -v cut.py jieba/cut.py
    python jieba/cut.py < sentences.txt > sentences.segged.txt
fi
# train word vectors
if [ ! -e vectors.bin ]; then
    time word2vec/word2vec -train sentences.segged.txt -output vectors.bin -cbow 0 -size 200 -window 10 -negative 5 -hs 0 -sample 1e-4 -threads 24 -binary 1 -iter 20 -min-count 1
fi
