import sys
import urllib.request

from Screen import Screen
from Button import Button
from MessageAlert import MessageAlert

from SourceCodeManager import SourceCodeManager
from SourceCodeManager import VersionExtractionError

class InitializationScreen(Screen):
    def __init__(self, preferences, doneHandler, *args, **kwargs):
        """Screen that executes ands hows the initialization process.

        preferences - An initialized Preference instance
        doneHandler - This is called when the initialization process is
            finished and the app's main screen should be displayed. The
            callable should not accept any argument.
        """
        self.preferences = preferences
        self.doneHandler = doneHandler

        super(InitializationScreen, self).__init__(*args, **kwargs)

    def initialize(self):
        self.__pendingAction = self.__initializeApplication

        self.initMessage = "Initializing the application"

    # Drawing
    def display(self):
        self.size = self.stdscr.getmaxyx()

        self.clear()
        self.box()

        self.__drawInitMessage()
        self.refresh()

        if self.__pendingAction != None:
            a = self.__pendingAction
            self.__pendingAction = None
            a()

    def __drawInitMessage(self):
        title = self.initMessage

        y = int(self.size[0] / 2)
        x = int((self.size[1] - len(title)) / 2)
        y, x = self.abs(y, x)
        self.addstr(y, x, title)

    # Initialization process
    def __initializeApplication(self):
        self.scm = SourceCodeManager(self.preferences)
        scm = self.scm

        # Check installation
        try:
            if not scm.youtubeDLIsInstalled():
                self.__youtubeDLNotInstalled()
                return
            
        except VersionExtractionError as e:
            self.__versionExtractionError(e)
            return

        # Check updates
        try:
            shouldUpdate = scm.checkForYoutubeDLUpdates()
        except urllib.request.URLError as e:
            self.__updateURLError(e)
            return

        except VersionExtractionError as e:
            self.__versionExtractionError(e)
            return

        if shouldUpdate:
            self.__updateYoutubeDL()
            return

        self.__continueApp()
            

    # Actions
    def __automaticInstall(self):
        self.endModalScreen(self.activeModalSession())
        self.initMessage = "Installing the code..."
        self.update()
        
        try:
            self.scm.downloadYoutubeDL()

        except PermissionError:
            self.__permissionInstallError()
            return

        except Exception as e:
            self.__installError(e)
            return

        self.__installSuccessfulMessage()

    def __manualInstall(self):
        title = "Manual installation guide."
        msg = "Extract the https://github.com/rg3/youtube-dl folder "
        msg+= "somewhere on your file system and point the 'sourcepath' "
        msg+= "option in the configuration file to the folder CONTAINING "
        msg+= "the youtube-dl folder. "
        msg+= "Your configuration file is located at "
        msg+= self.preferences._file

        a = MessageAlert(self, title, msg)
        b = Button("OK", self.__abort, Button.SHORTCUT_ENTER)
        a.addButton(b)

        self.beginModalScreen(a)

    def __abort(self):
        sys.exit(0)

    def __continueApp(self):
        self.scm.addYoutubeDLToPath()
        self.doneHandler()

    def __endAlert(self):
        self.endModalScreen(self.activeModalSession())

    # Errors
    def __youtubeDLNotInstalled(self):
        title = "Youtube DL source code is not installed."
        msg = "This application requires source code from "
        msg+= "https://github.com/rg3/youtube-dl. You can install the code "
        msg+= "manually or install it automatically."
        
        a = MessageAlert(self, title, msg)
        b = Button("Automatically", self.__automaticInstall, Button.SHORTCUT_ENTER)
        a.addButton(b)
        b = Button("Manually", self.__manualInstall, 'm')
        a.addButton(b)

        self.beginModalScreen(a)

    def __updateYoutubeDL(self):
        title = "An update of the Youtube DL source code is available."
        msg = "You can install the application's backend automatically or "
        msg+= "manually, or you can continue to use the current version."

        
        a = MessageAlert(self, title, msg)
        b = Button("Automatically", self.__automaticInstall, Button.SHORTCUT_ENTER)
        a.addButton(b)
        b = Button("Manually", self.__manualInstall, 'm')
        a.addButton(b)
        b = Button("Continue", self.__continueApp, 'c')
        a.addButton(b)

        self.beginModalScreen(a)
        
    def __updateURLError(self, e):
        title = "Could not check for newer Youtube DL versions."
        msg = str(e)
        a = MessageAlert(self, title, msg)
        b = Button("Continue", self.__endAlert, Button.SHORTCUT_ENTER)
        a.addButton(b)
        b = Button("Abort", self.__abort, 'a')
        a.addButton(b)

        self.beginModalScreen(a)
        
    def __versionExtractionError(self, e):
        title = "Could not check for newer Youtube DL versions."
        msg = "Could not extract the version of the installed or new "
        msg += "source code."
        a = MessageAlert(self, title, msg)
        b = Button("Continue", self.__endAlert, Button.SHORTCUT_ENTER)
        a.addButton(b)
        b = Button("Abort", self.__abort, 'a')
        a.addButton(b)

        self.beginModalScreen(a)

    def __permissionInstallError(self):
        title = "Installation failed."
        msg = "Could not install the Youtube DL code because the file "
        msg+= "system could not be accessed. You can try again as root "
        msg+= "or change the installation directory in the configuration "
        msg+= "file."

        a = MessageAlert(self, title, msg)
        b = Button("Abort", self.__abort, 'a')
        a.addButton(b)

        self.beginModalScreen(a)

    def __installError(self, e):
        title = "Installation failed."
        msg = "An error occurred while installing the Youtube DL source code: "
        msg+= str(e)

        a = MessageAlert(self, title, msg)
        b = Button("Abort", self.__abort, 'a')
        a.addButton(b)

        self.beginModalScreen(a)

    def __installSuccessfulMessage(self):
        title = "Installation successful."
        msg = "The code has been installed. Please restart the application."

        a = MessageAlert(self, title, msg)
        b = Button("OK", self.__abort, Button.SHORTCUT_ENTER)
        a.addButton(b)

        self.beginModalScreen(a)

    


        
