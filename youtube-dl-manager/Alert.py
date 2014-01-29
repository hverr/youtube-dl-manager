import curses
import curses.ascii

from Screen import Screen
from Button import Button

class Alert(Screen):
    CONTENT_HEIGHT = 0

    def __init__(self, parent):
        super(Alert, self).__init__(parent, (0,0))

    def initialize(self):
        super(Alert, self).initialize()

        # A list containing (title, handler, shortcut) tuples
        self.buttons = []

        self.automaticallyCycleThroughChildren = True

    # Buttons
    def addButton(self, b):
        """Add a Button instance to the Alert.

        This method does not update the screen.
        """
        b.parent = self
        if len(self.buttons) == 0:
            self.children.append(b)
        else:
            insertIndex = self.children.index(self.buttons[0])
            self.children.insert(insertIndex, b)
            
        self.buttons.append(b)

    def addChild(self, c):
        c.parent = self
        if len(self.buttons) == 0:
            self.children.append(c)
        else:       
            insertIndex = self.children.index(self.buttons[0])
            self.children.insert(insertIndex, c)

    # Drawing
    def abs(self, y, x):
        y += self.origin[0]
        x += self.origin[1]
        return (y, x)
    
    def layout(self):
        # We go in the middle of the terminal
        # We are obnoxious
        termy, termx = self.getmaxyx()

        s = [self.CONTENT_HEIGHT + 3, int(0.7* termx)]

        x = int((termx - s[1])/2)
        y = int((termy - s[0])/2)

        self.origin = (y, x)
        self.size = s

        # Layout buttons
        self.__layoutButtons()

    def __layoutButtons(self):
        y, x = (self.size[0] - 2, self.size[1] - 2)
        for b in self.buttons:
            w = b.neededWidth()
            x -= (w + 1)
            b.origin = (y, x)
            
        
    def display(self):
        self.clean()
        self.box()

    def __shortcutPosition(self, title, shortcut):
        i = 0
        shortcut = shortcut.lower()
        for c in title.lower():
            if c == shortcut:
                return i
            i += 1
        return None

    # Events
    def respondsTo(self, key):
        c = chr(key).lower()
        # Check for shortcut
        for b in self.buttons:
            if b.shortcut.lower() == c:
                return True

        # If enter or space and on a button
        if key in [curses.ascii.LF, curses.ascii.CR, ord(' ')]:
            for b in self.buttons:
                if b.isFirstResponder():
                    return True

        return super(Alert, self).respondsTo(key)

    def handleEvent(self, key):
        c = chr(key).lower()

        # If enter or space and on a button
        if key in [curses.ascii.LF, curses.ascii.CR, ord(' ')]:
            for b in self.buttons:
                if b.isFirstResponder():
                    handler = b.handler
                    if handler != None:
                        handler()
                    return True

        # Check for shortcut
        foundButton = None
        for b in self.buttons:
            if b.shortcut.lower() == c:
                foundButton = b
                break

        if foundButton:
            self.makeChildFirstResponder(foundButton)

        # No button found
        return super(Alert, self).handleEvent(key)

    

            
            
