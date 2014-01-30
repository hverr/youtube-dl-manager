
from Alert import Alert

from TextField import TextField
from Button import Button
from MessageAlert import MessageAlert
from ChooseDetailsDialog import ChooseDetailsDialog

from MediaObject import (MediaObject, UnsupportedURLError)

class VideoURLDialog(Alert):
    CONTENT_HEIGHT = 6

    def initialize(self):
        super(VideoURLDialog, self).initialize()

        self.textField = TextField(self, (3, 2))
        self.addChild(self.textField)

        self.__progressMessage = None

        self.addButton(Button("OK", self.handleOK, Button.SHORTCUT_ENTER))
        self.addButton(Button("Cancel", self.handleCancel, 'c'))

    # Drawing
    def layout(self):
        super(VideoURLDialog, self).layout()

        self.textField.size = (1, self.size[1] - 4)

    def display(self):
        super(VideoURLDialog, self).display()

        y, x = self.abs(1, 1)
        self.addstr(y, x, "Video URL or YouTube hash:")

        self.__drawProgressMessage()

    def __drawProgressMessage(self):
        y, x = self.abs(5, 1)
        w = (self.size[1] - 4)
        self.addstr(y, x, ' '*w)
        
        if self.__progressMessage != None:
            y, x = self.abs(5, 1)
            self.addstr(y, x, self.__progressMessage[:w])
                    
        self.refresh()

    # Events
    def handleOK(self):
        self.__handleURL(self.textField.getValue())
        

    def handleCancel(self):
        self.parent.endModalScreen(self)

    def __handleURL(self, url):
        invalidURL = False
        try:
            mo = MediaObject(url)
            mo.delegate = self
            info = mo.getMediaInformation()

            if info == None:
                raise UnsupportedURLError(url)
            
        except UnsupportedURLError:
            invalidURL = True
        finally:
            self.__progressMessage = None
            self.update()

        if invalidURL == True:
            t = "Could not extract information."
            m = "Invalid URL or video hash."
            self.__handleError(t, m)
            return

        # Choose details
        self.chooseDetailsDialog = ChooseDetailsDialog(self, mo, info)
        self.chooseDetailsDialog.doneHandler = self.__handleChooseDetailsDone
        self.beginModalScreen(self.chooseDetailsDialog)

    def __handleChooseDetailsDone(self, dc):
        self.parent.addDownloadConfiguration(dc)
        self.endModalScreen(self.chooseDetailsDialog)
        self.chooseDetailsDialog = None
        self.parent.endModalScreen(self)

    def __handleError(self, title, msg):
        self.errorAlert = MessageAlert(self.parent, title, msg)

        b = Button("OK", self.__handleErrorOK, Button.SHORTCUT_ENTER)
        self.errorAlert.addButton(b)
        
        self.parent.beginModalScreen(self.errorAlert)

    def __handleErrorOK(self):
        self.parent.endModalScreen(self.errorAlert)

    # Media Object delegate
    def mediaObjectMessage(self, msg):
        self.__progressMessage = msg
        self.__drawProgressMessage()

    def mediaObjectError(self, msg):
        self.__progressMessage = msg
        self.__drawProgressMessage()
        
            
        
