import curses
from curses import wrapper

from clockin.gui.ui import List_menu, Timer, Pad, Task_menu, Log
from clockin.core.util import Delay
from clockin.core.keys import Keys
from clockin.core.task import Tasks

from clockin.gui import Color


def app(stdscr):
    curses.curs_set(0)
    Color.init()
    
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
    log = Log(25, 17, (28, 4), title="Log", bd=True)
    
    log.log(">"+"0"*30)
    log.log(">"+"1"*30)
    log.log(">"+"2"*30)
    log.log(">"+"3"*30)
    log.log(">"+"4"*30)
    log.log(">"+"5"*30)
    log.log(">"+"6"*30)
    log.log(">"+"7"*30)
    log.log(">"+"8"*30)
    log.log(">"+"9"*30)
    
    tasks_menu.activate()
    
    
    delay = Delay()
    end = False
    while not end:
        #update
        keys.update()
        tasks_menu.update(keys)
        timer.update(keys)
                
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