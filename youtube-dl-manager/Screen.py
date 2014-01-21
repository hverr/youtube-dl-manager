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
        self.children = []

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
        
        try:
            eval("self.stdscr." + funName)
            return actOnStdscr
        except AttributeError:
            pass
        raise AttributeError(funName)

    # Managing children
    def addChild(self, c):
        """Adds a child and sets its parent."""
        c.parent = self
        self.children.append(c)

    # Coordinate system
    def abs(self, y, x):
        """Calculates the coordinates of y and x in the curses screen."""
        y += self.origin[0]
        x += self.origin[1]
        if self.parent != None:
            super(Screen, self).abs(y, x)
        return (y, x)
    
    # Drawing
    def update(self):
        """Issues the screen and all its children to display."""
        self.display()
        for child in self.children:
            child.update()
        
    def display(self):
        """Don't call this function directly, call update!"""
        pass
            
        
