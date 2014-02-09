import curses

import QueueBox
from Screen import Screen
from VideoURLDialog import VideoURLDialog

from DownloadManager import DownloadManager

class MainScreen(Screen):
    def __init__(self, filename=None, *args, **kwargs):
        """Initializes the main screen.

        filename - The filename to store the download manager status.
                   None implies the default filename.
        """
        if filename != None:
            self.downloadManager = DownloadManager(filename)
        else:
            self.downloadManager = DownloadManager()
            
        super(MainScreen, self).__init__(*args, **kwargs)
        
    def initialize(self):
        self.queueBox = QueueBox.QueueBox(self, (1, 1))
        self.queueBox.downloadManager = self.downloadManager
        self.queueBoxDetails = QueueBox.DetailsScreen(self, self.queueBox)
        self.addChild(self.queueBox)
        self.addChild(self.queueBoxDetails)

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

        maxWidth = self.size[1] - 6 - len(title) - 8
        s = self.downloadManager.filename 
        sl = len(s)
        if sl > maxWidth:
            s = s[sl-maxWidth+3:]
            s = "..." + s
            sl = maxWidth
        y, x = self.abs(0, self.size[1] - 3 - sl)
        self.addstr(y, x, s)

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
        self.downloadManager.addToQueue(dc)

    
