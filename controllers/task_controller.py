from models.task import Task

class TaskController:
    @staticmethod
    def create_task(name, description, project_id, collaborator_id):
        print(name, description, project_id, collaborator_id)
        task = Task(name=name, description=description, project_id=project_id, collaborator_id=collaborator_id)
        task.save()

    @staticmethod
    def delete_task(task_id):
        task = Task.get_by_id(task_id)
        if task:
            task.delete()

    @staticmethod
    def get_all_tasks():
        return Task.get_all()

    @staticmethod
    def get_task_by_id(task_id):
        return Task.get_by_id(task_id)

    @staticmethod
    def get_task_by_name(name):
        tasks = Task.get_all()
        for task in tasks:
            if task.name == name:
                return task
        return None
