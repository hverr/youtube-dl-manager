import curses

from Screen import Screen
from QueueBox import QueueBox
from Alert import Alert
from Button import Button

class MainScreen(Screen):
    def initialize(self):
        self.queueBox = QueueBox(self, (1, 1))
        self.queueBox2 = QueueBox(self, (10, 1))
        self.addChild(self.queueBox)
        self.addChild(self.queueBox2)

        self.alert = Alert(self)
        self.alert.addButton(Button("OK", self.endAlert, Button.SHORTCUT_ENTER))
        self.alert.addButton(Button("Cancel", None, 'c'))

        self.automaticallyCycleThroughChildren = True
    
    # Drawing
    def layout(self):
        self.queueBox.size = (int(self.size[0]/3), self.size[1]-2)
        self.queueBox2.size = (int(self.size[0]/3), self.size[1]-2)
        
    def display(self):
        self.clear()
        self.size = self.stdscr.getmaxyx()
        self.__drawBox()


    def __drawBox(self):
        self.box()

        title = "Youtube DL Manager"
        y, x = self.abs(0,3)
        self.addstr(y, x, title, curses.A_BOLD)

    # Events
    def acceptsFirstResponder(self):
        return True

    def respondsTo(self, key):
        if chr(key) == 'a':
            return True
        return super(MainScreen, self).respondsTo(key)

    def handleEvent(self, key):
        if chr(key) == 'a':
            self.beginModalScreen(self.alert)
            return True

        return super(MainScreen, self).handleEvent(key)

    def endAlert(self):
        self.endModalScreen(self.alert)

    
