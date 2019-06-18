from flask import Flask, render_template, request, redirect


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list_questions():
    return render_template('list.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1',
            port=5000,
            debug=True)
