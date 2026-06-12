import curses 

class Color:
    GREEN = None
    RED = None
    BLUE = None
    def init():
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        
        Color.GREEN = curses.color_pair(1)
        Color.RED = curses.color_pair(2)
        Color.BLUE = curses.color_pair(3)
        
