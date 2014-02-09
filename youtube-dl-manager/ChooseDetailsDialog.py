import string
import unicodedata

from Alert import Alert

from TextField import TextField
from Button import Button
from MessageAlert import MessageAlert
from MultilineBox import MultilineBox

from MediaFormat import MediaFormat
from DownloadConfiguration import DownloadConfiguration

class ChooseDetailsDialog(Alert):
    CONTENT_HEIGHT = 12

    def __init__(self, parent, mediaObject, info):
        """Initializes the dialog.

        mediaObject - A MediaObject instance
        info - The dictionary from the mediaObject as returned by
               getMediaInformation.
        """
        self.mediaObject = mediaObject
        self.mediaInformation = info
        super(ChooseDetailsDialog, self).__init__(parent)

    def initialize(self):
        super(ChooseDetailsDialog, self).initialize()

        self.filenameField = TextField(self, (2,2), (1,1))
        self.addChild(self.filenameField)
        self.filenameField.setValue(self.__extractDefaultFilename())

        self.formatBox = FormatBox(self, (4, 2))
        self.formatBox.formats = self.__extractFormats()
        self.addChild(self.formatBox)

        self.addButton(Button("OK", self.handleOK, Button.SHORTCUT_ENTER))
        self.addButton(Button("Cancel", self.handleCancel, 'c'))

        # This callable is called to notify we are done and have
        # successfully configured a DownloadConfiguration instance.
        # The function should accept the DownloadConfiguration instance
        # as its only argument and should end the modal session.
        self.doneHandler = None

    def __extractFormats(self):
        mo = self.mediaObject
        info = self.mediaInformation
        f = mo.extractAvailableFormatsFromInfo(info)
        f.reverse()
        for i in range(1, len(f)):
            mf = f[i]
            if mf.quality == MediaFormat.QUALITY_BEST:
                del f[i]
                f.insert(0, mf)
                break

        return f

    def __extractDefaultFilename(self):
        s = self.mediaInformation.get('title', 'Untitled')
        if type(s) != str:
            return 'Untitled'
        return self.__normalizeFilename(s)

    def __normalizeFilename(self, fn):
        # From http://stackoverflow.com/a/517974/262660
        new = unicodedata.normalize('NFKD', fn)
        new = new.encode('ASCII', 'ignore').decode('utf-8')

        # Only allowed characters
        allowed = "-_.() %s%s" % (string.ascii_letters, string.digits)
        new = ''.join(c for c in new if c in allowed)
        return new
        
            

    # Drawing
    def layout(self):
        super(ChooseDetailsDialog, self).layout()

        # Filename
        w = self.size[1] - 4
        if self.filenameField.size != (1, w):
            self.filenameField.size = (1, w)
            self.filenameField.setValue(self.filenameField.getValue())

        # Format Box
        h = self.CONTENT_HEIGHT - 3
        self.formatBox.size = (h, w)

    def display(self):
        super(ChooseDetailsDialog, self).display()

        y, x = self.abs(1, 1)
        self.addstr(y, x, "Filename:")

        y += 2
        self.addstr(y, x, "Format:")

    # Events
    def handleOK(self):
        fn = self.__getFinalFilename()
        if fn == None:
            t = "Invalid filename."
            msg = "Please choose a valid filename. The file must "
            msg+= "be in the current directory and cannot contain "
            msg+= "any illegal characters."
            alert = MessageAlert(self, t, msg)
            b = Button("OK", self.__handleErrorOK, Button.SHORTCUT_ENTER)
            alert.addButton(b)
            self.beginModalScreen(alert)
            return

        mo = self.mediaObject
        mf = self.formatBox.selectedFormat()
        dc = DownloadConfiguration(mo, mf, fn)
        try:
            self.doneHandler(dc)
        except Exception as e:
            self.__handleException(e)

    def __handleException(self, exception):
        t = "An error occurred."
        m = str(exception)
        alert = MessageAlert(self, t, m)

        b = Button("OK", self.__handleErrorOK, Button.SHORTCUT_ENTER)
        alert.addButton(b)
                        
        self.beginModalScreen(alert)

    def __handleErrorOK(self):
        self.endModalScreen(self.activeModalSession())
        self.makeChildFirstResponder(self.filenameField)
    
    def handleCancel(self):
        self.parent.endModalScreen(self)

    def __getFinalFilename(self):
        selFormat = self.formatBox.selectedFormat()

        fn = self.filenameField.getValue()
        if '/' in fn or '\\' in fn:
            return None
        
        fn = self.__normalizeFilename(fn)
        
        if fn in ['', '.', '..']:
            return None

        ext = selFormat.extension
        if ext != None and len(ext) != 0:
            fn += '.' + ext
        return fn

class FormatBox(MultilineBox):
    def initialize(self):
        super(FormatBox, self).initialize()
        self.formats = [] # MediaFormat instances

    def numberOfLines(self):
        return len(self.formats)

    def lineAtIndex(self, index):
        return str(self.formats[index])

    def selectedFormat(self):
        return self.formats[self.selectedLine]

        
