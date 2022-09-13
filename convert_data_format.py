import re
import os
from utils.tagSchemeConverter import BIO2BIOES

LABEL_MAP = {'number': 'NUM',
             'fraction': 'FRAC',
             'range': 'RANGE',
             'date': 'DATE',
             'time': 'TIME',
             'loanword': 'LW',
             'read_as_sequence': 'RAS',
             'composite': 'CPS',
             'measure': 'MSR',
             'address': 'ADD'}

def rasa2bio(s):
    # pre-process
    result = re.findall('\[[^\[]*\]\([^\[]*\)', s)
    for p in result:
        value = p.split('](')[0][1:]
        key = p.split('](')[1][:-1]

        key = LABEL_MAP[key]
        tokens = value.split()
        for i in range(len(tokens)):
            if i == 0:
                tokens[i] = tokens[i] + '+B-' + key
            else:
                tokens[i] = tokens[i] + '+I-' + key
        s = s.replace(p, ' '.join(tokens))

    # convert
    sentence_tokens = s.split()
    s_converted = ''

    for token in sentence_tokens[1:]:
        if len(token.split('+')) > 1:
            s_converted += (token.split('+')[0] + ' ' + token.split('+')[1] + '\n')
        else:
            s_converted += (token + ' ' + 'O' + '\n')

    return s_converted

def rasa2bio_file(input_file, output_file):
    with open(input_file, 'r') as f_in:
        lines = f_in.readlines()
    
    f_out = open(output_file, 'w')
    for line in lines:
        f_out.write(rasa2bio(line) + '\n')

    f_out.close()


# print(rasa2bio(s = 'tổng thống thứ [ba mươi chín](number) của mỹ sẽ được điều trị tại hệ thống chăm sóc y tế [e mo ri](loanword) [heo ke](loanword) tại thành phố [át lan ta](loanword) miền nam của mỹ'))
rasa2bio_file('data/rasa/test.yml', 'data/test.txt')
BIO2BIOES('data/test.txt', 'data/bioes/test.bmes')
os.remove('data/test.txt')