from flask import Flask, render_template, request
import data_manager
from operator import itemgetter


app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(host='127.0.0.1',
            port=5000,
            debug=True)
