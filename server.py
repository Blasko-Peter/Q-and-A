from flask import Flask, render_template, request, redirect
import data_manager
from operator import itemgetter
import os
import datetime
import time


app = Flask(__name__)

UPLOAD_FOLDER = os.path.dirname('image/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/list')
def list_questions():
    rule = request.url_rule
    limit = False
    if 'list' in rule.rule:
        data_list = data_manager.sql_display()
    else:
        limit = True
        limit_number = '5'
        data_list = data_manager.sql_display_limit(limit_number)
    for item in data_list:
        item['submission_time'] = item['submission_time']
        item['vote_number'] = int(item['vote_number'])
    list_head = ['id', 'title', 'submission_time', 'vote_number']
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    if order_by:
        data_list = sorted(data_list, key=itemgetter(order_by))
    if order_direction == 'desc':
        data_list.reverse()
    return render_template('list.html', data_list=data_list, list_head=list_head, limit=limit)


@app.route('/add-question', methods=['GET'])
def add_question():
    return render_template('add_question.html')


@app.route('/add-question', methods=['POST'])
def add_new_question():
    file = request.files['img']
    if file:
        file_image = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_image)
        file_image = file.filename
    else:
        file_image = None
    subtime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    title = request.form['title']
    msg = request.form['msg']
    img = file_image
    data_manager.sql_add(subtime, title, msg, img)
    return redirect('/')


@app.route('/search')
def search():
    words = request.args.get('words')
    keywords = words.split( )
    goals = []
    id_numbers = set()
    for keyword in keywords:
        result = data_manager.sql_search(keyword)
        for item in result:
            goals.append(item)
            id_numbers.add(item['id'])
    search_list = []
    for number in id_numbers:
        index = 0
        for goal in goals:
            if goal['id'] == number and index == 0:
                search_list.append(goal)
                index += 1
    for item in search_list:
        item['submission_time'] = item['submission_time']
        item['vote_number'] = int(item['vote_number'])
    list_head = ['id', 'title', 'submission_time', 'vote_number']
    return render_template('search.html', search_list=search_list, list_head=list_head)


if __name__ == '__main__':
    app.run(host='127.0.0.1',
            port=5000,
            debug=True)
