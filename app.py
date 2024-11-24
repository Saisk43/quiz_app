from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'quiz.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/quiz')
def quiz():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM questions')
    questions = cur.fetchall()
    conn.close()
    return render_template('quiz.html', questions=questions)


@app.route('/submit', methods=['POST'])
def submit():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM questions')
    questions = cur.fetchall()
    conn.close()

    score = 0
    for question in questions:
        print(question['question'])
        q_id = str(question['id'])
        selected_option = request.form.get(q_id)
        correct_options = question['correct_options'].split(',')
        if selected_option in correct_options:
            score += 1

    return render_template('result.html', score=score, total=len(questions))


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_options = request.form.getlist('correct_options')

        correct_options_str = ','.join(correct_options)

        conn = get_db()
        cur = conn.cursor()
        cur.execute('''INSERT INTO questions (question, option1, option2, option3, option4, correct_options)
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (question, option1, option2, option3, option4, correct_options_str))
        conn.commit()
        conn.close()
        return redirect(url_for('quiz'))
    return render_template('add_question.html')


if __name__ == "__main__":
    app.run(debug=True)
