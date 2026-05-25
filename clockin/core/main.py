import time
import curses
from curses import wrapper
from curses.textpad import rectangle

from clockin.gui.ui import List_menu, Timer, Pad
from clockin.core.util import Delay
from clockin.core.keys import Keys



class Task:
    def __init__(self, name: str):
        self.name = name
        

def app(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    COLOR_GREEN = curses.color_pair(1)
    COLOR_RED = curses.color_pair(2)
    COLOR_BLUE = curses.color_pair(3)
    curses.curs_set(0)
    
    keys = Keys(stdscr)
    
    logo = Pad(8, 1, [1,1], bd=True)
    logo.addstr("Clock In")
    logo.draw()
    
    #init
    timer = Timer(50, 1, [20, 1])
    tasks_menu = List_menu(18, 15, [1, 3], ["T1", "task 2", "other thing 3"])
    log = Pad(50, 5, (1, 18), bd=True)
    
    log.addstr("?"*(6*50))
    log.addstr(f" <{log._pad.getyx()}> ", (0,0))
    
    timer.start()
    
    
    delay = Delay()
    end = False
    while not end:
        
        #update
        tasks_menu.update()
        keys.update()
        
        log.addstr(keys.usekey(), (0,0))
        
        #draw
        tasks_menu.draw()
        timer.draw()
        log.draw()
        
        
        delay.delay(1/30)
    
    
    
    
    stdscr.getch()
    

def main():
    wrapper(app)