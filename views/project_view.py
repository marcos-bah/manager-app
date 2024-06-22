import tkinter as tk
from tkinter import ttk, messagebox
from controllers.collaborator_controller import CollaboratorController
from controllers.project_controller import ProjectController
from controllers.task_controller import TaskController
from models.project import Project
from models.task import Task

class ProjectFormAppView:
    def __init__(self, root, project_id=None):
        self.root = root
        self.project_id = project_id
        self.root.geometry("600x400")
        self.root.title("Manage Projects")
        self.classmodel = Project()

        # Create and position UI elements
        self.create_widgets()

        # If an ID is provided, load project data
        if self.project_id:
            self.load_project_data()

    def create_widgets(self):
        """Create and position widgets in the main window."""
        # Labels
        tk.Label(self.root, text="Name:").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        tk.Label(self.root, text="Description:").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        tk.Label(self.root, text="Tasks:").grid(row=2, column=0, sticky="e", padx=10, pady=10)

        # Entry fields
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=1, column=1, padx=10, pady=10)

        # Combobox for tasks
        self.tasks_combobox = ttk.Combobox(self.root, state="readonly", postcommand=self.update_tasks)
        self.tasks_combobox.grid(row=2, column=1, padx=10, pady=10)

        # Buttons
        if self.project_id:
            self.save_button = tk.Button(self.root, text="Save Changes", command=self.update_project)
        else:
            self.save_button = tk.Button(self.root, text="Create Project", command=self.create_project)
        self.save_button.grid(row=3, column=1, padx=10, pady=10)

    def update_tasks(self):
        """Update the tasks combobox with the list of tasks."""
        tasks = TaskController.get_all_tasks()
        task_names = [task.name for task in tasks]
        self.tasks_combobox['values'] = task_names

    def create_project(self):
        """Create a new project."""
        name = self.name_entry.get()
        description = self.description_entry.get()
        selected_task_name = self.tasks_combobox.get()
        selected_task = TaskController.get_task_by_name(selected_task_name)
        
        if selected_task:
            selected_task = [selected_task]
        else:
            selected_task = []
        
        if name and description:
            ProjectController.create_project(name, description, selected_task)
            messagebox.showinfo("Success", "Project created successfully!")
            self.root.destroy()
        else:
            messagebox.showwarning("Input error", "Please provide name, description, and select a task.")

    def load_project_data(self):
        """Load existing project data for editing."""
        project = ProjectController.get_project_by_id(self.project_id)
        if project:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, project.name)
            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, project.description)
            
            if project.tasks:
                for task in project.tasks:
                    self.tasks_combobox.set(task.name)
                      
        else:
            messagebox.showerror("Error", "Project not found.")
            self.root.destroy()

    def update_project(self):
        """Update an existing project."""
        new_name = self.name_entry.get()
        new_description = self.description_entry.get()
        selected_task_name = self.tasks_combobox.get()
        selected_task = TaskController.get_task_by_name(selected_task_name)

        if new_name and new_description and selected_task:
            ProjectController.update_project(self.project_id, new_name, new_description, selected_task.task_id)
            messagebox.showinfo("Success", "Project updated successfully!")
            self.root.destroy()
        else:
            messagebox.showwarning("Input error", "Please provide name, description, and select a task.")

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectFormAppView(root)
    root.mainloop()
