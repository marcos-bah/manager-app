import tkinter as tk
from tkinter import ttk, messagebox
from controllers.team_controller import TeamController
from controllers.project_controller import ProjectController
from controllers.collaborator_controller import CollaboratorController
from models.team import Team
from models.collaborator import Collaborator


class TeamFormAppView:
    def __init__(self, root, team_id=None):
        self.root = root
        self.team_id = team_id
        self.root.geometry("600x400")
        self.root.title("Manage Teams")
        self.classmodel = Team()

        # Create and position UI elements
        self.create_widgets()

        # If an ID is provided, load team data
        if self.team_id:
            self.load_team_data()

    def create_widgets(self):
        """Create and position widgets in the main window."""
        # Labels
        tk.Label(self.root, text="Name:").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        tk.Label(self.root, text="Project:").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        tk.Label(self.root, text="Collaborators:").grid(row=2, column=0, sticky="e", padx=10, pady=10)

        # Entry fields
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Combobox for projects
        self.projects_combobox = ttk.Combobox(self.root, state="readonly", postcommand=self.update_projects)
        self.projects_combobox.grid(row=1, column=1, padx=10, pady=10)

        # Listbox for collaborators
        self.collaborators_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=40, height=4)
        self.collaborators_listbox.grid(row=2, column=1, padx=10, pady=10)
        self.update_collaborators()

        # Buttons
        if self.team_id:
            self.save_button = tk.Button(self.root, text="Save Changes", command=self.update_team)
        else:
            self.save_button = tk.Button(self.root, text="Create Team", command=self.create_team)
        self.save_button.grid(row=3, column=1, padx=10, pady=10)

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

    def create_team(self):
        """Create a new team."""
        name = self.name_entry.get()
        selected_project_name = self.projects_combobox.get()
        selected_project = ProjectController.get_project_by_name(selected_project_name)
        selected_collaborators = [self.collaborators_listbox.get(idx) for idx in self.collaborators_listbox.curselection()]
        selected_collaborator_ids = [CollaboratorController.get_collaborator_by_name(collab_name).collaborator_id for collab_name in selected_collaborators]

        if name and selected_project and selected_collaborator_ids:
            team = Team(name=name, project_id=selected_project.project_id,
                        collaborators=[Collaborator(collaborator_id=id) for id in selected_collaborator_ids])
            team.save()
            messagebox.showinfo("Success", "Team created successfully!")
            self.root.destroy()
        else:
            messagebox.showwarning("Input error", "Please provide name, select a project and at least one collaborator.")

    def load_team_data(self):
        """Load existing team data for editing."""
        team = TeamController.get_team_by_id(self.team_id)
        if team:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, team.name)

            project = ProjectController.get_project_by_id(team.project_id)
            self.projects_combobox.set(project.name)

            for collaborator in team.collaborators:
                self.collaborators_listbox.select_set(collaborator.collaborator_id - 1)

        else:
            messagebox.showerror("Error", "Team not found.")
            self.root.destroy()

    def update_team(self):
        """Update an existing team."""
        new_name = self.name_entry.get()
        selected_project_name = self.projects_combobox.get()
        selected_project = ProjectController.get_project_by_name(selected_project_name)
        selected_collaborators = [self.collaborators_listbox.get(idx) for idx in self.collaborators_listbox.curselection()]
        selected_collaborator_ids = [CollaboratorController.get_collaborator_by_name(collab_name).collaborator_id for collab_name in selected_collaborators]

        if new_name and selected_project and selected_collaborator_ids:
            team = Team(team_id=self.team_id, name=new_name,
                        project_id=selected_project.project_id, collaborators=[Collaborator(collaborator_id=id) for id in selected_collaborator_ids])
            team.save()
            messagebox.showinfo("Success", "Team updated successfully!")
            self.root.destroy()
        else:
            messagebox.showwarning("Input error", "Please provide name, select a project and at least one collaborator.")
