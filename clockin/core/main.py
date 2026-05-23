import time
import curses
from curses import wrapper
from curses.textpad import rectangle

from clockin.gui.ui import List_menu, Timer
from clockin.core.util import Delay



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
    #stdscr.nodelay(True)
    curses.curs_set(0)
    
    
    rectangle(stdscr, 0,0, 2,9)
    stdscr.addstr(1,1, "Clock In")
    stdscr.refresh()
    
    #init
    timer = Timer(1, 50, [20, 1])
    
    tasks_menu = List_menu(15, 18, [1, 3], ["T1", "task 2", "other thing 3"])
    tasks_menu.attron(COLOR_GREEN)
    
    timer.start()
    
    
    delay = Delay()
    
    end = False
    while not end:
        
        #update
        tasks_menu.update()
        
        #draw
        tasks_menu.draw()
        timer.draw()
        
        
        delay.delay(1/30)
    
    
    
    
    stdscr.getch()
    

def main():
    wrapper(app)