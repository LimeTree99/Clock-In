
class Event:
    def __init__(self, start):
        self.start = start
        self.end = None 
        

class Task:
    def __init__(self, name: str):
        self.name = name
        self.events = []
        
    def add_event(self, event):
        self.event.append(event)


class Tasks:
    """
    Container for tasks 
    """
    def __init__(self, tasks: list=[]):
        self.tasks = tasks
        
    def add(self, task_name: str):
        self.tasks.append(Task(task_name))
        
    def load_file(self, filename: str):
        pass
    
    def save_file(self, filename: str):
        pass