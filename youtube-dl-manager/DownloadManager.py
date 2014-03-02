from threading import RLock, Thread

import xml.etree.ElementTree as ET
import xml.dom.minidom as MD

from Button import Button
from MessageAlert import MessageAlert

from Notification import Notification

from DownloadConfiguration import DownloadConfiguration
from DownloadThread import DownloadThread

class DownloadManager(object):
    XML_TAG = 'download-manager'
    DEFAULT_FILENAME = "download-manager.xml"

    # Posted when the download manager stops downloading because
    # the queue is empty.
    DONE_NOTIFICATION = "DownloadManagerDoneNotification"

    # Posted when the download manager stopped after a call to the
    # stop method. Note that this notification is NOT posted when
    # the manager stops due to an empty queue.
    STOPPED_NOTIFICATION = "DownloadManagerStoppedNotification"

    # Posted when the downloading of a new object has commenced.
    NEXT_DOWNLOAD_NOTIFICATION = "DownloadManagerNextDownloadNotification"

    # Posted when new output in self.output is available.
    NEW_OUTPUT_NOTIFICATION = "DownloadManagerNewOutputNotification"
    
    def __init__(self, filename=DEFAULT_FILENAME):
        self.queue = [] # Collection of DownloadConfiguration instances
        self.done = [] # Cellection of ... instances
        self.active = None # DownloadConfiguration instance or None

        # List of tuples (text, type) where text is a string and type
        # is 0 for stdout and 1 for stderr.
        self.output = []

        self.__downloadThread = None
        self.__shouldStop = False

        self.filename = filename

        self.__lock = RLock()

    # Saving and loading
    def synchronize(self):
        """Writes and saves the download status."""
        with self.__lock:
            tb = ET.TreeBuilder()
            tb.start(self.XML_TAG)

            # Queue
            tb.start('queue')
            for dc in self.queue:
                dc.addToTreeBuilder(tb)
            if self.active != None:
                self.active.addToTreeBuilder(tb)
            tb.end('queue')

            root = tb.close()
            tree = ET.ElementTree(root)
            tree.write(self.filename)
            
            
    def load(self):
        """Loads the download status from the file."""
        with self.__lock:
            doc = MD.parse(self.filename)
            root = doc.documentElement
            if root.tagName != self.XML_TAG:
                raise UnsupportedFormat()

            cn = root.childNodes
            for c in cn:
                if c.nodeType != MD.Node.ELEMENT_NODE:
                    continue
                if c.tagName == 'queue':
                    self.__parseQueue(c)


    def __parseQueue(self, queueElem):
        cn = queueElem.childNodes
        for c in cn:
            if c.nodeType != MD.Node.ELEMENT_NODE:
                continue
            if c.tagName == DownloadConfiguration.XML_TAG:
                dc = DownloadConfiguration.fromXMLElement(c)
                if dc != None:
                    self.queue.append(dc)

    # Managing queue
    def addToQueue(self, dc):
        """Adds a download configuration to the queue."""
        with self.__lock:
            self.queue.append(dc)
            self.synchronize()

    def removeFromQueue(self, index, alertParent=None):
        """Removes a download configuration from the queue.

        index - The index of the download configuration
        alertParent - The parent of the confirmation alert if you
           want to show one to the user. If you want to remove the
           download configuration without confiromation, pass None.
        """
        with self.__lock:
            if index >= len(self.queue):
                return

            if alertParent != None:
                self.__showRemovalConfirmation(index, alertParent)
            else:
                dc = self.queue[index]
                self.__removalConfiguration = dc
                self.__continueRemoval()

    def __showRemovalConfirmation(self, index, alertParent):
        with self.__lock:
            if index >= len(self.queue):
                return

            dc = self.queue[index]
            self.__removalConfiguration = dc

            title = "Are you sure you want to delete the selected "
            title+= "download configuration?"
            msg = "This operation cannot be undone."

            a = MessageAlert(alertParent, title, msg)
            b = Button("OK", self.__continueRemoval, Button.SHORTCUT_ENTER)
            a.addButton(b)
            b = Button("Cancel", self.__endRemovalConfirmation, 'c')
            a.addButton(b)
            
            self.__removalAlert = a
            alertParent.beginModalScreen(a)

    def __endRemovalConfirmation(self):
        self.__removalAlert.parent.endModalScreen(self.__removalAlert)
        self.__removalAlert = None

    def __continueRemoval(self):
        with self.__lock:
            try:
                self.queue.remove(self.__removalConfiguration)
                self.synchronize()
            except ValueError:
                pass
            
        self.__removalAlert.parent.endModalScreen(self.__removalAlert)
        self.__removalAlert = None


    # Downloading Objects
    def isDownloading(self):
        with self.__lock:
            return self.active != None

    def startDownloading(self):
        with self.__lock:
            self.__shouldStop = False
            if self.active != None:
                return

            self.__downloadNextItem()

    def stopDownloading(self):
        with self.__lock:
            self.__shouldStop = True

    def __downloadNextItem(self):
        with self.__lock:
            if self.__shouldStop == True:
                self.__shouldStop = False
                self.active = None

                notifName = DownloadThread.DONE_NOTIFICATION
                Notification.removeObserver(self, notifName)
                self.__notifyStopped()
                return

            if len(self.queue) == 0:
                self.active = None

                notifName = DownloadThread.DONE_NOTIFICATION
                Notification.removeObserver(self, notifName)
                self.__notifyDone()
                return

            # Start the download-thread
            notifName = DownloadThread.DONE_NOTIFICATION
            Notification.addObserver(self, notifName)

            notifName = DownloadThread.NEW_OUTPUT_NOTIFICATION
            Notification.addObserver(self, notifName)

            self.active = self.queue[0]
            del self.queue[0]
            self.__downloadThread = DownloadThread(self.active)
            self.__downloadThread.start()

            self.__notifyNextDownload()

    def __handleDownloadThreadDoneNotification(self, notif):
        if notif.sender != self.__downloadThread:
            return

        self.__downloadThread = None
        self.__downloadNextItem()

    def __handleDownloadThreadNewOutputNotification(self, notif):
        if notif.sender != self.__downloadThread:
            return

        self.output = notif.sender.output
        self.__notifyNewOutput()

    # Notification
    def __notifyDone(self):
        n = Notification(self.DONE_NOTIFICATION, self)
        Notification.post(n)

    def __notifyStopped(self):
        n = Notification(self.STOPPED_NOTIFICATION, self)
        Notification.post(n)

    def __notifyNextDownload(self):
        n = Notification(self.NEXT_DOWNLOAD_NOTIFICATION, self)
        Notification.post(n)

    def __notifyNewOutput(self):
        n = Notification(self.NEW_OUTPUT_NOTIFICATION, self)
        Notification.post(n)
        
    def handleNotification(self, notif):
        if notif.name == DownloadThread.DONE_NOTIFICATION:
            self.__handleDownloadThreadDoneNotification(notif)

        if notif.name == DownloadThread.NEW_OUTPUT_NOTIFICATION:
            self.__handleDownloadThreadNewOutputNotification(notif)
        


# Exceptions
class UnsupportedFormat(Exception):
    def __repr__(self):
        return "Unsupported document type. Your data is corrupted."

    def __str__(self):
        return self.__repr__()
    
