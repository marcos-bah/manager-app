from models.project import Project
    
class ProjectController:
    @staticmethod
    def create_project(name, description, tasks):
        if tasks:
            project = Project(name=name, description=description, tasks=tasks)
        else:
            project = Project(name=name, description=description)
        project.save()

    @staticmethod
    def get_project_by_id(project_id):
        return Project.get_by_id(project_id)

    @staticmethod
    def update_project(project_id, name, description, tasks):
        project = Project.get_by_id(project_id)
        if project:
            project.name = name
            project.description = description
            project.tasks = tasks
            project.save()

    @staticmethod
    def get_all_projects():
        return Project.get_all()
    
    @staticmethod
    def delete_project(project_id):
        project = Project.get_by_id(project_id)
        if project:
            project.delete()
            
    @staticmethod
    def get_project_by_name(name):
        return Project.get_by_name(name)

