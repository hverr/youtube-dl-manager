import curses



class CursesApplication(object):
    def __init__(self):
        pass

    def run(self):
        curses.wrapper(self.__cursesWrapper)

    def __cursesWrapper(self, stdscr):
        stdscr.addstr(1,1, "Hello World!")
        stdscr.getch()
        
        
