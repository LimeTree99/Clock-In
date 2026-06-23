import csv


class Event:
    def __init__(self, start: float, end: float=None):
        self.start = start
        self.end = end 
        

class Task:
    def __init__(self, name: str):
        self.name = name
        self.events = []
        
    def start(self, time: float):
        self.events.append(Event(time))
        
    def end(self, time: float):
        self.events[-1].end = time
        
    def add_event(self, start: float, end: float):
        self.events.append(Event(start, end))


class Tasks:
    """
    Container for tasks 
    """
    def __init__(self, tasks: list=[]):
        self.tasks = {}
        self.task_names = []
        for task in tasks:
            self.tasks[task.name] = task
            self.task_names.append(task.name)
        self.selected = None
        
    def add(self, task_name: str):
        self.tasks[task_name] = Task(task_name)
        self.task_names.append(task_name)
        
    def pop(self, task_name: str) -> Task:
        self.task_names.remove(task_name)
        return self.tasks.pop(task_name)
    
    def get_names(self):
        return self.task_names
        
    def set_selected(self, task_name: str) -> bool:
        found = False
        self.selected = 0
        while not found and self.selected < len(self.task_names):
            if task_name == self.task_names[self.selected]:
                found = True
            else:
                self.selected += 1
                
        return found            
        
    def get_selected(self) -> None | Task:
        if self.selected == None:
            return None
        else:
            return self.tasks[self.task_names[self.selected]]
        
    def event(self, start: float, end: float):
        self.tasks[self.task_names[self.selected]].add_event(start, end)
        
    def load_file(self, filename: str):
        with open(filename, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)  
            for row in csvreader:
                if row['task'] not in self.tasks:
                    self.add(row['task'])
                self.tasks[row['task']].add_event(row['start'], row['end'])
                
                    
                

            
    
    def save_file(self, filename: str):
        pass