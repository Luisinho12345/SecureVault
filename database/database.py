import sqlite3

DATABASE_NAME = "securevault.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            username TEXT,
            password TEXT,
            website TEXT,
            category TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()

    # Migracao: adiciona a coluna pin_hash se ainda nao existir
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN pin_hash TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # a coluna ja existe

    conn.close()
