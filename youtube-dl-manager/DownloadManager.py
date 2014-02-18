
from threading import RLock

import xml.etree.ElementTree as ET
import xml.dom.minidom as MD

from DownloadConfiguration import DownloadConfiguration

class DownloadManager(object):
    XML_TAG = 'download-manager'
    DEFAULT_FILENAME = "download-manager.xml"
    def __init__(self, filename=DEFAULT_FILENAME):
        self.queue = [] # Collection of DownloadConfiguration instances
        self.done = [] # Cellection of ... instances
        self.active = None # DownloadConfiguration instance or None

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


# Exceptions
class UnsupportedFormat(Exception):
    def __repr__(self):
        return "Unsupported document type. Your data is corrupted."

    def __str__(self):
        return self.__repr__()
    
