import sqlite3

DATABASE = 'quiz.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS questions
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    option1 TEXT NOT NULL,
                    option2 TEXT NOT NULL,
                    option3 TEXT NOT NULL,
                    option4 TEXT NOT NULL,
                    correct_options TEXT NOT NULL)''')
    conn.commit()
    conn.close()


def populate_db():
    questions = [
        ('What is the capital of India?', 'Chennai', 'Mumbai', 'New Delhi', 'Kolkata', '3'),
        ('What is 2 + 2?', '3', '4', '5', '6', '2'),
        ('Which country has most population in the world?', 'China', 'India', 'United States', 'Russia', '2'),
        ('Which numbers are prime?', '1', '2', '3', '5', '2,3,4'),  # Example with multiple correct options
    ]
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.executemany('''INSERT INTO questions (question, option1, option2, option3, option4, correct_options)
                       VALUES (?, ?, ?, ?, ?, ?)''', questions)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    populate_db()
    print("Database initialized and populated with initial data.")
