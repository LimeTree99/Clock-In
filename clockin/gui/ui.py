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
        
    def draw(self):
        pass
    
    def render(self):
        pass
    
    def update(self, keys: Keys):
        pass



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
        
    def clear(self):
        self._pad.clear()
        
    def resize(self, width, height, vec):
        self.width = max(width, 0)
        self.height = max(height, 0)
        self.vec = vec
        self._pad = curses.newpad(self.height, self.width)
        self._bd_pad = curses.newpad(self.height + 2, self.width + 2)
        self._create_bd()
        
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
        if self.width > 0 and self.height > 0:
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
        
class Log(Pad):
    "a Pad that you can add to continuously"
    def __init__(self, 
                 width: int,  
                 height: int, 
                 vec: tuple[int, int], 
                 **kargs: dict):
        super().__init__(width, height, vec, **kargs)   
        self._logs = [] 
        
    def log(self, string: str):
        self._logs.append(string)
        self.render()
        
    def render(self):
        self.clear()
        n = len(self._logs) - 1
        line = 0
        while n >= 0 and line < self.height:
            self.addstr(self._logs[n], [0,line])
            
            line += len(self._logs[n]) // self.width + 1
            
            # remember to truncate final line
            n -= 1
            
    def resize(self, width, height, vec):
        re = super().resize(width, height, vec)
        self.render()
        return re
        
    
class List_menu(Pad):
    def __init__(self, 
                 width: int,  
                 height: int, 
                 vec: tuple[int, int], 
                 options: list, 
                 funcs: list, 
                 start_active: bool=False,
                 mask_options: list=[],
                 **kargs: dict):
        
        self.mask_options = mask_options
        super().__init__(width, height, vec, **kargs)
        self.options = options
        self.funcs = funcs
        
        self.selected = 0
        if self.selected in self.mask_options:
            self.next()
        
        
        self.active = start_active
        
        self.key = Keys(self._pad)
        
    def update(self, keys: Keys):
        if self.active:
            key = keys.checkkey()                
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
                self.addstr(f"{self.options[i]}", attr=curses.A_UNDERLINE)
            else:
                self.addstr(f"{self.options[i]}")
            self.addstr(" \n")
        
        self.draw()
        
    def next(self):
        self.selected += 1
        if self.selected >= len(self.options):
            self.selected = 0
        
        while self.selected in self.mask_options:
            self.selected += 1
            if self.selected >= len(self.options):
                self.selected = 0
        
    def prev(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.options) - 1
            
        while self.selected in self.mask_options:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.options) - 1
        
    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False
        
    def press(self):
        "Run the function associated with the selected option"
        self.funcs[self.selected]()
        
class Textbox(Pad):
    def __init__(self, 
                 width: int,  
                 height: int, 
                 vec: tuple[int, int],
                 enter_func,
                 **kargs: dict):
        self.message = ''
        super().__init__(width, height, vec, **kargs)
        self._enter_func = enter_func
        self.cursor_char = '|'
        self.cursor = self.cursor_char
        self.entry = ''
        
        self.events = Event_loop()
        self.events.new(self.cursorflash, 0.5)
        
    def cursorflash(self):
        if self.cursor == '':
            self.cursor = self.cursor_char
        else:
            self.cursor = ''
        
    def update(self, keys):
        if keys.checkkey() != -1:
            key = keys.usekey()
            if key == curses.KEY_BACKSPACE or key == Keys.KEY_BACKSPACE:
                self.entry = self.entry[:-1]
            elif key in [curses.KEY_ENTER, Keys.KEY_ENTER, Keys.KEY_PADENTER]:
                self._enter_func(self.entry)
            key = curses.keyname(key).decode("utf-8")
            if len(key) == 1:
                self.entry = self.entry + key
            
        self.clear()
        self.addstr(self.entry)
        self.addstr(self.cursor)
        self.addstr(self.message, [0, self.height-1])
        self.events.run()
        
        
class Popup_container:
    def __init__(self, 
                 width: int,  
                 height: int, 
                 vec: tuple[int, int],
                 **kargs: dict):
        self.width = width
        self.height = height
        self.vec = vec
        self.kargs = kargs
        
        self._pad = None # of type clockin.gui.ui.Pad NOT curses.pad
        
    def set_pad(self, pad: Pad):
        self._pad = pad
        self._pad.resize(self.width, self.height, self.vec)
        
    def destroy(self):
        self._pad = None        
        
    def draw(self):
        if self._pad != None:
            self._pad.draw()
    
    def update(self, keys:Keys):
        if self._pad != None:
            self._pad.update(keys)
    
    def resize(self, width: int, height: int, vec: tuple[int, int]):
        self.width = max(width, 0)
        self.height = max(height, 0)
        self.vec = vec
        if self._pad != None:
            self._pad.resize(width, height, vec)


class Task_menu(List_menu):
    def __init__(self, 
                 width: int,  
                 height: int, 
                 tasks: Tasks,
                 vec: tuple[int, int],
                 popup: Popup_container,
                 **kargs: dict):
        self.tasks = tasks
        funcs = [lambda name=name: self.select_task(name) for name in self.tasks.get_names()]
        
        funcs = funcs + [lambda: "hold", self.add_task, self.delete_task]
        super().__init__(width, height, vec, 
                         options=self.tasks.get_names() + ["", "Add Task", "Delete Task"], 
                         funcs=funcs, **kargs)
        self.popup = popup
        self.mask_options = [len(self.options) - 3]
        
    def recreate(self):
        "recreate the list and asociated functions"
        self.selected = 0
        self.funcs = []
        for name in self.tasks.get_names():
            self.funcs.append(lambda name=name: self.select_task(name))
        self.funcs = self.funcs + [lambda: "hold", self.add_task, self.delete_task]
        self.options=self.tasks.get_names() + ["", "Add Task", "Delete Task"]
        self.mask_options = [len(self.options) - 3]
        
    def add_task(self):
        self.deactivate()
        self.popup.set_pad(Textbox(10,10,[10,10], 
                                   bd=True, 
                                   enter_func=self.add_task_output,
                                   title="New Task Name", 
                                   message="[ENTER]"))
    
    def add_task_output(self, text):
        self.tasks.add(text)   
        self.exit_popup()
        
    def exit_popup(self):
        self.popup.destroy()
        self.recreate()
        self.activate()
    
    def delete_task(self):
        def check(name):
            def delete_this_task(name):
                self.tasks.pop(name)
                self.exit_popup()
            
            self.popup.destroy()
            options = [f"Delete [{name}]\nPermanently?",'',"No","Yes"]
            funcs=['','',self.exit_popup, lambda name=name: delete_this_task(name)]
            menu = List_menu(10,10,[10,10],
                             options=options,
                             funcs=funcs,
                             start_active=True,
                             mask_options=[0,1],
                             bd=True,
                             title=f"Delete Task")
            menu.attron(Color.RED)
            self.popup.set_pad(menu)
            
        
        self.deactivate()
        funcs = [self.exit_popup,'']
        for name in self.tasks.get_names():
            funcs.append(lambda name=name: check(name))
        self.popup.set_pad(List_menu(10,10,[10,10],
                                     options=["[Exit]",'',]+self.tasks.get_names(),
                                     funcs=funcs,
                                     start_active=True,
                                     mask_options=[1],
                                     bd=True,
                                     title="Delete Task"))
        
    def select_task(self, name):
        self.tasks.set_selected(name)


class Timer(Pad):
    def __init__(self, width: int, height: int, vec, tasks: Tasks, log: Log, **kargs: dict):
        super().__init__(width, height, vec, **kargs)
        self.tasks = tasks
        self.log = log
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
        self.tasks.event(self.timestart, self.timeend)
        self.log.log(f"{self.tasks.get_selected().name} duration: {self.gettime()}")
    
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
