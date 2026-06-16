from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('memos.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')
        content = request.form.get('content')

        if not title or not date or not content:
            return render_template('error.html')

        conn = get_db()
        conn.execute(
            'INSERT INTO memos (title, date, content) VALUES (?, ?, ?)',
            (title, date, content)
        )
        conn.commit()
        conn.close()

        return redirect('/list')

    return render_template('form.html')

@app.route('/list')
def memo_list():
    conn = get_db()
    memos = conn.execute('SELECT * FROM memos').fetchall()
    conn.close()
    return render_template('list.html', memos=memos)

@app.route('/detail/<int:id>')
def detail(id):
    conn = get_db()
    memo = conn.execute('SELECT * FROM memos WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('detail.html', memo=memo)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')
        content = request.form.get('content')
        conn.execute(
            'UPDATE memos SET title = ?, date = ?, content = ? WHERE id = ?',
            (title, date, content, id)
        )
        conn.commit()
        conn.close()
        return redirect('/detail/' + str(id))

    memo = conn.execute('SELECT * FROM memos WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', memo=memo)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)