import sqlite3
from table import Table

TABLE_NAME = 'todo'
class Todo(Table):
    def __init__(self, db_name):
        super().__init__(db_name)
        self._table_name = TABLE_NAME
        
    def create(self):
        try:
            conn = self._connect()
            c = conn.cursor()
            c.execute(conn.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL)"))
            conn.commit()
            c.close()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        finally:
            if conn:
                conn.close()
            return True
    

