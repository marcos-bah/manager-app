import sqlite3

from models.collaborator import Collaborator

class Task:
    def __init__(self, task_id=None, project_id=None, name="", description="", status="", collaborators=None):
        self.task_id = task_id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.status = status
        self.collaborators = collaborators if collaborators else []
        self.tablename = "tasks"

    def save(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if self.task_id:
            cursor.execute("UPDATE tasks SET project_id = ?, name = ?, description = ?, status = ? WHERE task_id = ?", 
                           (self.project_id, self.name, self.description, self.status, self.task_id))
        else:
            cursor.execute("INSERT INTO tasks (project_id, name, description, status) VALUES (?, ?, ?, ?)", 
                           (self.project_id, self.name, self.description, self.status))
            self.task_id = cursor.lastrowid

        # Save or update collaborators
        for collaborator in self.collaborators:
            cursor.execute("INSERT OR IGNORE INTO task_collaborators (task_id, collaborator_id) VALUES (?, ?)", 
                           (self.task_id, collaborator.collaborator_id))
        
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE task_id = ?", 
                       (self.task_id,))
        cursor.execute("DELETE FROM task_collaborators WHERE task_id = ?", 
                       (self.task_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_by_project(project_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE project_id = ?", 
                       (project_id,))
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            task = Task(*row)
            task.collaborators = Task.get_collaborators_for_task(task.task_id)
            tasks.append(task)
        conn.close()
        return tasks

    @staticmethod
    def get_by_id(task_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE task_id = ?", 
                       (task_id,))
        row = cursor.fetchone()
        if row:
            task = Task(*row)
            task.collaborators = Task.get_collaborators_for_task(task.task_id)
            conn.close()
            return task
        conn.close()
        return None

    @staticmethod
    def get_collaborators_for_task(task_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT c.* FROM collaborators c JOIN task_collaborators tc ON c.collaborator_id = tc.collaborator_id WHERE tc.task_id = ?", 
                       (task_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Collaborator(*row) for row in rows]
    
    @staticmethod
    def get_all():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        conn.close()
        return [Task(*row) for row in rows]