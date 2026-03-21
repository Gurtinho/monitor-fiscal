# cria a conexão com o sqlite

from dbm import sqlite3


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_file)
            self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                texto TEXT NOT NULL,
                url TEXT NOT NULL,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def insert_nota(self, tipo, texto, url):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO notas (tipo, texto, url) VALUES (?, ?, ?)
        ''', (tipo, texto, url))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None