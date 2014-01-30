import curses

from Screen import Screen
from QueueBox import QueueBox
from VideoURLDialog import VideoURLDialog

class MainScreen(Screen):
    def initialize(self):
        self.queueBox = QueueBox(self, (1, 1))
        self.addChild(self.queueBox)

        self.automaticallyCycleThroughChildren = True
    
    # Drawing
    def layout(self):
        self.queueBox.size = (int(self.size[0]/3), self.size[1]-2)
        
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
            self.videoURLDialog = VideoURLDialog(self)
            self.beginModalScreen(self.videoURLDialog)
            return True

        return super(MainScreen, self).handleEvent(key)

    # Download Configuration management
    def addDownloadConfiguration(self, dc):
        """Adds a DownloadConfiguration instance to the queue"""
        self.queueBox.downloadConfigurations.append(dc)

    
