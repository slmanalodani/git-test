import sqlite3
from flask import g

DATABASE = "pyramids.db"

# Function to get a database connection
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Close the database connection when the app context ends
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# Initialize the database (create tables if they don't exist)
def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            height INTEGER NOT NULL,
            pyramid TEXT NOT NULL
        )
    """)
    db.commit()

# Insert a new submission into the database
def insert_submission(name, height, pyramid):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO submissions (name, height, pyramid) VALUES (?, ?, ?)", (name, height, pyramid))
    db.commit()

# Retrieve all submissions from the database
def get_submissions():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, height, pyramid FROM submissions")
    return cursor.fetchall()
