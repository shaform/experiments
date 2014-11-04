import jieba
import sys

if __name__ == '__main__':
    jieba.set_dictionary('jieba/extra_dict/dict.txt.big')
    for l in sys.stdin:
        words = jieba.cut(l.strip())
        sys.stdout.write((u' '.join(words) + u'\n').encode('utf8'))
