import curses
import time
from threading import Thread

from Notification import Notification

class DownloadThread(Thread):

    # This notification is posted when the thread is finished
    DONE_NOTIFICATION = "DownloadThreadDoneNotification"

    # This notification is posted when new output is available
    NEW_OUTPUT_NOTIFICATION = "DownloadThreadNewOutputNotification"
    
    def __init__(self, downloadConfiguration):
        """Initializes a download thread.

        downloadConfiguration - The object to be downloaded. Must be
            an instance of DownloadConfiguration.
        doneHandler - A callable that will be called from this thread
            when the download has finished. It must accept exactly one
            argument. This will be None in case of success, or an
            Exception when one occurs.
        """
        super(DownloadThread, self).__init__()
        self.downloadConfiguration = downloadConfiguration

        # List of tuples (text, type) where text is a string and type
        # is 0 for stdout and 1 for stderr.
        self.output = []

    def run(self):

        dc = self.downloadConfiguration
        mo = self.downloadConfiguration.mediaObject
        mf = self.downloadConfiguration.mediaFormat

        self.output.append(("Starting download from " + mo.url, 0))
        self.__notifyNewOutput()

        mo.delegate = self
        mo.downloadMedia(dc.filename, mf.id)
        
        self.__notifyDone(None)
        pass

    def __notifyDone(self, e):
        n = Notification(self.DONE_NOTIFICATION, self)
        Notification.post(n)

    def __notifyNewOutput(self):
        n = Notification(self.NEW_OUTPUT_NOTIFICATION, self)
        Notification.post(n)

    # Media Object delegate
    def mediaObjectMessage(self, msg):
        self.output.append((msg, 0))
        self.__notifyNewOutput()

    def mediaObjectError(self, err):
        self.output.append((err, 1))
        self.__notifyNewOutput()
