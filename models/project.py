import sqlite3

from models.task import Task

class Project:
    def __init__(self, project_id=None, name="", description="", tasks=None):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.tasks = tasks if tasks else []
        self.tablename = "projects"

    def save(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if self.project_id:
            cursor.execute("UPDATE projects SET name = ?, description = ? WHERE project_id = ?", 
                           (self.name, self.description, self.project_id))
        else:
            cursor.execute("INSERT INTO projects (name, description) VALUES (?, ?)", 
                           (self.name, self.description))
            self.project_id = cursor.lastrowid
        
        # Save or update tasks
        for task in self.tasks:
            task.project_id = self.project_id
            task.save()

        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE project_id = ?", 
                       (self.project_id,))
        cursor.execute("DELETE FROM tasks WHERE project_id = ?", 
                       (self.project_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects")
        rows = cursor.fetchall()
        projects = []
        for row in rows:
            project = Project(*row)
            project.tasks = Task.get_all_by_project(project.project_id)
            projects.append(project)
        conn.close()
        return projects

    @staticmethod
    def get_by_id(project_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE project_id = ?", 
                       (project_id,))
        row = cursor.fetchone()
        if row:
            project = Project(*row)
            project.tasks = Task.get_all_by_project(project.project_id)
            conn.close()
            return project
        conn.close()
        return None
    
    @staticmethod
    def get_by_name(name):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE name = ?", 
                       (name,))
        row = cursor.fetchone()
        if row:
            project = Project(*row)
            project.tasks = Task.get_all_by_project(project.project_id)
            conn.close()
            return project
        conn.close()
        return None
