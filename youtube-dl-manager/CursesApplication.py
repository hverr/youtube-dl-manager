import curses
import time

from MainScreen import MainScreen


class CursesApplication(object):
    def __init__(self):
        pass

    def run(self):
        curses.wrapper(self.__cursesWrapper)

    def __cursesWrapper(self, stdscr):
        size = stdscr.getmaxyx()
        self.mainScreen = MainScreen(None, (0,0), size)
        self.mainScreen.stdscr = stdscr
        self.mainScreen.makeFirstResponder()

        # Main runloop
        while True:
            # List of responders
            c = stdscr.getch()

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

            s = 'Handling key %d took %0.3f ms' % (c, ((time2-time1)*1000.0))
            stdscr.addstr(size[0]-1, 0, s)

                
                    
        
        
