import sqlite3
from .config import DB_NAME


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = self.dict_factory
        self.cur = self.conn.cursor()

    def dict_factory(self,cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def insert(self,data,table_name='spirals'):
        self.cur.execute(f"INSERT INTO {table_name} VALUES ({data[0]}, {data[1]}, {data[2]}, {data[3]})")
        self.conn.commit()

    def get_all(self):
        self.cur.execute("SELECT * FROM spirals")
        rows = self.cur.fetchall()
        return rows

    def get(self, table_id,row_id,col_id):
        self.cur.execute(f"SELECT * FROM spirals WHERE table_id = {table_id} AND row_id = {row_id} AND col_id = {col_id}")
        rows = self.cur.fetchall()
        return rows
    
    def get_last_id(self):
        self.cur.execute("SELECT last FROM last_table")
        rows = self.cur.fetchall()
        return int(rows[0]['last'])
    
    def set_last_id(self,id):
        self.cur.execute(f"UPDATE last_table SET last = {id}")
        self.conn.commit()

    def close(self):
        self.conn.close()