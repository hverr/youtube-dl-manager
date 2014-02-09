
from threading import RLock

import xml.etree.ElementTree as ET

class DownloadManager(object):
    XML_TAG = 'download-manager'
    DEFAULT_FILENAME = "download-manager.xml"
    def __init__(self, filename=DEFAULT_FILENAME):
        self.queue = [] # Collection of DownloadConfiguration instances
        self.done = [] # Cellection of ... instances
        self.active = None # DownloadConfiguration instance or None

        self.filename = filename

        self.lock = RLock()

    # Saving and loading
    def synchronize(self):
        """Writes and saves the download status."""
        with self.lock:
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

    # Managing queue
    def addToQueue(self, dc):
        """Adds a download configuration to the queue."""
        with self.lock:
            self.queue.append(dc)
            self.synchronize()


    
