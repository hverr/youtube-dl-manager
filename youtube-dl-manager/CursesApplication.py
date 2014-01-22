import curses

from MainScreen import MainScreen


class CursesApplication(object):
    def __init__(self):
        pass

    def run(self):
        curses.wrapper(self.__cursesWrapper)

    def __cursesWrapper(self, stdscr):
        size = stdscr.getmaxyx()
        ms = MainScreen(None, (0,0), size)
        ms.stdscr = stdscr
        ms.update()

        # Main runloop
        while True:
            # List of responders
            c = stdscr.getch()
            
            r = ms
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

                
                    
        
        
