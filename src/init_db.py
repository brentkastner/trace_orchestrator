import sqlite3
import secrets

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO clients (name, hash) VALUES (?, ?)",
            ('Seed Client', "wKFv06_08lboHBo7l5NJIA")
            )

connection.commit()
connection.close()