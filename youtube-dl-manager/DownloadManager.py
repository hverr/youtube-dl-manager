import curses

from threading import RLock, Thread

import xml.etree.ElementTree as ET
import xml.dom.minidom as MD

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
    
    def __init__(self, filename=DEFAULT_FILENAME):
        self.queue = [] # Collection of DownloadConfiguration instances
        self.done = [] # Cellection of ... instances
        self.active = None # DownloadConfiguration instance or None

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

            self.active = self.queue[-1]
            del self.queue[-1]
            self.__downloadThread = DownloadThread(self.active)
            self.__downloadThread.start()

    def __handleDownloadThreadDoneNotification(self, notif):
        if notif.sender != self.__downloadThread:
            return

        self.__downloadThread = None
        self.__downloadNextItem()

    # Notification
    def __notifyDone(self):
        n = Notification(self.DONE_NOTIFICATION, self)
        Notification.post(n)

    def __notifyStopped(self):
        n = Notification(self.STOPPED_NOTIFICATION, self)
        Notification.post(n)
        
    def handleNotification(self, notif):
        if notif.name == DownloadThread.DONE_NOTIFICATION:
            self.__handleDownloadThreadDoneNotification(notif)
        


# Exceptions
class UnsupportedFormat(Exception):
    def __repr__(self):
        return "Unsupported document type. Your data is corrupted."

    def __str__(self):
        return self.__repr__()
    
