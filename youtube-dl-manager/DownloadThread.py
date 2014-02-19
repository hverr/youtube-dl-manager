
import time
from threading import Thread

from Notification import Notification

class DownloadThread(Thread):

    # This notification is posted when the thread is finished
    DONE_NOTIFICATION = "DownloadThreadDoneNotification"
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

    def run(self):
        time.sleep(3)
        self.__notifyDone(None)
        pass

    def __notifyDone(self, e):
        n = Notification(self.DONE_NOTIFICATION, self)
        Notification.post(n)
