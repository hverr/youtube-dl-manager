import curses

class Screen(object):
    def __init__(self, parent, relOrigin, size=(None, None)):
        """Initializes a screen, which does nothing.

        parent - The parent screen. Must be a Screen object or None if
                 this is the root screen.
        relOrigin - The origin (y, x) of this screen relative to its parent.
        size - The size (height, width) of the screen.

        If this will be the root screen, please set stdscr accordingly.

        self.parentResponder - The parent responder. The screen will first
        try let this screen handle events. If it can't, it will handle the
        events itself.
        """
        self.stdscr = None
        self.parent = parent
        self.origin = relOrigin
        self.size = size
        self.children = []
        self.parentResponder = None

        self.initialize()

    def initialize(self):
        """Called when the screen is initialized.

        This method is the prefered method to override if you have custom
        initialization to do.
        """
        pass

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
            try:
                eval("self.parent." + funName)
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
            self.parent.abs(y, x)
        return (y, x)
    
    # Drawing
    def update(self):
        """Issues the screen and all its children to display."""
        self.layout()
        self.display()
        for child in self.children:
            child.update()
        
    def display(self):
        """Don't call this function directly, call update!"""
        pass

    def layout(self):
        """Subclasses should override this function to layout it's children.

        Don't call this function directly, call upate!
        """
        pass

    def clean(self):
        """Cleans the whole screen.

        Subclasses are encouraged to write custom methods that are more
        efficient.
        """
        empty = ' '*self.size[1]
        y, x = self.abs(0, 0)
        for i in range(0, self.size[0]):
            self.addstr(y+i, x, empty)

    def box(self, origin=(0,0), size=(None, None)):
        """Draws a box. The origin should be relative."""
        
        y, x = origin
        y, x = self.abs(y, x)
        h, w = size
        if h == None:
            h = self.size[0]
        if w == None:
            w = self.size[1]

        for i in range(x+1, x+w-1):
            self.addch(y, i, curses.ACS_HLINE)
            self.addch(y+h-1, i, curses.ACS_HLINE)

        for i in range(y+1, y+h-1):
            self.addch(i, x, curses.ACS_VLINE)
            self.addch(i, x+w-1, curses.ACS_VLINE)

        self.addch(y, x, curses.ACS_ULCORNER)
        self.addch(y+h-1, x, curses.ACS_LLCORNER)
        self.addch(y, x+w-1, curses.ACS_URCORNER)
        try:
            self.addch(y+h-1,x+w-1, curses.ACS_LRCORNER)
        except: # curses bug
            pass

    # Events
    def respondsTo(self, key):
        """This method will be called to check if the screen can handle a key.

        If this method returns False, the screen calling this method will try
        to handle the event itself. If this method returns True, the
        handleEvent method will be called, and the event will be discarded.

        key - The integer value returned by curses.getch
        """
        return False

    def handleEvent(self, key):
        """Handle an event.

        This method will only be called if respondsTo returns True for the key.

        key - The integer value returned by curses.getch
        """
        pass
        
            
        
