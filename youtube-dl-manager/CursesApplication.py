import sys
import curses

from InitializationScreen import InitializationScreen

from Notification import Notification

import Preferences

class CursesApplication(object):
    MIN_SIZE = (80,24)
    
    def __init__(self):
        pass

    def run(self):
        self.preferences = Preferences.Preferences()
        try:
            self.preferences.readPreferences()
        except Preferences.PreferencesException as e:
            print("An error occurred while parsing the preferences:",
                  e, file=sys.stderr)
            return
            
        curses.wrapper(self.__cursesWrapper)

    def __cursesWrapper(self, stdscr):
        curses.curs_set(0) # No cursor
        stdscr.nodelay(1) # getch returns immediately
        stdscr.notimeout(1) # escape sequences come immediately

        # Begin with the initialization screen
        prefs = self.preferences
        doneHandler = self.__initializationFinished
        self.mainScreen = InitializationScreen(prefs, doneHandler, None, (0, 0))
        self.mainScreen.stdscr = stdscr

        # Make sure the terminal has enough space
        self.__handleTerminalResize(False)
        self.mainScreen.makeFirstResponder()

        # Main runloop
        while True:
            # Notifications
            Notification.handleNotifications()

            # List of responders
            c = stdscr.getch()
            if c == -1:
                continue
            
            if c == curses.KEY_RESIZE:
                self.__handleTerminalResize()
                continue

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
                if r.activeModalSession() != None:
                    break
                
                if r.respondsTo(c):
                    r.handleEvent(c)
                    break

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

    def __initializationFinished(self):
        from MainScreen import MainScreen

        if len(sys.argv) >= 2:
            fn = sys.argv[1]
        else:
            fn = None

        stdscr = self.mainScreen.stdscr
        self.mainScreen = MainScreen(fn, None, (0,0))
        self.mainScreen.stdscr = stdscr
        self.__handleTerminalResize()
        self.mainScreen.makeFirstResponder()

                
                    
        
        
