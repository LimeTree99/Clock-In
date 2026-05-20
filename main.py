import time
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle



class Task:
    def __init__(self, name):
        self.name = name


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    COLOR_GREEN = curses.color_pair(1)
    COLOR_RED = curses.color_pair(2)
    COLOR_BLUE = curses.color_pair(3)
    #stdscr.nodelay(True)
    curses.curs_set(0)
    
    win = curses.newwin(0, 18, 4, 1)
    
    
    
    rectangle(stdscr, 0,0, 2,9)
    stdscr.addstr(1,1, "Clock In")
    stdscr.refresh()
    
    win.attron(COLOR_GREEN)
    
    tasks = ["T1", "task 2", "other thing 3"]
    
    for task in tasks:
        win.addstr(task + '\n')
        
    win.refresh()
    
    
    
    
    stdscr.getch()

if __name__ == "__main__":
    wrapper(main)