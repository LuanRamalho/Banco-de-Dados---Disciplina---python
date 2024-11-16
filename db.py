import sqlite3

def connect_db():
    conn = sqlite3.connect("disciplinas.db")
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disciplina TEXT NOT NULL,
        av1 REAL,
        av2 REAL,
        av3 REAL,
        av4 REAL,
        media REAL,
        situacao TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_disciplina(disciplina, av1, av2, av3, av4, media, situacao):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO disciplinas (disciplina, av1, av2, av3, av4, media, situacao) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (disciplina, av1, av2, av3, av4, media, situacao))
    conn.commit()
    conn.close()

def get_all_disciplinas():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT disciplina, av1, av2, av3, av4, media, situacao FROM disciplinas")
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_disciplinas(disciplina):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT disciplina, av1, av2, av3, av4, media, situacao FROM disciplinas WHERE disciplina LIKE ?", ('%' + disciplina + '%',))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_disciplina(old_discipline, new_discipline, av1, av2, av3, av4, media, situacao):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE disciplinas SET disciplina=?, av1=?, av2=?, av3=?, av4=?, media=?, situacao=?
    WHERE disciplina=?
    """, (new_discipline, av1, av2, av3, av4, media, situacao, old_discipline))
    conn.commit()
    conn.close()

def delete_disciplina(disciplina):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM disciplinas WHERE disciplina = ?", (disciplina,))
    conn.commit()
    conn.close()

create_table()
