# coding: utf-8
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import datetime
from multiprocessing import Pool
from pathlib import Path
import os
import json
from pprint import pprint as pp
from tqdm import tqdm

# global
data_path = 'cts_0301_0403_news.json'
ud_path = 'ckip_ud.txt'

count = 0
weight = 1
data = list()
user_words = list()
user_dict = dict()

# load data
with open(data_path, 'r') as f:
    for l in f.readlines():
        data.append(json.loads(l))

# load user words
with open(ud_path, 'r') as f:
    for l in f.readlines():
        user_words.append(l.strip())

user_words = list(set(user_words))

# create user dictionary
for w in user_words:
    user_dict[w] = weight

# set construct dictionary
user_dictionary = construct_dictionary(user_dict)

# load zh_ws
path = str(Path.home()) + '/ckip/'
zh_ws = WS(path + '/data')


def get_seg(article):
    global count
    count += 1
    print(count)

    title = article['title']
    content = article['content']

    title_ckiptagger_segment = zh_ws([title], coerce_dictionary=user_dictionary)
    content_ckiptagger_segment = zh_ws([content], coerce_dictionary=user_dictionary)

    article['title_ckiptagger_segment'] = title_ckiptagger_segment[0]
    article['content_ckiptagger_segment'] = content_ckiptagger_segment[0]

    return article


def create_result_json(data, fn='ckip.json'):
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def create_teacher_json(data, fn='teacher.json'):
    with open(fn, 'w+', encoding='utf-8') as f:
        for d in data:
            f.write('{}\n'.format(json.dumps(d, ensure_ascii=False)))


if __name__ == '__main__':
    a = datetime.datetime.now()
    with Pool(4) as p:
        res = p.map(get_seg, [d for d in data])
        create_result_json(res)
        create_teacher_json(res)

    b = datetime.datetime.now()
    print(b - a)
