import tkinter as tk
from tkinter import ttk
import sqlite3

from models.collaborator import Collaborator
from models.project import Project
from models.task import Task
from models.team import Team
from views.collaborator_view import CollaboratorFormAppView
from views.project_view import ProjectFormAppView
from views.task_view import TaskFormAppView
from views.team_view import TeamFormAppView 

class ManagerTableApp:
    def __init__(self, model):
        self.model = model
        self.table_name = model.tablename
        self.columns = []

        # Initialize the main window
        self.window = tk.Tk()
        self.window.title(f"{self.table_name.capitalize()} Table")
        self.window.geometry("600x400")

        # Configure table style
        self.configure_styles()

        # Create UI elements
        self.create_widgets()

        # Read columns and data from the database
        self.columns = self.read_columns()
        data = self.get_data()

        # Generate the table with the retrieved data
        self.generate_table(data)

        # Run the main loop
        self.window.mainloop()

    def connect_database(self):
        """Connect to the SQLite3 database."""
        try:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            return connection, cursor
        except Exception as e:
            print(f"Connection error: {e}")
            return None, None

    def read_columns(self):
        """Read columns from the specified table."""
        connection, cursor = self.connect_database()
        if not connection:
            return []

        cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = cursor.fetchall()
        print(rows)
        columns = [desc[0] for desc in cursor.description]
        columns.append("Edit")
        columns.append("Delete")
        connection.close()
        return columns

    def get_data(self):
        """Get data from the specified table."""
        connection, cursor = self.connect_database()
        if not connection:
            return []

        cursor.execute(f"SELECT * FROM {self.table_name}")
        data = cursor.fetchall()
        connection.close()
        return data

    def generate_table(self, data):
        """Generate the table UI with the retrieved data."""
        self.table_ui.configure(columns=self.columns)
        
        self.table_ui.column('#0', width=0, stretch='no')

        # Define the column headings
        for i, column in enumerate(self.columns):
            self.table_ui.heading(column, text=column.capitalize())
            self.table_ui.column(column, anchor='center', width=100)

        # Clear existing data from the table
        self.table_ui.delete(*self.table_ui.get_children())

        # Insert new data
        for row in data:
            self.table_ui.insert('', 'end', values=(*row, 'Edit', 'Delete'))
            
        self.window.after(1500, self.update_table)
            
    def update_table(self):
        """Update the table with new data."""
        print("refreshing...")
        data = self.get_data()
        self.generate_table(data)
            
    def create_new(self):
        """Create a new model"""
        root = tk.Tk()
        match self.table_name:
            case "collaborators":
                app = CollaboratorFormAppView(root, collaborator_id=None)
                root.mainloop()
            case "projects":
                app = ProjectFormAppView(root, project_id=None)
                root.mainloop()
            case "tasks":
                app = TaskFormAppView(root, task_id=None)
                root.mainloop()
            case "teams":
                app = TeamFormAppView(root, team_id=None)
                root.mainloop()
            
    def edit_model(self, data):
        """Edit a model."""
        if not data:
            return
        root = tk.Tk()
        match self.table_name:
            case "collaborators":
                app = CollaboratorFormAppView(root, collaborator_id=data[0])
                root.mainloop()
            case "projects":
                app = ProjectFormAppView(root, project_id=data[0])
                root.mainloop()
            case "tasks":
                app = TaskFormAppView(root, task_id=data[0])
                root.mainloop()
            case "teams":
                app = TeamFormAppView(root, team_id=data[0])
                root.mainloop()

    def delete_model(self, data):
        """Delete a model"""
        if not data:
            return
        match self.table_name:
            case "collaborators":
                self.model.collaborator_id = data[0]
                self.model.delete()
                self.update_table()
            case "projects":
                self.model.project_id = data[0]
                self.model.delete()
                self.update_table()
            case "tasks":
                self.model.task_id = data[0]
                self.model.delete()
                self.update_table()
            case "teams":
                self.model.team_id = data[0]
                self.model.delete()
                self.update_table()

    def on_item_click(self, event):
        """Handle item click events in the table."""
        item = self.table_ui.identify('item', event.x, event.y)
        column = self.table_ui.identify_column(event.x)
        column_index = int(column.strip('#'))
        
        if column_index == len(self.columns) - 1:
            print(f"Edit clicked for item {self.table_ui.item(item, 'values')}")
            self.edit_model(self.table_ui.item(item, 'values'))
        elif column_index == len(self.columns):
            print(f"Delete clicked for item {self.table_ui.item(item, 'values')}")
            self.delete_model(self.table_ui.item(item, 'values'))

    def configure_styles(self):
        """Configure styles for the table."""
        table_style = ttk.Style()
        table_style.configure("Treeview.Row", background="#f0f0f0", padding=3)
        table_style.configure("Treeview.Heading", background="#d9d9d9")

    def create_widgets(self):
        """Create and position widgets in the main window."""
        # Frames
        title_frame = tk.Frame(self.window)
        table_frame = tk.Frame(self.window)
        button_frame = tk.Frame(self.window)

        # Title label
        title_label = tk.Label(title_frame, text=f"{self.table_name.capitalize()} Table", font=("Arial", 16))

        # Scrollbar for the table
        scrollbar = tk.Scrollbar(table_frame)

        # Table UI
        self.table_ui = ttk.Treeview(table_frame, yscrollcommand=scrollbar.set)
        self.table_ui.bind('<ButtonRelease-1>', self.on_item_click)
        scrollbar.config(command=self.table_ui.yview)

        # Create New button
        create_button = tk.Button(button_frame, text="Create New", command=self.create_new)

        # Positioning widgets
        title_frame.pack(fill=tk.X)
        title_label.pack(pady=10)

        table_frame.pack(fill=tk.BOTH, expand=True)
        self.table_ui.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        button_frame.pack(fill=tk.X, pady=10)
        create_button.pack(side=tk.LEFT, padx=10)

# Create an instance of the CollaboratorTableApp class with the specified table name
collaborator = Collaborator()
project = Project()
task = Task()
team = Team()

models = [collaborator, project, task, team]

#criar uma mini interface grafica para escolher qual tabela deseja visualizar
root = tk.Tk()
root.title("Choose a table")
root.geometry("200x200")

def on_button_click(model):
    app = ManagerTableApp(model)
    root.destroy()

for model in models:
    button = tk.Button(root, text=model.tablename, command=lambda model=model: on_button_click(model))
    button.pack(pady=5)
    
root.mainloop()
