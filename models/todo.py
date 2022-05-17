import sqlite3

class Todo:
    def __init__(self, database):
        self.database = database
    
    def __connect(self):
        conn = sqlite3.connect(self.database)
    
        return conn

    
    def select(self):
        data = None
        try:
            conn = self.__connect()
            c = conn.cursor()
            c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
            data = c.fetchall()
            conn.commit()
            c.close()
            
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        
        finally:
            if conn:
                conn.close()
            return data
    
    def get_task(self, no):
        data = None
        try:
            conn = self.__connect()
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
    
    def insert_task(self, task):
        try:
            conn = self.__connect()
            c = conn.cursor()
            c.execute("INSERT INTO todo (task, status) VALUES (?,?)", (task, 1))
            conn.commit()
            c.close()
        
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        
        finally:
            if conn:
                conn.close()    
            return True
    
    def update(self, no, task, status):
        try:
            conn = self.__connect()
            c = conn.cursor()
            c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (task, status, no))
            conn.commit()
            c.close()
        
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        
        finally:
            if conn:
                conn.close()
            return True

    def delete(self, no):
        try:
            conn = self.__connect()
            c = conn.cursor()
            c.execute("DELETE FROM todo WHERE id LIKE ?", str(no))
            conn.commit()
            c.close()
            
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        
        finally:
            if conn:
                conn.close()
            return True