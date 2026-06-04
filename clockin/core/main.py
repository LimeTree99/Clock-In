import curses
from curses import wrapper

from clockin.gui.ui import List_menu, Timer, Pad, Task_menu
from clockin.core.util import Delay
from clockin.core.keys import Keys
from clockin.core.task import Tasks


def app(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    COLOR_GREEN = curses.color_pair(1)
    COLOR_RED = curses.color_pair(2)
    COLOR_BLUE = curses.color_pair(3)
    curses.curs_set(0)
    
    tasks = Tasks()
    tasks.add("first")
    tasks.add("second")
    tasks.add("t3")
    tasks.add("t4")
    tasks.add("t5")
    
    keys = Keys(stdscr)
    
    
    logo = Pad(8, 1, [1,1], bd=True)
    logo.addstr("Clock In")
    
    timer = Timer(50, 1, [11, 1], tasks, bd=True)
    tasks_menu = Task_menu(width=25, 
                           height=17, 
                           vec=[1, 4], 
                           tasks=tasks,
                           title="Tasks", 
                           bd=True)
    log = Pad(50, 5, (1, 23), title="Log", bd=True)
    
    log.addstr("?"*(6*50))
    
    timer.start()
    tasks_menu.activate()
    
    
    delay = Delay()
    end = False
    while not end:
        
        #update
        keys.update()
        tasks_menu.update(keys)
        
        #log.addstr(keys.usekey(), (0,0))
        
        #draw
        tasks_menu.draw()
        timer.draw()
        log.draw()
        logo.draw()
        
        curses.doupdate()
        delay.delay(1/30)
        
    curses.endwin()
    

def main():
    wrapper(app)