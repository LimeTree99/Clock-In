import curses
import time
from datetime import timedelta

from clockin.core.keys import Keys
from clockin.core.task import Tasks
from clockin.core.util import Event_loop

from clockin.gui import Color

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
    def __init__(self, 
                 width: int,  
                 height: int, 
                 vec: tuple[int, int], 
                 options: list, 
                 funcs: list, 
                 **kargs: dict):
        
        self.mask_options = []
        super().__init__(width, height, vec, **kargs)
        self.options = options
        self.funcs = funcs
        self.selected = None
        
        
        self.active = False
        
        self.key = Keys(self._pad)
        
    def update(self, keys: Keys):
        if self.active:
            key = keys.checkkey()
            if self.selected == None:
                self.selected = 0
                
            if key == curses.KEY_UP:
                self.prev()
                keys.usekey()
            elif key == curses.KEY_DOWN:
                self.next()
                keys.usekey()
            elif key == Keys.KEY_ENTER or key == Keys.KEY_PADENTER or key == curses.KEY_ENTER:
                # the above elif hopefully checks for enter on most systems
                self.press()
                keys.usekey()
            elif key == -1:
                pass
            else:
                pass
        
            
        
        self._pad.clear()
        for i in range(len(self.options)):
            if i == self.selected:
                self.addstr(f"{self.options[i]}\n", (0, i), curses.A_UNDERLINE)
            else:
                self.addstr(f"{self.options[i]}\n")
        
        self.draw()
        
    def next(self):
        self.selected += 1
        
        while self.selected in self.mask_options:
            self.selected += 1
            if self.selected >= len(self.options):
                self.selected = 0
        
        
        if self.selected >= len(self.options):
            self.selected = 0
    
    def prev(self):
        self.selected -= 1
        while self.selected in self.mask_options:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.options) - 1
        
        if self.selected < 0:
            self.selected = len(self.options) - 1
        
    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False
        
    def press(self):
        "Run the function associated with the selected option"
        self.funcs[self.selected]()

class Task_menu(List_menu):
    def __init__(self, 
                 width: int,  
                 height: int, 
                 tasks: Tasks,
                 vec: tuple[int, int],
                 **kargs: dict):
        self.tasks = tasks
        funcs = [lambda name=name: self.select_task(name) for name in self.tasks.get_names()]
        
        funcs = funcs + [lambda: "hold", self.add_task, self.delete_task]
        super().__init__(width, height, vec, 
                         options=self.tasks.get_names() + ["", "Add Task", "Delete Task"], 
                         funcs=funcs, **kargs)
        
        self.mask_options = [len(self.options) - 3]
        
    def add_task(self):
        pass
    
    def delete_task(self):
        pass
        
        
    def select_task(self, name):
        self.tasks.set_selected(name)
        
        


class Timer(Pad):
    def __init__(self, width: int, height: int, vec, tasks: Tasks, **kargs: dict):
        super().__init__(width, height, vec, **kargs)
        self.tasks = tasks
        self.active = False
        self.timestart = None
        self.timeend = None
        self.timing = False
        self.attr = curses.A_NORMAL
        
        self.events = Event_loop()
                
    def start(self):
        self.timestart = time.time()
        self.flash(Color.GREEN, 0.5)
        self.timing = True
        
    def stop(self):
        self.timeend = time.time()
        self.flash(Color.RED, 0.5)
        self.timing = False
    
    def update(self, keys: Keys):
        if keys.checkkey() == Keys.KEY_SPACE and self.tasks.get_selected() != None:
            keys.usekey()
            if self.timing:
                self.stop()
            else:
                self.start()
                
        self.events.run()
        
    def flash(self, color, duration: float):
        self.attr = color
        self.events.new(func=lambda: self.set_attr(curses.A_NORMAL), delay=duration, repeat=1)
        
    def set_attr(self, attr):
        self.attr = attr
    
    def gettime(self):
        timestr = ""
        if self.timestart == None:
            timestr = "0:00:00"
        else:
            if self.timing:
                self.timeend = time.time()
                timestr = str(timedelta(seconds=int(self.timeend - self.timestart)))
            else:
                timestr = str(timedelta(seconds=int(self.timeend - self.timestart)))
        
        return timestr
    
    def draw(self):
        self._pad.clear()
        if self.tasks.get_selected() == None:
            task = "Select a task"
        else: 
            task = self.tasks.get_selected().name
            
        self.addstr(f"{task} | {self.gettime()}", attr=self.attr)
        return super().draw()
