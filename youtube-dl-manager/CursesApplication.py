import curses

from MainScreen import MainScreen


class CursesApplication(object):
    def __init__(self):
        pass

    def run(self):
        curses.wrapper(self.__cursesWrapper)

    def __cursesWrapper(self, stdscr):
        ms = MainScreen(None, (0,0))
        ms.stdscr = stdscr
        ms.update()
        stdscr.getch()
        
        
