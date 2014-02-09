

class MediaFormat(object):
    XML_TAG = 'media-format'
    
    QUALITY_NONE = None
    QUALITY_BEST = 'best'
    QUALITY_WORST = 'worst'
    
    def __init__(self, formatDictionary=None):
        """Initializes a MediaFormat.

        The initializer can extract all the information from a format
        dictionary as returned by the extractAvailableFormatsFromInfo
        method from YoutubeDLEngine.

        The quality property is not extracted from the formatDictionary
        and should be set manually if wanted.
        """
        self.id = None
        self.extension = None
        self.resolution = None
        self.quality = self.QUALITY_NONE
        self.filesize = None
        self.formatNote = None

        if formatDictionary != None:
            self.id = formatDictionary.get('format_id')
            self.extension = formatDictionary.get('ext')
            self.resolution = self.__extractResolution(formatDictionary)
            self.filesize = formatDictionary.get('filesize')
            self.formatNote = formatDictionary.get('format_note')
            
    def __str__(self):
        s = "<" + str(self.id)
        if self.extension != None:
            s += ", " + str(self.extension)
        if self.resolution != None:
            s += ", " + str(self.resolution)
        if self.formatNote != None:
            s += " (" + str(self.formatNote) + ")"
        if self.quality != self.QUALITY_NONE:
            s += " (" + self.quality + ")"
        s += ">"
        return s

    def __repr__(self):
        return str(self)

    def addToTreeBuilder(self, tb):
        """Adds itself to a xml.etree.TreeBuilder instance.

        The element name is media-format.
        """
        tb.start(self.XML_TAG)

        tb.start('id')
        tb.data(str(self.id))
        tb.end('id')

        if self.extension != None:
            tb.start('extension')
            tb.data(self.extension)
            tb.end('extension')

        if self.resolution != None:
            tb.start('resolution')
            tb.data(str(self.resolution))
            tb.end('resolution')

        if self.quality != None:
            tb.start('quality')
            tb.data(str(self.quality))
            tb.end('quality')

        if self.filesize != None:
            tb.start('filesize')
            tb.data(str(self.filesize))
            tb.end('filesize')

        if self.formatNote != None:
            tb.start('format-note')
            tb.data(self.formatNote)
            tb.end('format-note')
        
        tb.end(self.XML_TAG)

    @staticmethod
    def __extractResolution(fd):
        """Returns a human readable string representing the resolution.

        fd - The format dictionary

        Code taken from YoutubeDL's format_resolution method.
        """
        if fd.get('vcodec') == 'none':
            return 'audio only'
        if fd.get('resolution') is not None:
            return fd['resolution']
        if fd.get('height') is not None:
            if fd.get('width') is not None:
                res = '%sx%s' % (fd['width'], fd['height'])
            else:
                res = '%sp' % fd['height']
        elif fd.get('width') is not None:
            res = '?x%d' % fd['width']
        else:
            res = None
        return res
        
        
