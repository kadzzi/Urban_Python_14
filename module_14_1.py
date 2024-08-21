import sqlite3


connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(1, 11):
    cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)",
                   (f'User{i}', f'example{i}@gmail.com', i * 10, 1000)
                   )

keys_for_replace = list(range(1, 11, 2))
keys_for_delete = list(range(1, 11))[0:10:3]


for key in keys_for_replace:
    cursor.execute(f"UPDATE Users SET balance = 500 WHERE id = {key}")

for key in keys_for_delete:
    cursor.execute(f"DELETE FROM Users WHERE id = {key}")


connection.commit()
connection.close()
