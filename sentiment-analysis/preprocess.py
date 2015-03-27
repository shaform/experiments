import argparse
import re
import socket


def seg_it(q_str, *, server, port, user, password, pos=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    query = ('<?xml version="1.0" ?>' +
             '<wordsegmentation version="0.1" charsetcode="utf-8">' +
             '<option showcategory="0" />' +
             '<authentication username="' + user + '" password="' + password +
             '" /><text><![CDATA[' + q_str + ']]></text></wordsegmentation>')
    sock.send(query.encode(encoding='utf-8'))
    result = sock.recv(1048576).decode('utf-8', errors='ignore')
    sock.close()
    try:
        stripped = result.replace('</sentence><sentence>', '').split(
            '<sentence>')[1].split('</sentence>')[0]
    except:
        print(q_str)
        print(result)
        raise
    if pos:
        return stripped.replace('\u3000', ' ').strip()
    else:
        return re.sub(r'\([^) ]+\)(\u3000|$)', ' ', stripped).strip()


def process_commands():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', required=True)
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--user', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)

    return parser.parse_args()

if __name__ == '__main__':
    args = process_commands()

    data_set = set()
    with open(args.input, 'r') as f:
        while True:
            cls = f.readline()
            line = f.readline()

            if not line:
                break

            data_set.add((int(cls), line.split('|', 1)[1].strip()))

    with open(args.output, 'w') as f:
        for i, (cls, text) in enumerate(data_set):
            try:
                f.write('{} {}\n'.format(cls,
                                         seg_it(text,
                                                server=args.server,
                                                port=args.port,
                                                user=args.user,
                                                password=args.password)))
            except IndexError:
                pass
            if i % 100 == 99:
                print('{} processed'.format(i + 1))
