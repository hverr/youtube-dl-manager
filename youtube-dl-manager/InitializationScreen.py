import time

from Screen import Screen

from SourceCodeManager import SourceCodeManager

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
        title = "Initializing the application"
        try:
            title += " (" + str(self.seconds) + ")..."
        except:
            pass
            
        y = int(self.size[0] / 2)
        x = int((self.size[1] - len(title)) / 2)
        y, x = self.abs(y, x)
        self.addstr(y, x, title)

    # Initialization process
    def __initializeApplication(self):
        for self.seconds in range(5, 0, -1):
            self.update()
            time.sleep(1)

        self.doneHandler()
        
