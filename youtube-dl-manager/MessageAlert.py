import textwrap
import curses

from Alert import Alert

class MessageAlert(Alert):
    def __init__(self, parent, title, msg):
        super(MessageAlert, self).__init__(parent)

        self.title = title
        self.message = msg
        
    def initialize(self):
        super(MessageAlert, self).initialize()

    # Drawing
    def layout(self):
        super(MessageAlert, self).layout()

        width = self.size[1] - 2
        numLines = 0

        if self.title != None:
            wrappedTitle = textwrap.wrap(self.title, width)
            numLines += len(wrappedTitle)
            numLines += 1

        if self.message != None:
            wrappedMsg = textwrap.wrap(self.message, width - 1)
            numLines += len(wrappedMsg)
            numLines += 1

        self.CONTENT_HEIGHT = numLines

        super(MessageAlert, self).layout()

    def display(self):
        super(MessageAlert, self).display()
        width = self.size[1] - 2

        usedLines = self.__drawTitle(width)
        self.__drawMessage(usedLines, width)

    def __drawTitle(self, width):
        if self.title == None:
            return 0

        lines = textwrap.wrap(self.title, width)
        y, x = self.abs(1, 1)
        for i in range(0, len(lines)):
            self.addstr(y + i, x, lines[i], curses.A_BOLD)

        return len(lines) + 1

    def __drawMessage(self, relStartY, width):
        if self.message == None:
            return

        lines = textwrap.wrap(self.message, width - 1)
        y, x = self.abs(1 + relStartY, 2)
        for i in range(0, len(lines)):
            self.addstr(y + i, x, lines[i])
            
        
        

        
        
