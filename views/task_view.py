import tkinter as tk
from tkinter import ttk, messagebox
from controllers.task_controller import TaskController
from controllers.project_controller import ProjectController
from controllers.collaborator_controller import CollaboratorController
from models.task import Task
from models.project import Project
from models.collaborator import Collaborator

class TaskFormAppView:
    def __init__(self, root, task_id=None):
        self.root = root
        self.task_id = task_id
        self.root.geometry("600x400")
        self.root.title("Manage Tasks")
        self.classmodel = Task()

        # Create and position UI elements
        self.create_widgets()

        # If an ID is provided, load task data
        if self.task_id:
            self.load_task_data()

    def create_widgets(self):
        """Create and position widgets in the main window."""
        # Labels
        tk.Label(self.root, text="Name:").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        tk.Label(self.root, text="Description:").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        tk.Label(self.root, text="Project:").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        tk.Label(self.root, text="Collaborators:").grid(row=3, column=0, sticky="e", padx=10, pady=10)
        tk.Label(self.root, text="Status:").grid(row=4, column=0, sticky="e", padx=10, pady=10)

        # Entry fields
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=1, column=1, padx=10, pady=10)

        # Combobox for projects
        self.projects_combobox = ttk.Combobox(self.root, state="readonly", postcommand=self.update_projects)
        self.projects_combobox.grid(row=2, column=1, padx=10, pady=10)

        # Listbox for collaborators
        self.collaborators_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=40, height=4)
        self.collaborators_listbox.grid(row=3, column=1, padx=10, pady=10)
        self.update_collaborators()

        # Combobox for status
        self.status_combobox = ttk.Combobox(self.root, state="readonly")
        self.status_combobox['values'] = ("Not Started", "In Progress", "Completed")
        self.status_combobox.grid(row=4, column=1, padx=10, pady=10)
        self.status_combobox.current(0)  # Default status

        # Buttons
        if self.task_id:
            self.save_button = tk.Button(self.root, text="Save Changes", command=self.update_task)
        else:
            self.save_button = tk.Button(self.root, text="Create Task", command=self.create_task)
        self.save_button.grid(row=5, column=1, padx=10, pady=10)

    def update_projects(self):
        """Update the projects combobox with the list of projects."""
        projects = ProjectController.get_all_projects()
        project_names = [project.name for project in projects]
        self.projects_combobox['values'] = project_names

    def update_collaborators(self):
        """Update the collaborators listbox with the list of collaborators."""
        self.collaborators_listbox.delete(0, tk.END)
        collaborators = CollaboratorController.get_all_collaborators()
        for collaborator in collaborators:
            self.collaborators_listbox.insert(tk.END, collaborator.name)

    def create_task(self):
        """Create a new task."""
        name = self.name_entry.get()
        description = self.description_entry.get()
        selected_project_name = self.projects_combobox.get()
        selected_project = ProjectController.get_project_by_name(selected_project_name)
        selected_collaborators = [self.collaborators_listbox.get(idx) for idx in self.collaborators_listbox.curselection()]
        selected_collaborator_ids = [CollaboratorController.get_collaborator_by_name(collab_name).collaborator_id for collab_name in selected_collaborators]
        status = self.status_combobox.get()

        if name and description and selected_project and selected_collaborator_ids:
            task = Task(name=name, description=description, project_id=selected_project.project_id,
                        status=status, collaborators=[Collaborator(collaborator_id=id) for id in selected_collaborator_ids])
            task.save()
            messagebox.showinfo("Success", "Task created successfully!")
            self.root.destroy()
        else:
            messagebox.showwarning("Input error", "Please provide name, description, select a project and at least one collaborator.")

    def load_task_data(self):
        """Load existing task data for editing."""
        task = TaskController.get_task_by_id(self.task_id)
        if task:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, task.name)
            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, task.description)

            project = ProjectController.get_project_by_id(task.project_id)
            self.projects_combobox.set(project.name)

            for collaborator in task.collaborators:
                self.collaborators_listbox.select_set(collaborator.collaborator_id - 1)

            self.status_combobox.set(task.status)
        else:
            messagebox.showerror("Error", "Task not found.")
            self.root.destroy()

    def update_task(self):
        """Update an existing task."""
        new_name = self.name_entry.get()
        new_description = self.description_entry.get()
        selected_project_name = self.projects_combobox.get()
        selected_project = ProjectController.get_project_by_name(selected_project_name)
        selected_collaborators = [self.collaborators_listbox.get(idx) for idx in self.collaborators_listbox.curselection()]
        selected_collaborator_ids = [CollaboratorController.get_collaborator_by_name(collab_name).collaborator_id for collab_name in selected_collaborators]
        new_status = self.status_combobox.get()

        if new_name and new_description and selected_project and selected_collaborator_ids:
            task = Task(task_id=self.task_id, name=new_name, description=new_description,
                        project_id=selected_project.project_id, status=new_status, collaborators=[Collaborator(collaborator_id=id) for id in selected_collaborator_ids])
            task.save()
            messagebox.showinfo("Success", "Task updated successfully!")
            self.root.destroy()
        else:
            messagebox.showwarning("Input error", "Please provide name, description, select a project and at least one collaborator.")


