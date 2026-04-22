import sqlite3

DB_PATH = "fraud.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        amount_usd REAL,
        country TEXT,
        payment_channel TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_fraud INTEGER
    )
    """)

    conn.commit()
    conn.close()