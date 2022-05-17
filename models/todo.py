import sqlite3
class Todo:
    def __init__(self, database):
        self.database = database
    
    def __connect(self):
        conn = sqlite3.connect(self.database)
        return conn

    
    def select(self):
        conn = self.__connect()
        c = conn.cursor()
        c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
        data = c.fetchall()
        conn.commit()
        c.close()
        return data
    
    def get_task(self, id):
        conn = self.__connect()
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (id,))
        data = c.fetchone()
        conn.commit()
        c.close()
        return data
    
    def insert(self, task):
        conn = self.__connect()
        c = conn.cursor()
        c.execute("INSERT INTO todo (task, status) VALUES (?,?)", (task, 1))
        conn.commit()
        c.close()
        return True
    
    def update(self, no, task, status):
        conn = self.__connect()
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (task, status, no))
        self.conn.commit()
        c.close()
        return True