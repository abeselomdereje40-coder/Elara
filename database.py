import sqlite3
import os

db_name = os.path.abspath("elara.db")
print("Elara database: ",db_name)

def get_connection():
    conn=sqlite3.connect(db_name,check_same_thread=False,timeout=10)
    conn.row_factory=sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=10000")
    return conn

def initial():
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    role TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fact TEXT,
    catagory TEXT,
    importance INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    description TEXT,
    status TEXT,
    priority TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    task TEXT,
    status TEXT,
    deadline TEXT,
    FOREIGN KEY(project_id) REFERENCES projects(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_notes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    note TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES projects(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    source TEXT,
    tags TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_state(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    vision TEXT,
    current_phase TEXT,
    current_module TEXT,
    current_goal TEXT,
    next_goal TEXT,
    completion INTEGER,
    last_updated DATETIME,
    FOREIGN KEY (last_updated) REFERENCES projects(updated_at)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_plan(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    step_number INTEGER,
    title TEXT,
    status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_chunks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    knowledge_id INTEGER NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    location TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(knowledge_id) REFERENCES knowledge(id)
    )
    """)

    conn.commit()
    conn.close()
