import curses

from MultilineBox import MultilineBox

from DownloadConfiguration import DownloadConfiguration
from MediaObject import MediaObject

class QueueBox(MultilineBox):
    def initialize(self):
        super(QueueBox, self).initialize()
        self.downloadConfigurations = []

    def numberOfLines(self):
        return len(self.downloadConfigurations)

    def lineAtIndex(self, index):
        mfl = self.__maximumFilenameLength()

        mul = self.size[1] - mfl - 3

        url = self.__URLAtIndex(index, mul)
        fn = self.__filenameAtIndex(index, mfl)

        return url + ' '*(self.size[1] - mfl - len(url) - 2) + fn

    def display(self):
        super(QueueBox, self).display()

        x = self.size[1] - self.__maximumFilenameLength() - 2
        y, x = self.abs(1, x)
        for i in range(0, self.size[0] - 2):
            attr = curses.A_NORMAL
            selected = self.selectedLine - self.getTopLine() == i
            selected = selected and len(self.downloadConfigurations) != 0
            if selected and self.isFirstResponder():
                attr = attr | curses.A_REVERSE
            self.addch(y + i, x, curses.ACS_VLINE, attr)
        

    def __maximumFilenameLength(self):
        s = 0
        for dc in self.downloadConfigurations:
            l = len(dc.filename)
            if l > s:
                s = l

        if s < 10:
            s = 10
        if int(self.size[1] / 2 - 1) < s:
            s = int(self.size[1] / 2 - 1)
        return s

    def __URLAtIndex(self, index, maxWidth):
        dc = self.downloadConfigurations[index]
        s = dc.mediaObject.url
        sl = len(s)
        if sl <= maxWidth:
            return s

        s = "..." + s[-maxWidth + 3:]
        return s

    def __filenameAtIndex(self, index, maxWidth):
        dc = self.downloadConfigurations[index]
        s = dc.filename
        sl = len(s)
        if sl <= maxWidth:
            return s
        s = s[:maxWidth - 3] + "..."
        return s
