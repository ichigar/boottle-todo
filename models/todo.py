import sqlite3
from table import Table

class Todo(Table):

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
    
    def get_task(self, no):
        data = None
        try:
            conn = self._connect()
            c = conn.cursor()
            c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no),))
            data = c.fetchone()
            conn.commit()
            c.close()
        
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        
        finally:
            if conn:
                conn.close()
            return data
        
    def open_task(self, no):
        try:
            conn = self._connect()
            c = conn.cursor()
            c.execute("UPDATE todo SET status = 1 WHERE id LIKE ?", (str(no),))
            conn.commit()
            c.close()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        finally:
            if conn:
                conn.close()    
            return True
    
    def close_task(self, no):
        try:
            conn = self._connect()
            c = conn.cursor()
            c.execute("UPDATE todo SET status = 0 WHERE id LIKE ?", (str(no),))
            conn.commit()
            c.close()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        finally:
            if conn:
                conn.close()
            return True
