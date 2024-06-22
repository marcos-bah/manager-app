import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from controllers.collaborator_controller import CollaboratorController
from models.collaborator import Collaborator

class CollaboratorFormAppView:
    def __init__(self, root, collaborator_id=None):
        self.root = root
        self.collaborator_id = collaborator_id
        self.root.geometry("400x220")
        self.root.title("Manage Collaborators")
        self.classmodel = Collaborator()
        
        # Create and position UI elements
        self.create_widgets()

        # If an ID is provided, load collaborator data
        if self.collaborator_id:
            self.load_collaborator_data()

    def create_widgets(self):
        """Create and position widgets in the main window."""
        # Labels
        tk.Label(self.root, text="Name:").grid(row=0, column=0, sticky="e")
        tk.Label(self.root, text="Role:").grid(row=1, column=0, sticky="e")

        # Entry fields
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        # role é um select com opções sendo: "Developer", "Designer", "Tester", "Manager"
        self.role_combobox = ttk.Combobox(self.root, state="readonly")  # state="readonly" para evitar entrada de texto
        self.role_combobox['values'] = ("Developer", "Designer", "Tester", "Manager")
        self.role_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.role_combobox.current(0)  # Opcional: definir o valor padrão como o primeiro da lista

        

        # Buttons
        if self.collaborator_id:
            self.save_button = tk.Button(self.root, text="Save Changes", command=self.update_collaborator)
        else:
            self.save_button = tk.Button(self.root, text="Create Collaborator", command=self.create_collaborator)
        self.save_button.grid(row=2, column=1, padx=10, pady=10)

    def create_collaborator(self):
        """Create a new collaborator."""
        name = self.name_entry.get()
        role = self.role_combobox.get()
        if name and role:
            CollaboratorController.create_collaborator(name, role)
            messagebox.showinfo("Success", "Collaborator created successfully!")
            self.root.destroy()
        else:
            messagebox.showwarning("Input error", "Please provide both name and role.")

    def load_collaborator_data(self):
        """Load existing collaborator data for editing."""
        collaborator = CollaboratorController.get_collaborator_by_id(self.collaborator_id)
        if collaborator:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, collaborator.name)
            self.role_combobox.set(collaborator.role)
        else:
            messagebox.showerror("Error", "Collaborator not found.")
            self.root.destroy()

    def update_collaborator(self):
        """Update an existing collaborator."""
        new_name = self.name_entry.get()
        new_role = self.role_combobox.get()
        if new_name and new_role:
            CollaboratorController.update_collaborator(self.collaborator_id, new_name, new_role)
            messagebox.showinfo("Success", "Collaborator updated successfully!")
            self.root.destroy()
        else:
            messagebox.showwarning("Input error", "Please provide both name and role.")
            self.root.destroy()

