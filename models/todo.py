import sqlite3
class Todo:
    def __init__(self, database):
        self.database = database
    
    def __connect(self):
        conn = sqlite3.connect(self.database)
        self.conn = conn
        c = conn.cursor()
        return c

    
    def tasks(self):
        c = self.__connect()
        c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
        data = c.fetchall()
        c.close()
        return data
    
    def task(self, id):
        c = self.__connect()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (id,))
        data = c.fetchone()
        c.close()
        return data
    
    def new_todo(self, task):
        c = self.__connect()
        c.execute("INSERT INTO todo (task, status) VALUES (?,?)", (task, 1))
        self.conn.commit()
        c.close()
        return True
    
    def edit_todo(self, no, task, status):
        c = self.__connect()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (task, status, no))
        self.conn.commit()
        c.close()
        return True