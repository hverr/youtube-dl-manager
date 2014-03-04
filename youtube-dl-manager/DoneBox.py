import curses

from Screen import Screen
from MultilineBox import MultilineBox

# Shared drawing code
def drawLegend(self, y):
    legend = ['[c] Clear', '[r] Retry']

    x = self.size[1] - 3
    x = self.abs(0, x)[1]
    for l in legend:
        l = ' ' + l + ' '
        x -= len(l)
        self.addstr(y, x, l)
        x -= 2

class DoneBox(MultilineBox):
    def initialize(self):
        super(DoneBox, self).initialize()

        # Set this after the initialization of the done box!
        self.downloadManager

        self.title = "Done"

    def numberOfLines(self):
        return len(self.downloadManager.done)

    def lineAtIndex(self, index):
        mfl = self.__maximumFilenameLength()

        mul = self.size[1] - mfl - 3

        url = self.__URLAtIndex(index, mul)
        fn = self.__filenameAtIndex(index, mfl)

        return url + ' '*(self.size[1] - mfl - len(url) - 2) + fn

    def display(self):
        super(DoneBox, self).display()

        x = self.size[1] - self.__maximumFilenameLength() - 2
        y, x = self.abs(1, x)
        for i in range(0, self.size[0] - 2):
            attr = curses.A_NORMAL
            selected = self.selectedLine - self.getTopLine() == i
            selected = selected and len(self.downloadManager.done) != 0
            if selected and self.isFirstResponder():
                attr = attr | curses.A_REVERSE
            self.addch(y + i, x, curses.ACS_VLINE, attr)

        self.__connectBoxes()
        self.__drawLegend()

    def __connectBoxes(self):
        y, x = self.abs(self.size[0] - 1, 0)
        self.addch(y, x, curses.ACS_LTEE)
        self.addch(y, x + self.size[1] - 1, curses.ACS_RTEE)
        

    def __maximumFilenameLength(self):
        s = 0
        for dc in self.downloadManager.done:
            l = len(dc.filename)
            if l > s:
                s = l

        if s < 10:
            s = 10
        if int(self.size[1] / 2 - 1) < s:
            s = int(self.size[1] / 2 - 1)
        return s

    def __URLAtIndex(self, index, maxWidth):
        try:
            dc = self.downloadManager.done[index]
        except IndexError: # Concurrency error emergency stop
            return ''
        s = dc.mediaObject.url
        sl = len(s)
        if sl <= maxWidth:
            return s

        s = "..." + s[-maxWidth + 3:]
        return s

    def __filenameAtIndex(self, index, maxWidth):
        try:
            dc = self.downloadManager.done[index]
        except IndexError: # Concurrency error emergency stop
            return ''
        s = dc.filename
        sl = len(s)
        if sl <= maxWidth:
            return s
        s = s[:maxWidth - 3] + "..."
        return s

    def __drawLegend(self):
        y, x = self.abs(self.size[0] - 1, 0)
        drawLegend(self, y)

class DetailsScreen(Screen):
    def __init__(self, parent, doneBox):
        """Initializes a details screen attached to the done box.

        The details screen will attach itself to the bottom of the
        done box. It should be drawn after the done box.

        You can check the size attribute to see how big in height it
        will be. The width will be calculated when the layout method
        is called and will be the same as the width of the done box.
        """
        super(DetailsScreen, self).__init__(parent, (0, 0))

        self.doneBox = doneBox
        h = self.doneBoxSelectionDidChange
        self.doneBox.selectionDidChangeHandler = h

    def initialize(self):
        self.__values = ['URL', 'Format', 'Output file']
        self.__downloadConfiguration = None
        self.size = (len(self.__values) + 2, 1)

    def layout(self):
        self.size = list(self.size)
        self.size[1] = self.doneBox.size[1]
        self.origin = list(self.doneBox.origin)
        self.origin[0] += self.doneBox.size[0] - 1

    def display(self):
        self.clean()
        self.box()
        self.__connectBoxes()
        self.__drawLegend()
        mvnl = self.__maximumValueNameLength()

        y, x = self.abs(1, 1)
        for v in self.__values:
            indent = mvnl - len(v)
            v = ' '*indent + v + ":"
            self.addstr(y, x, v)
            y += 1

        y, x = self.abs(1, mvnl + 3)
        dc = self.currentDownloadConfiguration()
        if dc == None:
            for v in self.__values:
                self.addstr(y, x, "N/A")
                y += 1

        else:
            maxLen = self.size[1] - mvnl - 4
            
            # URL
            s = dc.mediaObject.url
            s = s[:maxLen]
            self.addstr(y, x, s)

            # Format
            s = dc.mediaFormat
            s = str(s)[:maxLen]
            self.addstr(y+1, x, s)

            # Output File
            s = dc.filename
            s = s[:maxLen]
            self.addstr(y+2, x, s)
            
            

    def __connectBoxes(self):
        y, x = self.abs(0, 0)
        self.addch(y, x, curses.ACS_LTEE)
        self.addch(y, x + self.size[1] - 1, curses.ACS_RTEE)
        

    def __maximumValueNameLength(self):
        s = 0
        for v in self.__values:
            l = len(v)
            if l > s:
                s = l
        return s

    def __drawLegend(self):
        y, x = self.abs(0, 0)
        drawLegend(self, y)

    def doneBoxSelectionDidChange(self, index):
        self.update()

    def currentDownloadConfiguration(self):
        if len(self.doneBox.downloadManager.done) == 0:
            return None

        index = self.doneBox.selectedLine
        if index >= len(self.doneBox.downloadManager.done):
            return None
        try:
            return self.doneBox.downloadManager.done[index]
        except IndexError: # Concurrency emergency stop
            return None

    def acceptsFirstResponder(self):
        return False
        
