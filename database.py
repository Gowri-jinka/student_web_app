import sqlite3

def connect():
    return sqlite3.connect("students.db")

def create_table():
    con = connect()
    con.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        course TEXT
    )
    """)
    con.commit()
    con.close()

create_table()
