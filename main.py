import time
import curses
from curses import wrapper
from curses.textpad import rectangle



class Task:
    def __init__(self, name: str):
        self.name = name
        
class Pad:
    def __init__(self, nrow: int, ncol: int, vec: tuple[int, int]):
        self.nrow = nrow
        self.ncol = ncol 
        self.vec = vec
        
        self._pad = curses.newpad(self.nrow, self.ncol)
        
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
        
        if attr == None and vec == None:
            self._pad.addstr(str)
        elif attr != None and vec == None:
            self._pad.addstr(str, attr)
        elif attr == None and vec != None:
            self._pad.addstr(vec[1], vec[0], str)
        else:
            self._pad.addstr(vec[1], vec[0], str, attr)
        
    def draw(self):
        self._pad.refresh(0,0, 
                          self.vec[1], self.vec[0], 
                          self.vec[1] + self.nrow, self.vec[0] + self.ncol)
        
    
    
class List_menu(Pad):
    def __init__(self, nrow, ncol, vec, items: list):
        super().__init__(nrow, ncol, vec)
        self.items = items
        self.selected = None
        
    def update(self):
        pass
    
    
class Timer(Pad):
    def __init__(self, nrow, ncol, vec):
        super().__init__(nrow, ncol, vec)
        self.task = None
        self.active = False
        self.start = None
        
    def settask(self, task):
        self.task = task
        
    def start(self):
        self.start = time.time()
        
    def stop(self):
        pass
    
    def draw(self):
        self.addstr("thing | 11:02")
        return super().draw()
        
        


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    COLOR_GREEN = curses.color_pair(1)
    COLOR_RED = curses.color_pair(2)
    COLOR_BLUE = curses.color_pair(3)
    #stdscr.nodelay(True)
    curses.curs_set(0)
    
    
    
    
    
    rectangle(stdscr, 0,0, 2,9)
    stdscr.addstr(1,1, "Clock In")
    stdscr.refresh()
    
    timer = Timer(1, 15, [20, 1])
    
    
    
    tasks_menu = Pad(15, 18, [1, 3])
    tasks_menu.attron(COLOR_GREEN)
    
    tasks = ["T1", "task 2", "other thing 3"]
    for task in tasks:
        tasks_menu.addstr(task + '\n')
    
    tasks_menu.draw()
    timer.draw()
    
    
    
    end = False
    while not end:
        pass
    
    
    
    
    stdscr.getch()

if __name__ == "__main__":
    wrapper(main)