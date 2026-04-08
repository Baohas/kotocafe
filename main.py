from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
app = Flask(__name__)
app.secret_key = 'my_strong_secret_key_hz'

#функция подключения к БД
def get_db_connection():
    conn = sqlite3.connect('kotocafe.db')
    conn.row_factory = sqlite3.Row
    return conn

# Маршрут для страницы авторизации
@app.route('/login', methods=['GET'])
def login():
    return render_template('auth.html', auth_class='default')

# Маршрут для обработки отправки формы авторизации
@app.route('/dashboard', methods=['POST'])
def authenticate():

    username = request.form['username']
    password = request.form['password']
    print(username,password)
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM Dannve_avtorizacii WHERE Login = ? AND Password = ?',
        (username, password)
    ).fetchone()
    conn.close()

    if user is not None:
        session['Login'] = username
        return redirect(url_for('dashboard'))
    else:
        auth_class='failure'
        return render_template('auth.html', auth_class='failure')

@app.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)