# coding: utf-8
import json
import time
import threading
import os


class ArticleReader:
    title_display = '''
    原標題:
    {}

    標題斷詞:
    {}

    '''

    content_display = '''
    內容原文:
    {}

    內容斷詞:
    {}

    '''

    def __init__(self, start=0):
        self.data = ArticleReader.get_data()
        self.article_index = start

        self.keyboard = threading.Thread()
        self.screen = threading.Thread()

        self.mode = 'title'

        self.row_len = 15

        self.raw_title = None
        self.ckip_title = None
        self.stanza_title = None

        self.raw_content = None
        self.ckip_content = None
        self.stanza_content = None


    @staticmethod
    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    @staticmethod
    def get_data():
        with open('raw_data/article.json', encoding='utf-8') as f:
            return json.loads(f.read())

    def raw_title_setter(self):
        self.raw_title = self.data[self.article_index].get('title')

    def ckip_title_setter(self):
        segs = self.data[self.article_index].get('title_ckiptagger_segment')
        segs = list(ArticleReader.chunks(segs, self.row_len))
        display = ''
        for row in segs:
            for s in row:
                display += '{'+s+'}' + '&nbsp;&nbsp;'
            display += '<br>'

        self.ckip_title = display

    def stanza_title_setter(self):
        segs = self.data[self.article_index].get('title_stanza_segment')
        segs = list(ArticleReader.chunks(segs, self.row_len))
        display = ''
        for row in segs:
            for s in row:
                display += '{'+s+'}' + '&nbsp;&nbsp;'
            display += '<br>'

        self.stanza_title = display

    def raw_content_setter(self):
        self.raw_content = self.data[self.article_index].get('content')

    def ckip_content_setter(self):
        segs = self.data[self.article_index].get('content_ckiptagger_segment')
        segs = list(ArticleReader.chunks(segs, self.row_len))
        display = ''
        for row in segs:
            for s in row:
                display += '{' + s + '}' + '&nbsp;&nbsp;'
            display += '<br><br>'

        self.ckip_content = display

    def stanza_content_setter(self):
        segs = self.data[self.article_index].get('content_stanza_segment')
        segs = list(ArticleReader.chunks(segs, self.row_len))
        display = ''
        for row in segs:
            for s in row:
                display += '{' + s + '}' + '&nbsp;&nbsp;'
            display += '<br><br>'

        self.stanza_content = display


    def get_reply(self, art_index: int):
        self.article_index = art_index
        self.raw_title_setter()
        self.ckip_title_setter()
        self.stanza_title_setter()
        self.raw_content_setter()
        self.ckip_content_setter()
        self.stanza_content_setter()

        result = '''
        <div>
        <h5>{}</h5>
        <div style="color:#A830FF"; border:2px #ccc solid;>{}</div>
        <br>
        <div style="color:#088A4B"; border:2px #ccc solid;>{}</div>
        </div>
        <div>
        <h5>{}</h5>
        <div style="color:#A830FF"; border:2px;>{}</div>
        <br>
        <div style="color:#088A4B"; border:2px #ccc solid;>{}</div>
        </div>
        '''.format(self.raw_title, self.ckip_title, self.stanza_title, self.raw_content, self.ckip_content, self.stanza_content)

        return result
