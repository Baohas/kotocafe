from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'my_strong_secret_key_hz'
import DB_utils
#функция подключения к БД
def get_db_connection():
    conn = sqlite3.connect('kotocafe.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def log_in():
    return redirect('/login')

# Маршрут для страницы авторизации
@app.route('/login', methods=['GET'])
def login():
    return render_template('auth.html', auth_class='default')

# Маршрут для обработки отправки формы авторизации
@app.route('/dashboard', methods=['POST'])
def authenticate():

    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM Dannve_avtorizacii WHERE Login = ? AND Password = ?',
        (username, password)
    ).fetchone()
    conn.close()

    if user is not None:
        data = DB_utils.get_user_data(username)
        session['Data'] = data
        print(session['Data'])
        return redirect(url_for('dashboard'))
    else:
        auth_class='failure'
        return render_template('auth.html', auth_class='failure')

# Маршрут для страницы дэшборда
@app.route('/dashboard')
def dashboard():
    try:
        return render_template('dashboard.html', user_name=session['Data']['Name'],
                           user_otchestvo=session['Data']['Otchestvo'],smena_id=10, smena_date='01.01.26',
                           Nachalniy_ostatok=6666)
    except:
        return redirect('/login')

# Редирект юзера на страницу авторизации
@app.route('/change_user')
def change_user():
    session.clear()
    return redirect('/login')

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)