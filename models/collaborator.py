import sqlite3

class Collaborator:
    def __init__(self, collaborator_id=None, name="", role=""):
        self.collaborator_id = collaborator_id
        self.name = name
        self.role = role
        self.tablename = "collaborators"

    def save(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if self.collaborator_id:
            cursor.execute("UPDATE collaborators SET name = ?, role = ? WHERE collaborator_id = ?", 
                           (self.name, self.role, self.collaborator_id))
        else:
            cursor.execute("INSERT INTO collaborators (name, role) VALUES (?, ?)", 
                           (self.name, self.role))
            self.collaborator_id = cursor.lastrowid
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM collaborators WHERE collaborator_id = ?", 
                       (self.collaborator_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collaborators")
        rows = cursor.fetchall()
        conn.close()
        return [Collaborator(*row) for row in rows]

    @staticmethod
    def get_by_id(collaborator_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collaborators WHERE collaborator_id = ?", 
                       (collaborator_id,))
        row = cursor.fetchone()
        conn.close()
        return Collaborator(*row) if row else None
    
    @staticmethod
    def get_by_name(name):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collaborators WHERE name = ?", 
                       (name,))
        row = cursor.fetchone()
        conn.close()
        return Collaborator(*row) if row else None