# coding: utf-8
from flask import Flask, request
from article_reader import ArticleReader
from flask import render_template

app = Flask(__name__, template_folder='templates')

num = 0


@app.route('/article', methods=['GET', 'POST'])
def index():
    global num

    ar = ArticleReader(num)

    if request.method == 'GET':
        html = str(render_template('page.html'))
        try:
            html = html.format(num+1, ar.get_reply(num))
            return html
        except:
            num = 0
            return '出錯了，請重新整理'

    if request.method == 'POST':
        num += 1
        html = str(render_template('page.html'))
        try:
            html = html.format(num+1, ar.get_reply(num))
            return html
        except:
            num = 0
            return '出錯了，請重新整理'


@app.route('/set/<i>', methods=['GET'])
def set_page(i=0):
    global num
    i = str(i)
    
    if i == '0':
        num = 0
        return '改變網址的數字 0 即可跳至您想閱讀的篇數'

    if i.isnumeric():
        input_num = int(i)
        input_num -= 1
        num = input_num

        return '已設定置第 {} 篇'.format(i)
    else:
        return '請輸入數字!'


if __name__ == '__main__':
    print('main page: http://127.0.0.1:5000/article')
    print('setting page: http://127.0.0.1:5000/set/0')
    app.debut = True
    app.run()
