#region CONNECTION TO DATABASE
import sqlite3
import calendar
import datetime
calendar.setfirstweekday(calendar.MONDAY)
#endregion
#region DB TABLES
'''
    В этом регионе описал создание всех сущностей БД с полями и связями
'''
def table_Dannye_avtorizacii():
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dannve_avtorizacii(
        ID INTEGER PRIMARY KEY NOT NULL,
        Login NVARCHAR NOT NULL, 
        Password NVARCHAR NOT NULL,
        ID_Sotrudnik INTEGER, 
        FOREIGN KEY (ID_Sotrudnik) REFERENCES Sotrudnik (ID)
    )
    ''')
def table_Pol():
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pol(
            ID INTEGER PRIMARY KEY NOT NULL,
            Name NVARCHAR NOT NULL,
            FOREIGN KEY (ID) REFERENCES Sotrudnik (ID_Pol)
        )
    ''')
def table_Sotrudnik():
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sotrudnik(
            ID INTEGER PRIMARY KEY NOT NULL,
            Family NVARCHAR(50) NOT NULL,
            Name NVARCHAR(30) NOT NULL,
            Otchestvo NVARCHAR(30) NOT NULL,
            Phone NVARCHAR(12),
            Work_phone NVARCHAR(12) NOT NULL,
            Address_email NVARCHAR(150), 
            ID_Role INTEGER NOT NULL,
            ID_Doljnost INTEGER NOT NULL,
            ID_Pol INTEGER NOT NULL,
            FOREIGN KEY (ID_Role) REFERENCES Role (ID),
            FOREIGN KEY (ID_Doljnost) REFERENCES Doljnost (ID),
            FOREIGN KEY (ID_Pol) REFERENCES Pol (ID)
        )
    ''')
def table_Kotocafe():
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS Kotocafe(
            ID INTEGER PRIMARY KEY NOT NULL,
            Name NVARCHAR(50) NOT NULL,
            Adress NVARCHAR(250) NOT NULL,
            INN NVARCHAR(12) NOT NULL,
            Otvetstvennoe_litso NVARCHAR(250) NOT NULL,
            ID_Sotrudnik INTEGER NOT NULL,
            ID_Tarif INTEGER NOT NULL,
            FOREIGN KEY (ID_Sotrudnik) REFERENCES Sotrudnik (ID),
            FOREIGN KEY (ID_Tarif) REFERENCES Tarif (ID)
         )
    ''')
def table_Role():
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Role(
            ID INTEGER PRIMARY KEY NOT NULL,
            Name NVARCHAR(150) NOT NULL,
            Prava_dostupa NVARCHAR
        )
    ''')
def table_Kassovaya_sessiya():
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Kassovaya_sessiya(
            ID INTEGER PRIMARY KEY NOT NULL,
            Time_start TIME NOT NULL,
            Time_end TIME NOT NULL,
            Nachalniy_ostatok NVARCHAR(50) NOT NULL,
            Ojidaemiy_ostatok NVARCHAR(50) NOT NULL,
            Fakticheskiy_ostatok NVARCHAR(50) NOT NULL,
            Rashozhdenie NVARCHAR(50) NOT NULL,
            ID_Smena INTEGER NOT NULL,
            ID_Tranzaktsiya INTEGER NOT NULL,
            FOREIGN KEY (ID_Smena) REFERENCES Smena (ID),
            FOREIGN KEY (ID_Tranzaktsiya) REFERENCES Tranzaktsiya (ID)
        )
    ''')
def table_Smena():
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Smena(
            ID INTEGER PRIMARY KEY NOT NULL,
            Date DATE NOT NULL,
            Planovoe_nachalo TIME NOT NULL,
            Planovoe_okonchanie TIME NOT NULL,
            Dlitelnost TIME NOT NULL,
            ID_Sotrudnik INTEGER NOT NULL,
            FOREIGN KEY (ID_Sotrudnik) REFERENCES Sotrudnik (ID)
        )
    ''')
def table_Tarif():
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tarif(
            ID INTEGER PRIMARY KEY NOT NULL,
            Name NVARCHAR(50) NOT NULL,
            Stoimost_za_minuty INTEGER NOT NULL,
            Opisanie NVARCHAR,
            Date_start DATE,
            Date_end DATE
        )
    ''')
def table_Doljnost():
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Doljnost(
            ID INTEGER PRIMARY KEY NOT NULL,
            Name NVARCHAR(100) NOT NULL,
            Stavka NVARCHAR(50) NOT NULL
        )
    ''')
def table_Poseshenie():
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Poseshenie(
            ID INTEGER PRIMARY KEY NOT NULL,
            Date DATE NOT NULL,
            Kol_vo_posetiteley INTEGER NOT NULL,
            Adress_filial NVARCHAR(250) NOT NULL,
            Time_start TIME NOT NULL,
            Time_end TIME NOT NULL,
            Kol_vo_minut INTEGER NOT NULL,
            ID_Kotocafe INTEGER NOT NULL,
            FOREIGN KEY (ID_Kotocafe) REFERENCES Kotocafe (ID)
        )
    ''')
def table_Tranzaktsiya():
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tranzaktsiya(
        ID INTEGER PRIMARY KEY NOT NULL,
        Sposob_oplaty NVARCHAR(50) NOT NULL,
        Summa_k_oplate NVARCHAR(50) NOT NULL,
        Date DATE NOT NULL,
        Time TIME NOT NULL,
        Status NVARCHAR(50) NOT NULL,
        ID_Poseshenie INTEGER NOT NULL,
        FOREIGN KEY (ID_Poseshenie) REFERENCES Poseshenie (ID)
        )
    ''')
#endregion
#region CREATE USER

#endregion
#region GET USER DATA
def get_user_data(login):
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    data = {}
    x=cursor.execute('''
        SELECT ID_Sotrudnik FROM Dannve_avtorizacii WHERE Login = ?
    ''',(login,)).fetchone()
    data['ID_Sotrudnik'] = x[0]
    x = cursor.execute('''
            SELECT * FROM Sotrudnik WHERE ID = ?
        ''', (data['ID_Sotrudnik'],)).fetchone()
    data['Family'],data['Name'],data['Otchestvo'],data['Phone'], data['Work_phone'],data['Email'], data['ID_Role'],data['ID_Doljnost'],data['ID_Pol'] = x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9]
    data['avatar_url'] = "user_avatar.png"
    connection.close()
    return data

def get_ID_by_family(family):
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    data = cursor.execute('''
        SELECT ID FROM Sotrudnik WHERE Family = ?
    ''', (family, )).fetchone()
    return data[0]
def get_employee_by_ID(id):
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    if id==0:
        d = cursor.execute('''
                SELECT Family FROM Sotrudnik
            ''').fetchall()
        return d
    else:
        d = cursor.execute('''
            SELECT Family FROM Sotrudnik WHERE ID = ?
        ''', (id,)).fetchone()
        return d[0]

def get_calendar_data(year, month, shifts_by_date):
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    days_in_prev = calendar.monthrange(prev_year, prev_month)[1]
    # Текущий
    days_in_current = calendar.monthrange(year, month)[1]
    first_weekday = calendar.monthrange(year, month)[0]  # 0 = понедельник
    # Следующий
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    grid = []
    # Дни предыдущего месяца
    for i in range(first_weekday):
        day_num = days_in_prev - first_weekday + i + 1
        date_str = f"{day_num:02d}.{prev_month:02d}.{prev_year}"
        grid.append(
            {'date': date_str, 'day': day_num, 'is_current_month': False, 'shifts': shifts_by_date.get(date_str, [])})

    # Дни текущего месяца
    for d in range(1, days_in_current + 1):
        date_str = f"{d:02d}.{month:02d}.{year}"
        grid.append({'date': date_str, 'day': d, 'is_current_month': True, 'shifts': shifts_by_date.get(date_str, [])})

    # Заполняем оставшиеся ячейки днями следующего месяца
    remaining = 42 - len(grid)
    for i in range(remaining):
        date_str = f"{i + 1:02d}.{next_month:02d}.{next_year}"
        grid.append(
            {'date': date_str, 'day': i + 1, 'is_current_month': False, 'shifts': shifts_by_date.get(date_str, [])})

    weeks = [grid[i:i + 7] for i in range(0, len(grid), 7)]
    return weeks

def create_user(login, password):
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    last_id = cursor.execute('''
            SELECT ID FROM Dannve_avtorizacii
    ''').fetchall()
    new_id = 0
    if last_id == []:
        new_id=1
    else:
        new_id= last_id[-1][0]+1
    cursor.execute('''
        INSERT INTO Dannve_avtorizacii (ID, Login, Password, ID_Sotrudnik) VALUES(?,?,?,?)
    ''', (new_id,login, password, new_id))
def create_shift(date, start_time, end_time, employee):
    """date приходит как '2026-04-15' → сохраняем как '15.04.2026'"""
    try:
        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        db_date = dt.strftime('%d.%m.%Y')
    except:
        db_date = date

    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()

    last_id = cursor.execute("SELECT ID FROM Smena ORDER BY ID DESC").fetchone()
    new_id = 1 if not last_id else last_id[0] + 1

    fam = get_ID_by_family(employee)

    cursor.execute('''
        INSERT INTO Smena (ID, Date, Planovoe_nachalo, Planovoe_okonchanie, Dlitelnost, ID_Sotrudnik)
        VALUES(?,?,?,?,?,?)
    ''', (new_id, db_date, start_time, end_time, 0, fam))

    connection.commit()
    connection.close()
    print(f"Смена сохранена: {db_date} {start_time}–{end_time} (ID={new_id})")

def get_shifts(year=None, month=None):
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()

    if year is None or month is None:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month

    # Надёжный поиск по месяцу и году (не зависит от строкового сравнения)
    rows = cursor.execute('''
        SELECT Date, Planovoe_nachalo, Planovoe_okonchanie, ID_Sotrudnik, ID 
        FROM Smena 
        WHERE substr(Date, 4, 2) = ? 
          AND substr(Date, 7, 4) = ?
        ORDER BY Date, Planovoe_nachalo
    ''', (f"{month:02d}", str(year))).fetchall()

    print(f"DEBUG: Найдено {len(rows)} смен за {month:02d}.{year}")

    shifts_by_date = {}
    for row in rows:
        d = row[0]   # '25.04.2026'
        shifts_by_date.setdefault(d, []).append({
            'id': row[4],                    # настоящий ID смены
            'employee': get_employee_by_ID(row[3]),
            'start': row[1],
            'end': row[2]
        })

    weeks = get_calendar_data(year, month, shifts_by_date)

    months = {1:'Январь',2:'Февраль',3:'Март',4:'Апрель',5:'Май',6:'Июнь',
              7:'Июль',8:'Август',9:'Сентябрь',10:'Октябрь',11:'Ноябрь',12:'Декабрь'}

    employees_raw = get_employee_by_ID(0)
    employees = [row[0] for row in employees_raw]

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return {
        'weeks': weeks,
        'year': year,
        'month_name': months[month],
        'employees': employees,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month
    }

def update_shift(employee, start_time, end_time, id_smena):
    connection = sqlite3.connect('kotocafe.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE Smena
        SET ID_Sotrudnik = ?, Planovoe_nachalo = ?, Planovoe_okonchanie = ?
        WHERE ID = ? 
    ''', (get_ID_by_family(employee), start_time, end_time, id_smena))
    connection.commit()
    connection.close()

#endregion
"""def sotrudnik(ID, Family, Name, Otchestvo, Phone, Work_phone, Address_email,ID_Role, ID_Doljnost, ID_Pol):
    cursor.execute('''
        INSERT INTO Sotrudnik (ID, Family, Name, Otchestvo, Phone, Work_phone, Address_email,
         ID_Role, ID_Doljnost, ID_Pol) VALUES (?,?,?,?,?,?,?,?,?,?)
    ''', (ID, Family, Name, Otchestvo, Phone, Work_phone, Address_email,ID_Role, ID_Doljnost, ID_Pol))
sotrudnik(1, 'Оболенский', 'Даниил','Алексеевич', '88005553535', '88006663636',
          'example@gmail.com', '1','1','1',)"""


"""
'''
Создание БД. Статус: Deprecated
'''
#todo Убрать на проде!

table_Dannye_avtorizacii()
table_Pol()
table_Sotrudnik()
table_Kotocafe()
table_Role()
table_Kassovaya_sessiya()
table_Smena()
table_Tarif()
table_Doljnost()
table_Poseshenie()
table_Tranzaktsiya()
connection.commit()
connection.close()
"""

