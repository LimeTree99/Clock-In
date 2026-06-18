
class Event:
    def __init__(self, start: float):
        self.start = start
        self.end = None 
        

class Task:
    def __init__(self, name: str):
        self.name = name
        self.events = []
        
    def start(self, time: float):
        self.events.append(Event(time))
        
    def end(self, time: float):
        self.events[-1].end = time


class Tasks:
    """
    Container for tasks 
    """
    def __init__(self, tasks: list=[]):
        self.tasks = tasks
        self.selected = None
        
    def add(self, task_name: str):
        self.tasks.append(Task(task_name))
        
    def pop(self, task_name: str) -> Task:
        task = None
        n = 0
        while task == None and n < len(self.tasks):
            if task_name == self.tasks[n].name:
                task = self.tasks.pop(n)
            else:
                n += 1
                
        return task
        
    def get_names(self):
        names = []
        for task in self.tasks:
            names.append(task.name)
        return names
        
    def set_selected(self, name) -> bool:
        found = False
        self.selected = 0
        while not found and self.selected < len(self.tasks):
            if name == self.tasks[self.selected].name:
                found = True
            else:
                self.selected += 1
                
        return found            
        
    def get_selected(self) -> None | Task:
        if self.selected == None:
            return None
        else:
            return self.tasks[self.selected]
        
    def load_file(self, filename: str):
        pass
    
    def save_file(self, filename: str):
        pass