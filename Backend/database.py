import os
import sqlite3

DB_NAME = "chat_logs.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions(
    session_id TEXT PRIMARY KEY,
    creation_time DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        creation_time DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            text TEXT NOT NULL,
            session_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        ) 
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reason TEXT NOT NULL,
            session_id TEXT NOT NULL,
            status TEXT CHECK(status IN ('Open', 'Closed')) NOT NULL DEFAULT 'Open',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    ''')

def save_message(session_id: str, sender: str, text:str):

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO sessions(session_id) VALUES(?)", (session_id,)
    )
    cursor.execute(
        "INSERT INTO messages(session_id, sender, text) VALUES(?, ?, ?)",
        (session_id, sender, text)
    )
    
    conn.commit()
    conn.close()

def create_ticket(session_id: str, reason: str):

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tickets(session_id, reason) VALUES(?, ?)",
        (session_id, reason)
    )

    conn.commit()
    conn.close()

def get_chat_history(session_id: str, limit: int = 10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, sender, text FROM messages WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?", 
        (session_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    
    rows.reverse()
    inversed_history = []
    for timestamp, sender, text in rows:
        mapped_role = "assistant" if sender == "bot" else "user"
        inversed_history.append({"role": mapped_role, "content": text})

    return inversed_history


def get_full_chat(session_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, sender, text FROM messages WHERE session_id = ? ORDER BY timestamp ASC", 
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_open_tickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, reason, session_id, timestamp FROM tickets WHERE status = 'Open' ORDER BY timestamp ASC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    print("Базати ни данни chat_logs.db e успешно създадена")