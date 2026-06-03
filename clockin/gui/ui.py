import curses
import time
from datetime import timedelta
from clockin.core.keys import Keys

class Pad_defalts:
    def __init__(self):
        self.bd = False
        self.title = None



class Pad(Pad_defalts):
    def __init__(self, width: int, height: int, vec: tuple[int, int], **kargs: dict):
        super().__init__()
        self.height = height
        self.width = width
        self.vec = vec
        
        self.__dict__ = self.__dict__ | kargs
        
        self._pad = curses.newpad(self.height, self.width)
        
        self._bd_pad = curses.newpad(self.height + 2, self.width + 2) 
        self._create_bd()
            
    def _create_bd(self):
        if self.bd:
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
        if self.title != None:
            self._bd_pad.addstr(0, 1, self.title)
        
        
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
        if self.bd or self.title != None:
            self._bd_pad.noutrefresh(0,0, 
                                 self.vec[1] - 1, 
                                 self.vec[0] - 1, 
                                 self.vec[1] + self.height + 1, 
                                 self.vec[0] + self.width + 1)
        self._pad.noutrefresh(0,0, 
                          self.vec[1], 
                          self.vec[0], 
                          self.vec[1] + self.height, 
                          self.vec[0] + self.width)
        
    
    
class List_menu(Pad):
    def __init__(self, width: int,  height: int, vec, items: list, **kargs: dict):
        super().__init__(width, height, vec, **kargs)
        self.items = items
        self.selected = None
        
        self.active = False
        
        self.key = Keys(self._pad)
        
    def update(self, keys: Keys):
        if self.active:
            key = keys.usekey()
            if self.selected == None:
                self.selected = 0
                
            if key == "KEY_UP":
                self.prev()
            elif key == "KEY_DOWN":
                self.next()
            elif self.key == "KEY_ENTER":
                pass
        
            
        
        self._pad.clear()
        for i in range(len(self.items)):
            if i == self.selected:
                self.addstr(f"{self.items[i]}\n", (0, i), curses.A_UNDERLINE)
            else:
                self.addstr(f"{self.items[i]}\n")
        self.addstr(f"{self.key.last}\n")
        self.draw()
        
    def next(self):
        self.selected += 1
        if self.selected >= len(self.items):
            self.selected = 0
    
    def prev(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.items) - 1
        
    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False
    
    
class Timer(Pad):
    def __init__(self, width: int, height: int, vec, **kargs: dict):
        super().__init__(width, height, vec, **kargs)
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
