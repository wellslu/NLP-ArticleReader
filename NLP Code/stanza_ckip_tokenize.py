import json
from multiprocessing import Pool
import time
import stanza
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
from pathlib import Path

# load data
file = open('cts_0301_0403_news.json', encoding='utf8')
data = []
for i in file:
    data.append(json.loads(i))

zh_nlp = stanza.Pipeline(lang='zh-hant', processors='tokenize,lemma,pos', use_gpu=False)
# load add words
add_word = []
with open('stanza_ud.txt', 'r', encoding='utf8') as f:
    for l in f.readlines():
        add_word.append(l.strip())

path = str(Path.home()) + '/ckip/'
zh_ws = WS(path + '/data')
weight = 1
user_words = list()
user_dict = dict()

# load user words
with open('ckip_ud.txt', 'r', encoding='utf8') as f:
    for l in f.readlines():
        user_words.append(l.strip())
user_words = list(set(user_words))
# create user dictionary
for w in user_words:
    user_dict[w] = weight
user_dictionary = construct_dictionary(user_dict)


def show(doc):
    global add_word
    title = []
    content = []
    c_sentence = doc['content']
    t_sentence = doc['title']
    n = 0
    while n < len(add_word):
        if add_word[n] in t_sentence:
            t_sentence = t_sentence.replace(add_word[n], '', 1)
        else:
            n += 1
    doc_title = zh_nlp(t_sentence)
    for sent in doc_title.sentences:
        for w in sent.words:
            title.append(w.text)
    n = 0
    while n < len(add_word):
        if add_word[n] in c_sentence:
            c_sentence = c_sentence.replace(add_word[n], '', 1)
        else:
            n += 1
    doc_content = zh_nlp(c_sentence)
    for sent in doc_content.sentences:
        for w in sent.words:
            content.append(w.text)
    doc['title_stanza_segment'] = title
    doc['content_stanza_segment'] = content

    ckip_title = doc['title']
    ckip_content = doc['content']
    title_ckiptagger_segment = zh_ws([ckip_title], coerce_dictionary=user_dictionary)
    content_ckiptagger_segment = zh_ws([ckip_content], coerce_dictionary=user_dictionary)

    doc['title_ckiptagger_segment'] = title_ckiptagger_segment[0]
    doc['content_ckiptagger_segment'] = content_ckiptagger_segment[0]

    return doc


def create_result_json(res_data, fn='result00.json'):
    with open(fn, 'w', encoding='utf-8') as fi:
        json.dump(res_data, fi, ensure_ascii=False, indent=4)


def create_teacher_json(data, fn='teacher.json'):
    with open(fn, 'w+', encoding='utf-8') as f:
        for d in data:
            f.write('{}\n'.format(json.dumps(d, ensure_ascii=False)))


if __name__ == '__main__':
    a = time.time()
    pool = Pool(processes=5)
    chunks = [i for i in data]
    with Pool(5) as p:
        res = p.map(show, chunks)
    pool.close()
    pool.join()
    b = time.time()
    # title_list = []
    # content_list = []
    # for each_title in res[0]:
    #     title_list = title_list + each_title
    # for each_content in res[1]:
    #     content_list = content_list + each_content
    #
    # title = pd.DataFrame({'title': title_list})
    # title = title.groupby(['title'], as_index=False)['title'].agg({'cont': 'count'})
    # title_dict = {}
    # for title_index in range(len(title)):
    #     title_dict[title['title'][title_index]] = title['cont'][title_index]
    #
    # content = pd.DataFrame({'content': content_list})
    # content = content.groupby(['content'], as_index=False)['content'].agg({'cont': 'count'})
    # content_dict = {}
    # for content_index in range(len(content)):
    #     content_dict[content['content'][content_index]] = content['cont'][content_index]
    # data.append()
    print(b - a)
    create_result_json(res)
    create_teacher_json(res)
