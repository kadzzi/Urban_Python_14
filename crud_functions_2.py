import sqlite3

FILE_DB = 'telegram_bot_DB.db'


def initiate_db():
    connection_ = sqlite3.connect(FILE_DB)
    cursor_ = connection_.cursor()

    cursor_.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    cursor_.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')

    connection_.commit()
    connection_.close()


def get_all_products():
    connection_ = sqlite3.connect(FILE_DB)
    cursor_ = connection_.cursor()

    cursor_.execute("SELECT title, description, price from Products")
    result = cursor_.fetchall()

    connection_.commit()
    connection_.close()

    return result


def is_included(username):
    connection_ = sqlite3.connect(FILE_DB)
    cursor_ = connection_.cursor()

    cursor_.execute(f"SELECT Count(*) FROM Users WHERE username = '{username}'")
    result = bool(cursor_.fetchone()[0])

    connection_.commit()
    connection_.close()

    return result


def add_user(username, email, age):
    connection_ = sqlite3.connect(FILE_DB)
    cursor_ = connection_.cursor()

    cursor_.execute("INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)",
                    (username, email, age, 1000))

    connection_.commit()
    connection_.close()


if __name__ == "__main__":
    initiate_db()

    connection = sqlite3.connect(FILE_DB)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)",
                   ('Зеленоцвет', 'Снимает усталость', 200))
    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)",
                   ('Цветущий зеленоцвет', 'Лечит переутомление', 500))
    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)",
                   ('Пурпурный мох', 'Лечит отравление', 1000))
    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)",
                   ('Цветущий пурпурный мох', 'Выводит яды и токсины', 2000))

    connection.commit()
    connection.close()

    product_list = get_all_products()
    print(product_list)
