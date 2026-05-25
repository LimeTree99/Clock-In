import curses
import time
from datetime import timedelta


class Pad_defalts:
    def __init__(self):
        self.bd = False



class Pad(Pad_defalts):
    def __init__(self, width: int, height: int, vec: tuple[int, int], **kargs: dict):
        super().__init__()
        self.height = height
        self.width = width
        self.vec = vec
        
        self.__dict__ = self.__dict__ | kargs
        
        self._pad = curses.newpad(self.height, self.width)
        if self.bd:
            self._bd_pad = curses.newpad(self.height + 3, self.width + 2)
            self._create_bd()
            
    def _create_bd(self):
        self._bd_pad.addstr("┌" + "─" * self.width + "┐")
        for i in range(self.height):
            self._bd_pad.addch(i+1, 0, "│")
            self._bd_pad.addch(i+1, self.width+1, "│")
        self._bd_pad.addstr(self.height + 1, 0, "└" + "─" * self.width + "┘")
        
    def attron(self, attr: int):
        self._pad.attron(attr)
        
    def attroff(self, attr: int):
        self._pad.attroff(attr)
        
    def addstr(self, str: str, vec: tuple[int, int]=None, attr: int=None):
        """
        Add string to Pad

        Parameters
        ----------
        str: str
            The string to be added to the pad
        vec: [x,y]
            location for string to begin
        attr: int
            curses attributes  
        """
        assert len(str) <= self.height * self.width, "str too long for Pad"
        
        if attr == None and vec == None:
            self._pad.addstr(str)
        elif attr != None and vec == None:
            self._pad.addstr(str, attr)
        elif attr == None and vec != None:
            self._pad.addstr(vec[1], vec[0], str)
        else:
            self._pad.addstr(vec[1], vec[0], str, attr)
        
    def draw(self):
        if self.bd:
            self._bd_pad.refresh(0,0, 
                                 self.vec[1] - 1, 
                                 self.vec[0] - 1, 
                                 self.vec[1] + self.height + 1, 
                                 self.vec[0] + self.width + 1)
        self._pad.refresh(0,0, 
                          self.vec[1], 
                          self.vec[0], 
                          self.vec[1] + self.height, 
                          self.vec[0] + self.width)
        
    
    
class List_menu(Pad):
    def __init__(self, width: int,  height: int, vec, items: list):
        super().__init__(width, height, vec)
        self.items = items
        self.selected = None
        
    def update(self):
        self._pad.clear()
        for item in self.items:
            self.addstr(f"{item}\n")
        self.draw()
    
    
class Timer(Pad):
    def __init__(self, width: int, height: int, vec):
        super().__init__(width, height, vec)
        self.task = None
        self.active = False
        self.timestart = None
        
    def settask(self, task):
        self.task = task
        
    def start(self):
        self.timestart = time.time()
        
    def stop(self):
        pass
    
    def update(self):
        pass
    
    def gettime(self):
        timestr = ""
        if self.timestart == None:
            timestr = "00:00"
        else:
            timestr = str(timedelta(seconds=int(time.time()-self.timestart)))
        
        return timestr
    
    def draw(self):
        self._pad.clear()
        if self.task == None:
            task = "Select a task"
        else: 
            task = self.task
            
        self.addstr(f"{task} | {self.gettime()}")
        return super().draw()
