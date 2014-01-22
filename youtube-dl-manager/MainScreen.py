import curses

from Screen import Screen
from QueueBox import QueueBox

class MainScreen(Screen):
    def initialize(self):
        self.queueBox = QueueBox(self, (1, 1))
        self.queueBox2 = QueueBox(self, (10, 1))
        self.addChild(self.queueBox)
        self.addChild(self.queueBox2)

        self.automaticallyCycleThroughChildren = True
    
    # Drawing
    def layout(self):
        self.queueBox.size = (int(self.size[0]/3), self.size[1]-2)
        self.queueBox2.size = (int(self.size[0]/3), self.size[1]-2)
        
    def display(self):
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

    
