import argparse
import json
import re
import sys


def yield_moe_sentences(json_obj):
    r = re.compile(r'{\[.\*\]}')
    for x in yield_sentences(json_obj):
        if r.search(x) is None:
            yield x

def yield_sentences(json_obj):
    for item in json_obj:
        for heteronym in item['heteronyms']:
            for definition in heteronym['definitions']:
                if 'def' in definition:
                    sen = definition['def']
                    if len(sen) > 0 and '異體字。' not in sen and '<' not in sen:
                        yield sen
                if 'quote' in definition:
                    yield from definition['quote']

if __name__ == '__main__':
    moe_json = json.load(sys.stdin)
    for x in yield_moe_sentences(moe_json):
        sys.stdout.write(x + '\n')
