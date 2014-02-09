
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
