import curses

from Screen import Screen

from Notification import Notification

from DownloadManager import DownloadManager

class StatusBox(Screen):
    STATUS_IDLE = 'idle'
    STATUS_DOWNLOADING = 'downloading'
    
    def initialize(self):
        self.status = self.STATUS_IDLE
        self.currentObject = None # Set this to a string

        self.output = []
        n = DownloadManager.NEW_OUTPUT_NOTIFICATION
        Notification.addObserver(self, n)

    # Drawing
    def display(self):
        self.clean()
        self.box()

        self.__drawTitle()
        self.__drawOutput()

    def __drawTitle(self):
        y, x = self.abs(0, 3)
        s = "Status: "
        self.addstr(y, x, s, curses.A_BOLD)
        x += len(s)
        if self.status == self.STATUS_IDLE:
            self.addstr(y, x, "idle")
        elif self.status == self.STATUS_DOWNLOADING:
            d = "downloading"
            self.addstr(y, x, d)
            if self.currentObject != None:
                self.addstr(y, x + len(d), " '" + self.currentObject + "'")
        else:
            raise Exception("Invalid status")

    def __drawOutput(self):
        if self.status != self.STATUS_DOWNLOADING:
            return

        y, x = self.abs(1, 1)
        maxWidth = self.size[1] - 2

        numLines = self.size[0]
        if numLines > len(self.output):
            startIndex = 0
            endIndex = len(self.output)
        else:
            startIndex = len(self.output) - numLines
            endIndex = startIndex + numLines

        for i in range(startIndex, endIndex):
            self.addstr(y, x, self.output[i][0])
            y += 1
        

    # Notifications
    def handleNotification(self, notif):
        if notif.name == DownloadManager.NEW_OUTPUT_NOTIFICATION:
            self.__handleNewOutputNotification(notif)

    def __handleNewOutputNotification(self, notif):
        self.output = list(notif.sender.output)
        self.update()

    # Events
    def acceptsFirstResponder(self):
        return False
