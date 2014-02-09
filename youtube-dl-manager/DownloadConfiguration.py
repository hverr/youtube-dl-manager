
import xml.dom.minidom as MD

from MediaObject import MediaObject
from MediaFormat import MediaFormat

class DownloadConfiguration(object):
    XML_TAG = 'download-configuration'
    
    def __init__(self, mediaObject, mediaFormat, filename):
        self.mediaObject = mediaObject
        self.mediaFormat = mediaFormat
        self.filename = filename

    def addToTreeBuilder(self, tb):
        """Adds itself to a xml.etree.TreeBuilder instance.

        The element name is download-configuration.
        """
        tb.start(self.XML_TAG)

        # URL
        tb.start('url')
        tb.data(self.mediaObject.url)
        tb.end('url')

        # Media format
        self.mediaFormat.addToTreeBuilder(tb)

        # Filename
        tb.start('filename')
        tb.data(self.filename)
        tb.end('filename')

        # End download configuration
        tb.end(self.XML_TAG)

    @staticmethod
    def fromXMLElement(xmlElem):
        """Initializes an instance from a DOM element."""
        cn = xmlElem.childNodes

        mediaObject = None
        filename = None
        mediaFormat = None
        
        for c in cn:
            if c.nodeType != MD.Node.ELEMENT_NODE:
                continue
            if c.tagName == 'url':
                mediaObject = MediaObject(c.firstChild.nodeValue)
            elif c.tagName == 'filename':
                filename = c.firstChild.nodeValue
            elif c.tagName == MediaFormat.XML_TAG:
                mediaFormat = MediaFormat.fromXMLElement(c)

        if None in [mediaObject, filename, mediaFormat]:
            return None

        return DownloadConfiguration(mediaObject, mediaFormat, filename)
        
