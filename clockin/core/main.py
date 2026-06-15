import curses
from curses import wrapper

from clockin.gui.ui import List_menu, Timer, Pad, Task_menu, Log, Popup_container
from clockin.core.util import Delay
from clockin.core.keys import Keys
from clockin.core.task import Tasks

from clockin.gui import Color


def app(stdscr):
    curses.curs_set(0)
    Color.init()
    term_height, term_width = stdscr.getmaxyx()
    
    tasks = Tasks()
    tasks.add("first")
    tasks.add("second")
    tasks.add("t3")
    tasks.add("t4")
    tasks.add("t5")
    
    keys = Keys(stdscr)
    
    logo = Pad(8, 1, [1,1], bd=True)
    logo.addstr("Clock In")
    
    popup = Popup_container(width=20, 
                            height=5,
                            vec=(term_width//2-20//2, term_height//2-5//2), 
                            title="Popup", 
                            bd="True")
    
    timer = Timer(term_width-13, 1, [11, 1], tasks, bd=True)
    tasks_menu = Task_menu(width=term_width//2-2, 
                           height=term_height-6, 
                           vec=[1, 4], 
                           tasks=tasks,
                           popup=popup,
                           title="Tasks", 
                           bd=True)
    log = Log(width=term_width//2-3, 
              height=term_height-6, 
              vec=(term_width//2+1, 4), 
              title="Log", 
              bd=True)
    
    
    log.log(">"+"press space to start and stop the task")
    log.log(">"+"select the task")
    log.log(">"+"select create a task")
    log.log(">"+"navigate with arrow keys and [enter] to select an option")
    
    tasks_menu.activate()
    
    draw_list = [tasks_menu, log, timer, logo, popup]
    update_list = [tasks_menu, timer, popup]
    delay = Delay()
    end = False
    while not end:
        #update
        keys.update()
        if keys.checkkey() == curses.KEY_RESIZE:
            keys.usekey()
            log.log("> resize")
            curses.curs_set(0)
            term_height, term_width = stdscr.getmaxyx()
            log.resize(width=term_width//2-3, 
                       height=term_height-6,
                       vec=(term_width//2+1, 4))
            tasks_menu.resize(width=term_width//2-2, 
                              height=term_height-6, 
                              vec=[1, 4],)
            timer.resize((term_width//2)*2-13, 1, [11, 1])
            
        for pad in update_list:
            pad.update(keys)        
                
        for pad in draw_list:
            pad.draw()
        
        curses.doupdate()
        delay.delay(1/30)
        
    curses.endwin()
    

def main():
    try:
        wrapper(app)
    except KeyboardInterrupt:
        # put quitting routine here
        pass 
        