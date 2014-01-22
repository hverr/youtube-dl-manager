import curses

from Screen import Screen
from QueueBox import QueueBox

class MainScreen(Screen):
    def initialize(self):
        self.queueBox = QueueBox(self, (1, 1))
        self.addChild(self.queueBox)
    
    # Drawing
    def layout(self):
        self.queueBox.size = [i-2 for i in self.size]
        
    def display(self):
        self.size = self.stdscr.getmaxyx()
        self.__drawBox()

    def __drawBox(self):
        self.box()

        title = "Youtube DL Manager"
        y, x = self.abs(0,3)
        self.addstr(y, x, title, curses.A_BOLD)

    
