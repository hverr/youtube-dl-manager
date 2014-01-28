import curses
import time

from MainScreen import MainScreen


class CursesApplication(object):
    MIN_SIZE = (80,24)
    
    def __init__(self):
        pass

    def run(self):
        curses.wrapper(self.__cursesWrapper)

    def __cursesWrapper(self, stdscr):
        curses.curs_set(0) # No cursor
        
        self.mainScreen = MainScreen(None, (0,0))
        self.mainScreen.stdscr = stdscr

        # Make sure the terminal has enough space
        self.__handleTerminalResize(False)
        self.mainScreen.makeFirstResponder()

        # Main runloop
        while True:
            # List of responders
            c = stdscr.getch()
            if c == curses.KEY_RESIZE:
                self.__handleTerminalResize()
                continue

            # Timing for debugging purposes
            time1 = time.time()
            
            r = self.mainScreen
            responders = [r]
            while True: 
                r = r.parentResponder
                if r != None:
                    responders.append(r)
                else:
                    break

            # Top down
            for i in range(len(responders)-1, -1, -1):
                r = responders[i]
                if r.respondsTo(c):
                    r.handleEvent(c)
                    break
                
            # Next key
            time2 = time.time()

            size = stdscr.getmaxyx()
            s = 'Handling key %d took %0.3f ms' % (c, ((time2-time1)*1000.0))
            stdscr.addstr(size[0]-1, 0, s)

    def __handleTerminalResize(self, shouldRedraw=True):
        newSize = self.mainScreen.stdscr.getmaxyx()
        while newSize[0] < self.MIN_SIZE[1] or newSize[1] < self.MIN_SIZE[0]:
            self.mainScreen.stdscr.clear()
            error = "The minimal terminal size is " + str(self.MIN_SIZE)
            error = error[:newSize[1]]
            if newSize[1] > 1:
                self.mainScreen.stdscr.addstr(0, 0, error)

            self.mainScreen.stdscr.getch()
            newSize = self.mainScreen.stdscr.getmaxyx()
            
        self.mainScreen.size = newSize
        if shouldRedraw:
            self.mainScreen.clear()
            self.mainScreen.update()

                
                    
        
        
