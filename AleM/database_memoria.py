import sqlite3

# Connessione a un database SQLite in memoria
# ":memory:" significa che il database esiste solo finché l'app è in esecuzione
conn = sqlite3.connect(":memory:", check_same_thread=False)

def create_table():
    """
    Crea le tabelle nel database se non esistono.
    """
    cursor = conn.cursor()

    # Schema per la tabella 'users' (rinominata da 'user' per evitare conflitti con parole chiave SQL)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        hashed_pswd TEXT NOT NULL
    );
    """)

    conn.commit()

# Eseguito per testare se il file funziona
if __name__ == '__main__':
    create_table()
    print("Tabelle create con successo nel database in memoria.")
    # Puoi aggiungere qui query per verificare
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tabelle presenti:", cursor.fetchall())



