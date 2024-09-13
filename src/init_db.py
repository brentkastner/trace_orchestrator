import sqlite3
import secrets

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

client_hash = secrets.token_urlsafe(16)

cur.execute("INSERT INTO clients (name, hash) VALUES (?, ?)",
            ('Seed Client', client_hash)
            )

connection.commit()
connection.close()