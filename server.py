from flask import Flask, render_template, request, redirect
import data_manager
from operator import itemgetter
import os
import datetime
import time


app = Flask(__name__)

UPLOAD_FOLDER = os.path.dirname('static/images/')
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
        limit_number = '3'
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
    keywords = words.split(' ')
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


@app.route('/question/<question_id>')
def display_question(question_id):
    data_manager.sql_update_view_number(question_id)
    actual_question = data_manager.sql_display_question(question_id)
    answer_list = data_manager.sql_display_answer(question_id)
    comment_to_answer_list = data_manager.sql_display_comment_to_answer()
    comments = data_manager.sql_get_question_comments(question_id)
    return render_template('question.html', question_id=question_id, actual_question=actual_question,
                           actual_answer=answer_list, comment_to_answer_list=comment_to_answer_list, comments=comments)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.sql_delete(question_id)
    return redirect('/')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question_data = data_manager.sql_display_question(question_id)
    if request.method == 'GET':
        return render_template('add_question.html', question_data=question_data)
    else:
        try:
            file = request.files['img']
            file_image = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_image)
            file_image = file.filename
        except:
            file_image = ''
        subtime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        title = request.form['title']
        msg = request.form['msg']
        img = file_image
        data_manager.sql_update(question_id, subtime, title, msg, img)
        return redirect('/question/' + question_id)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'GET':
        actual_question = data_manager.sql_display_question(question_id)
        return render_template('answer.html', question_id=question_id, actual_question=actual_question)
    if request.method == 'POST':
        subtime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        new_question_id = question_id
        msg = request.form['answer']
        img = ''
        data_manager.sql_post_answer(subtime, new_question_id, msg, img)
        return redirect('/question/' + str(question_id))


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'GET':
        actual_answer = data_manager.sql_display_actual_answer(answer_id)
        return render_template('answer.html', answer_id=answer_id, actual_answer=actual_answer)
    if request.method == 'POST':
        actual_question_id = str((data_manager.sql_display_actual_answer(answer_id))[0]['question_id'])
        subtime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        msg = request.form['answer']
        data_manager.sql_update_answer(answer_id, subtime, msg)
        return redirect('/question/' + actual_question_id)


@app.route('/answer/<question_id>/<answer_id>/delete')
def delete_answer(question_id, answer_id):
    data_manager.sql_delete_answer(answer_id)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment(question_id):
    if request.method == 'GET':
        return render_template('comment.html')
    elif request.method == 'POST':
        question_id = question_id
        message = request.form['message']
        subtime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        data_manager.sql_add_comment_to_question(question_id, message, subtime)
        return redirect('/question/' + question_id)


@app.route('/comments/<comment_id>/delete')
def com_del(comment_id):
    question_id = get_question_id(comment_id)
    data_manager.sql_comdel(comment_id)
    return redirect('/question/' + str(question_id))


def get_question_id(comment_id):
    index = data_manager.question_or_answer(comment_id)
    if index['question_id'] == None:
        question_id_list = data_manager.get_question_id(comment_id)
        question_id = question_id_list['question_id']
    else:
        question_id = index['question_id']
    return question_id


@app.route('/comments/<comment_id>/edit', methods=['GET', 'POST'])
def comment_edit(comment_id):
    if request.method == 'GET':
        comment_data = data_manager.get_comment_data(comment_id)
        return render_template('comment.html', comment_data=comment_data)
    else:
        message=request.form['message']
        data_manager.sql_comment_edit(comment_id,message)
        question_id = get_question_id(comment_id)
        return redirect('/question/' + str(question_id))


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_answer(answer_id):
    if request.method == 'GET':
        return render_template('comment.html', answer_id=answer_id)
    elif request.method == 'POST':
        actual_question_id = str((data_manager.sql_display_actual_answer(answer_id))[0]['question_id'])
        message = request.form['message']
        subtime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        data_manager.sql_add_comment_to_answer(answer_id, message, subtime)
        return redirect('/question/' + actual_question_id)


if __name__ == '__main__':
    app.run(host='127.0.0.1',
            port=5000,
            debug=True)
