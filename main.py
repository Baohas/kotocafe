from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session,jsonify
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

@app.route('/schedule', methods=['GET', 'POST'])
def schedule_page():
    if 'Data' not in session:
        if request.method == 'POST':
            return jsonify({'success': False, 'error': 'Не авторизован'}), 401
        return redirect('/login')
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)

    if request.method=='POST':
        try:
            if not request.is_json:
                print("❌ Запрос не содержит JSON (Content-Type:", request.content_type, ")")
                return jsonify({'success': False, 'error': 'Content-Type должен быть application/json'}), 415
            data = request.get_json()
            print("📥 Получено от JS:", data)
            DB_utils.create_shift(data['date'],data['start_time'], data['end_time'], data['employee'])


            if data is None or not isinstance(data, dict):
                return jsonify({'success': False, 'error': 'Пустое или некорректное JSON тело'}), 400

            if not all(k in data for k in ['date', 'employee', 'start_time', 'end_time']):
                return jsonify({'success': False, 'error': 'Отсутствуют обязательные поля'}), 400

            return jsonify({'success': True})
        except Exception as e:
            print("Ошибка при добавлении смены:", e)
            return jsonify({'success': False, 'error': str(e)}), 400

    data = DB_utils.get_shifts(year, month)
    return render_template('smeny.html', weeks=data['weeks'],
                           year=data['year'], month_name=data['month_name'],
                           employees=data['employees'], prev_year=data['prev_year'],
                           prev_month=data['prev_month'], next_year=data['next_year'],
                           next_month=data['next_month'])

if __name__ == '__main__':
    app.run(debug=True)