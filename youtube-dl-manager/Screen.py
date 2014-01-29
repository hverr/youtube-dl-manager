import curses
import curses.ascii

MAC_OS_SHIFT_TAB = 353

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

        # Wether the screen should try and cycle between
        # the children when Tab and Arrow keys are used.
        self.automaticallyCycleThroughChildren = False

        # This property only shows wether this screen is in
        # the active responder chain. Use self.parentResponder
        # to check if it is really at the top.
        self.__isFirstResponder = False

        # Used to manage model sessions
        self.__modalScreens = []
        self.__firstResponderPreModalScreen = None

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

    def removeChild(self, c):
        """Removes a child and unsets its parent.

        This method does not throw an error when the child can't be found.
        """
        try:
            i = self.children.index(c)
            c.parent = None
            del self.children[i]
        except ValueError:
            pass

    # Coordinate system
    def abs(self, y, x):
        """Calculates the coordinates of y and x in the curses screen."""
        y += self.origin[0]
        x += self.origin[1]
        if self.parent != None:
            y, x = self.parent.abs(y, x)
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
        cycle = self.automaticallyCycleThroughChildren
        if cycle and self.activeModalSession() == None:
            nextKeys = [curses.ascii.TAB,
                        curses.KEY_RIGHT,
                        curses.KEY_DOWN]
            prevKeys = [curses.ascii.DEL,
                        curses.KEY_UP,
                        curses.KEY_LEFT,
                        MAC_OS_SHIFT_TAB]
            if key in nextKeys:
                return self.__hasNextChildForFirstResponder()
            elif key in prevKeys:
                return self.__hasPreviousChildForFirstResponder()
        
        return False

    def handleEvent(self, key):
        """Handle an event.

        This method will only be called if respondsTo returns True for the key.

        key - The integer value returned by curses.getch
        """
        cycle = self.automaticallyCycleThroughChildren
        if cycle and self.activeModalSession() == None:
            nextKeys = [curses.ascii.TAB,
                        curses.KEY_RIGHT,
                        curses.KEY_DOWN]
            prevKeys = [curses.ascii.DEL,
                        curses.KEY_UP,
                        curses.KEY_LEFT,
                        MAC_OS_SHIFT_TAB]
            if key in nextKeys:
                return self.__makeNextChildFirstResponder()
            elif key in prevKeys:
                return self.__makePreviousChildFirstResponder()

    def makeChildFirstResponder(self, c, shouldUpdate=True):
        """Makes a child the first responder, after resigning the current.

        A screen must be a first responder itself, to be allowed to do this.
        """

        try:
            self.children.index(c)
        except ValueError:
            if c == None:
                pass
            else:
                raise Exception("Child not found")

        if self.isFirstResponder() == False:
            raise Exception("Not in the responder chain")

        curFirst = None
        for child in self.children:
            if child.isFirstResponder():
                curFirst = child
                break

        if c == curFirst:
            return

        if curFirst != None:
            curFirst.resignFirstResponder(shouldUpdate)
        if c != None:
            c.makeFirstResponder(shouldUpdate)
        self.parentResponder = c

    def __hasNextChildForFirstResponder(self):
        nextFirst = self.__getNextChildForFirstResponder()[1]
        return nextFirst != None

    def __makeNextChildFirstResponder(self):
        curFirst, nextFirst = self.__getNextChildForFirstResponder()

        curFirst.resignFirstResponder()
        nextFirst.makeFirstResponder()
        self.parentResponder = nextFirst

    def __getNextChildForFirstResponder(self):
        """Returns the current and the next first responder.

        The return value is a tuple of the current child that is the
        first responder or None and the child that is suitable as the
        next first responder or None.
        """
        curFirst = None
        index = 0
        for child in self.children:
            if child.isFirstResponder():
                curFirst = child
                break
            index += 1
        if curFirst == None:
            index = -1


        nextFirst = None
        for i in range(index + 1, len(self.children)):
            child = self.children[i]
            if child.acceptsFirstResponder():
                nextFirst = child
                break

        return (curFirst, nextFirst)

    def __hasPreviousChildForFirstResponder(self):
        prevFirst = self.__getPreviousChildForFirstResponder()[1]
        return prevFirst != None

    def __makePreviousChildFirstResponder(self):
        curFirst, prevFirst = self.__getPreviousChildForFirstResponder()
        curFirst.resignFirstResponder()
        prevFirst.makeFirstResponder()
        self.parentResponder = prevFirst

    def __getPreviousChildForFirstResponder(self):
        """Returns the current and the previous first responder.

        See __getNextChildForFirstResponder
        """
        curFirst = None
        index = 0
        for child in self.children:
            if child.isFirstResponder():
                curFirst = child
                break
            index += 1
        if curFirst == None:
            index = len(self.children)

        prevFirst = None
        for i in range(index - 1, -1, -1):
            child = self.children[i]
            if child.acceptsFirstResponder():
                prevFirst = child
                break
        return (curFirst, prevFirst)
        

    def acceptsFirstResponder(self):
        """Wether this widget accepts to be at the top of the responder chain.

        Note: This method is used to skip elements when searching for a
        first responder. If this method returns false. This screen AND its
        children cannot receive events.
        """
        return True
    
    def makeFirstResponder(self, shouldUpdate=True):
        """Make this screen and its children the first responder.

        This method first tries to make a child the first responder. If
        there is no child that accepts this, it tries to make the screen
        itself the first responder. If that doesn't work False is returned.

        Return value: True or False
        """
        if not self.acceptsFirstResponder():
            return False

        if self.__isFirstResponder:
            return True
        
        self.__isFirstResponder = True
        childFound = False
        for c in self.children:
            if c.acceptsFirstResponder:
                self.parentResponder = c
                if c.makeFirstResponder(False):
                    childFound = True
                    break

        # No suitable child was found, we are at the top
        if childFound == False:
            self.parentResponder = None

        if shouldUpdate:
            self.update()
        return True

    def resignFirstResponder(self, shouldUpdate=True):
        """Stop being the first responder."""
        if self.acceptsFirstResponder() == False:
            return

        self.__isFirstResponder = False
        if self.parentResponder != None:
            self.parentResponder.resignFirstResponder(False)

        if shouldUpdate:
            self.update()

    def isFirstResponder(self):
        return self.__isFirstResponder

    # Modal Screens
    def beginModalScreen(self, screen):
        """Begins a modal session with the screen as the modal window.

        Each session must be ended with a corresponding call to
        endModalScreen. Multiple modal sessions can be up at the same
        time, but must be ended in the reverse order they were started.
        """
        self.__modalScreens.append(screen)
        self.addChild(screen)

        if self.parentResponder != None:
            self.__parentResponderPreModalScreen = self.parentResponder

        self.makeChildFirstResponder(screen, False)
        self.update()

    def endModalScreen(self, screen):
        """Ends a modal session.

        The session being ended must be at the top of the modal session stack.
        """
        if self.__modalScreens[-1] != screen:
            raise Exception("Screen not at top of modal session stack.")

        del self.__modalScreens[-1]
        self.makeChildFirstResponder(self.__parentResponderPreModalScreen,
                                     False)
        self.removeChild(screen)
        self.update()

        

    def activeModalSession(self):
        if len(self.__modalScreens) == 0:
            return None
        return self.__modalScreens[-1]

        
    
        
        
            
        
