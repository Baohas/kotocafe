#region CONNECTION TO DATABASE
import sqlite3

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
        new_id= last_id[0][0]+1
    cursor.execute('''
        INSERT INTO Dannve_avtorizacii (ID, Login, Password, ID_Sotrudnik) VALUES(?,?,?,?)
    ''', (new_id,login, password, new_id))
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
#endregion
"""def sotrudnik(ID, Family, Name, Otchestvo, Phone, Work_phone, Address_email,ID_Role, ID_Doljnost, ID_Pol):
    cursor.execute('''
        INSERT INTO Sotrudnik (ID, Family, Name, Otchestvo, Phone, Work_phone, Address_email,
         ID_Role, ID_Doljnost, ID_Pol) VALUES (?,?,?,?,?,?,?,?,?,?)
    ''', (ID, Family, Name, Otchestvo, Phone, Work_phone, Address_email,ID_Role, ID_Doljnost, ID_Pol))
sotrudnik(1, 'Оболенский', 'Даниил','Алексеевич', '88005553535', '88006663636',
          'example@gmail.com', '1','1','1',)"""
get_user_data('Razvodyatel')

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

