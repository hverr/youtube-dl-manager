import sys
import curses

from Notification import Notification

import QueueBox
import DoneBox
from StatusBox import StatusBox
from Screen import Screen
from Button import Button
from MessageAlert import MessageAlert
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

        self.statusBox = StatusBox(self, (1, 1))
        self.addChild(self.statusBox)

        self.doneBox = DoneBox.DoneBox(self, (1, 1))
        self.doneBox.downloadManager = self.downloadManager
        self.doneBoxDetails = DoneBox.DetailsScreen(self, self.doneBox)
        self.addChild(self.doneBox)
        self.addChild(self.doneBoxDetails)

        self.automaticallyCycleThroughChildren = True

        self.__pendingAlert = None
        try:
            self.downloadManager.load()
        except FileNotFoundError:
            pass
        except Exception as e:
            self.__handleException(e)

        ns = [DownloadManager.NEXT_DOWNLOAD_NOTIFICATION,
             DownloadManager.DONE_NOTIFICATION,
             DownloadManager.STOPPED_NOTIFICATION]
        for n in ns:
            Notification.addObserver(self, n)

            
    
    # Drawing
    def layout(self):
        h, w = (i - 2 for i in self.size)

        qbdHeight = self.queueBoxDetails.size[0] - 1
        dbdHeight = self.doneBoxDetails.size[0] - 1
        heightLeft = h - qbdHeight - dbdHeight
        
        self.queueBox.size = [int(heightLeft/3), w]

        y = self.queueBox.size[0] + self.queueBoxDetails.size[0]
        x = 1
        self.statusBox.origin = [y, x]
        self.statusBox.size = (int(heightLeft/3), w)

        y += self.statusBox.size[0]
        self.doneBox.size = (int(heightLeft/3), w)
        self.doneBox.origin = [y, x]

        emptyHeight = h - y - self.doneBox.size[0] - dbdHeight + 1
        
        self.queueBox.size[0] += emptyHeight
        self.statusBox.origin[0] += emptyHeight
        self.doneBox.origin[0] += emptyHeight

        
        
    def display(self):
        self.clear()
        self.size = self.stdscr.getmaxyx()
        self.__drawBox()
        self.__drawLegend()

        if self.__pendingAlert != None:
            alert = self.__pendingAlert
            self.__pendingAlert = None
            self.beginModalScreen(alert)


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

    def __drawLegend(self):
        legend = ['[s] ', '[q] Quit']
        if self.downloadManager.isDownloading():
            legend[0] += 'Stop downloading'
        else:
            legend[0] += 'Start downloading'

        y, x = self.abs(self.size[0] - 1, self.size[1] - 3)
        for l in legend:
            l = ' ' + l + ' '
            x -= len(l)
            self.addstr(y, x, l)
            x -= 2

    # Events
    def acceptsFirstResponder(self):
        return True

    def respondsTo(self, key):
        if chr(key) in ['s', 'q']:
            return True
        return super(MainScreen, self).respondsTo(key)

    def handleEvent(self, key):
        if chr(key) == 's':
            self.__toggleDownloading()
        elif chr(key) == 'q':
            self.__exitApplication()

        return super(MainScreen, self).handleEvent(key)

    def __toggleDownloading(self):
        if self.downloadManager.active == None:
            self.downloadManager.startDownloading()
        else:
            self.downloadManager.stopDownloading()

    def __exitApplication(self):
        title = "Are you sure you want to exit?"
        msg = "All download processes will be forcefully stopped."
        a = MessageAlert(self, title, msg)

        b = Button("Quit", self.__continueExit, Button.SHORTCUT_ENTER)
        a.addButton(b)
        b = Button("Cancel", self.__endAlert, 'c')
        a.addButton(b)

        self.beginModalScreen(a)

    def __handleException(self, exception):
        t = "An error occurred."
        m = str(exception)
        alert = MessageAlert(self, t, m)

        b = Button("OK", self.__handleErrorOK, Button.SHORTCUT_ENTER)
        alert.addButton(b)

        if not self.isFirstResponder():
            self.__pendingAlert = alert
            return
                        
        self.beginModalScreen(alert)

    def __continueExit(self):
        sys.exit(0)

    def __endAlert(self):
        self.endModalScreen(self.activeModalSession())

    def __handleErrorOK(self):
        self.endModalScreen(self.activeModalSession())

    # Notifications
    def handleNotification(self, n):
        if n.name == DownloadManager.STOPPED_NOTIFICATION:
            self.__handleDownloadManagerStoppedNotification()

        elif n.name == DownloadManager.DONE_NOTIFICATION:
            self.__handleDownloadManagerDoneNotification()

        elif n.name == DownloadManager.NEXT_DOWNLOAD_NOTIFICATION:
            self.__handleDownloadManagerNextDownloadNotification()

    def __handleDownloadManagerStoppedNotification(self):
        self.statusBox.status = StatusBox.STATUS_IDLE

        self.update()

    def __handleDownloadManagerDoneNotification(self):
        self.statusBox.status = StatusBox.STATUS_IDLE

        self.update()

    def __handleDownloadManagerNextDownloadNotification(self):
        self.statusBox.status = StatusBox.STATUS_DOWNLOADING

        fn = self.downloadManager.active.filename
        self.statusBox.currentObject = fn

        self.update()
        


    
