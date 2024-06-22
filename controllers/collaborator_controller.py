from models.collaborator import Collaborator

class CollaboratorController:
    @staticmethod
    def create_collaborator(name, role):
        collaborator = Collaborator(name=name, role=role)
        collaborator.save()

    @staticmethod
    def delete_collaborator(collaborator_id):
        collaborator = Collaborator.get_by_id(collaborator_id)
        if collaborator:
            collaborator.delete()
            
    @staticmethod
    def update_collaborator(collaborator_id, name, role):
        collaborator = Collaborator.get_by_id(collaborator_id)
        if collaborator:
            collaborator.name = name
            collaborator.role = role
            collaborator.update()

    @staticmethod
    def get_all_collaborators():
        return Collaborator.get_all()

    @staticmethod
    def get_collaborator_by_id(collaborator_id):
        return Collaborator.get_by_id(collaborator_id)
    
    @staticmethod
    def get_collaborator_by_name(name):
        return Collaborator.get_by_name(name)
