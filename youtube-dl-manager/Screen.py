import curses

class Screen(object):
    def __init__(self, parent, relOrigin, size=(None, None)):
        """Initializes a screen, which does nothing.

        parent - The parent screen. Must be a Screen object or None if
                 this is the root screen.
        relOrigin - The origin (y, x) of this screen relative to its parent.
        size - The size (height, width) of the screen.

        If this will be the root screen, please set stdscr accordingly.
        """
        self.stdscr = None
        self.parent = parent
        self.origin = relOrigin
        self.size = size

    # Accessing the stdscr
    def actOnStdscr(self, funName, *args, **kwargs):
        if self.stdscr != None:
            f = eval("self.stdscr." + funName)
        else:
            f = eval("self.parent." + funName)
            
        return f(*args, **kwargs)
        
    def __getattr__(self, funName):
        def actOnStdscr(*args, **kwargs):
            if self.stdscr != None:
                f = eval("self.stdscr." + funName)
            else:
                f = eval("self.parent." + funName)
                
            return f(*args, **kwargs)
        
        allowedNames = [
            'getch',
            'addstr'
        ]
        if funName in allowedNames:
            return actOnStdscr
        return super(Screen, self).__getattr__(funName)

    # Coordinate system
    def absoluteCoordinates(self, y, x):
        """Calculates the coordinates of y and x in the curses screen."""
        y += self.origin[0]
        x += self.origin[1]
        if self.parent != None:
            super(Screen, self).absoluteCoordinates(y, x)
        return (y, x)
    
    # Drawing
    def display(self):
        pass
            
        
