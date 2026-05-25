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
        self._buff = ""
        if self.bd:
            # lower right corner "quirk"              \/  sould be 2
            self._bd_pad = curses.newpad(self.height + 2, self.width + 2) 
            self._create_bd()
            
    def _create_bd(self):
        self._bd_pad.addstr("┌" + "─" * self.width + "┐")
        for i in range(self.height):
            self._bd_pad.addch(i+1, 0, "│")
            self._bd_pad.addch(i+1, self.width+1, "│")
        self._bd_pad.addstr(self.height + 1, 0, "└" + "─" * self.width)
        
        # rediculus workaround to the lower right corner "quirk"
        try:
            self._bd_pad.addch("┘")
        except curses.error as e:
            if "returned ERR" in str(e): # Common message for the quirk
                pass
            else:
                raise
        
        
    def attron(self, attr: int):
        self._pad.attron(attr)
        
    def attroff(self, attr: int):
        self._pad.attroff(attr)
        
    def addstr(self, string: str, vec: tuple[int, int]=None, attr: int=curses.A_NORMAL):
        """
        Add string to Pad, automatically truncates out of bounds strings

        Parameters
        ----------
        str: str
            The string to be added to the pad
        vec: [x,y]
            location for string to begin
        attr: int
            curses attributes  
        """
        if vec == None:
            y, x = self._pad.getyx()
        else:
            x, y = vec
        
        # truncate strings that go out of bounds
        space = self.width * self.height - (y * self.width) + x
        if len(string) > space:
            string = string[:space]
            
        
        # once again that rediculus workaround for the "quirk"
        try:
            self._pad.addstr(y, x, string, attr)
        except curses.error as e:
            if "returned ERR" in str(e): # Common message for the quirk
                pass
            else:
                raise
        
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
