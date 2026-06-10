import time


class Delay:
    def __init__(self):
        self.start = time.time()
        
    def delay(self, seconds: float):
        """
        Run a busy loop until the seconds elapsed from the last call is reached.
        
        Returns
        -------
        (bool): True if time was delayed, False if there was delay exicuted
        """
        delayed = False
        while time.time() - self.start < seconds:
            delayed = True
            
        self.start = time.time()            
        return delayed
    
class Event_loop:
    "run functions with a delay, order is not preserved"
    def __init__(self):
        self.start = time.time()
        self.events = []
    
    def new(self, func, delay: float, repeat: float=float('inf'), run_immediate: bool=False):
        "create a new event that will run"
        self.events.append(self.Event(func, delay, repeat, run_immediate))
        
    def delete(self) -> bool:
        """
        delete an event from the event loop 
        
        returns:
        --------
        True if succesfull false if not found
        """
    
    def run(self):
        i = 0
        while i < len(self.events):
            event = self.events[i]
            if event.run_immediate:
                event.func()
                event.last_run = time.time()
                event.run_immediate = False
            elif event.last_run + event.delay < time.time():
                event.func()
                event.last_run = time.time()
                event.repeat -= 1
                if event.repeat <= 0:
                    self.events.pop(i)
            i += 1
                    
    class Event:
        def __init__(self, func, delay: float, repeat: float, run_immediate: bool):
            self.func = func
            self.delay = delay 
            self.repeat = repeat
            self.run_immediate = run_immediate
            self.last_run = time.time()