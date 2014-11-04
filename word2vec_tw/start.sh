if [ ! -d moedict-data ]; then
    git clone --depth 1 https://github.com/g0v/moedict-data.git
fi
if [ ! -d moedict-epub ]; then
    git clone --depth 1 https://github.com/g0v/moedict-epub.git
fi
if [ ! -d jieba ]; then
    git clone --depth 1 https://github.com/fxsjy/jieba
fi
if [ ! -e dict-revised.unicode.json ]; then
    cp -v moedict-data/dict-revised.json moedict-epub/
    cd moedict-epub
    perl json2unicode.pl > dict-revised.unicode.json
    cp -v dict-revised.unicode.json ../
    cd ..
fi
if [ ! -e sentences.txt ]; then
    python3 extract_json.py < dict-revised.unicode.json > sentences.txt
fi
