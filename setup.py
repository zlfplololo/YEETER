import sqlite3
connection = sqlite3.connect('data.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                    at TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    password TEXT NOT NULL
               )''')
# cursor.execute('''INSERT INTO users (at, name, password) VALUES ('ben', 'ben robinson', '123');''')
# connection.commit()
cursor.execute('''SELECT password FROM users where at = 'mel' ''')
print(cursor.fetchall())
connection.close()