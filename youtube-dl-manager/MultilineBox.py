import curses

from Screen import Screen

class MultilineBox(Screen):
    def initialize(self):
        self.__topLine = 0
        self.selectedLine = 0
        self.title = None

        # You can set this to a function that will be called
        # when the selected line changed. The function must
        # accept the new selected index as its only argument.
        self.selectionDidChangeHandler = None
        
    # Data management
    def numberOfLines(self):
        """Returns the number of lines.

        This method should be overridden.
        """
        return 0

    def lineAtIndex(self, index):
        """Returns a string representing the line.

        This method should be overridden.
        """
        return None

    def selectLine(self, index):
        """Selects a row and redraws."""
        numLines = self.numberOfLines()
        if index >= numLines or index < 0:
            raise IndexError(index)

        self.selectedLine = index
        self.update()
        self.__notifySelectionChange()

    def getTopLine(self):
        return self.__topLine

    def __notifySelectionChange(self):
        if self.selectionDidChangeHandler == None:
            return

        self.selectionDidChangeHandler(self.selectedLine)

    # Displaying
    def drawLineAt(self, line, point, selected=False):
        """Can be overridden if special drawing is needed.

        point - (y, x) relative coordinates
        """
        nol = self.numberOfLines()
        maxWidth = self.size[1] - 2
        if self.__shouldDrawScroller(nol):
            maxWidth -= 1
        line = line[:maxWidth]
        y, x = self.abs(point[0], point[1])
        attr = curses.A_NORMAL
        if selected == True:
            attr = curses.A_BOLD
            if self.isFirstResponder():
                l = len(line)
                if l < maxWidth:
                    line += ' '*(maxWidth - l - 1)
                    if not self.__shouldDrawScroller(nol):
                        line += ' '
                attr = attr | curses.A_REVERSE

        self.addstr(y, x, line, attr)
        
    def display(self):
        self.clean()
        self.box()

        if self.title != None and len(self.title) > 0:
            y, x = self.abs(0, 3)
            a = curses.A_BOLD if self.isFirstResponder() else curses.A_NORMAL
            self.addstr(y, x, self.title, a)

        numLines = self.numberOfLines()

        self.__checkSelectedLine(numLines)

        endLine = self.__topLine + self.size[0] - 2 # not included
        endLine = min(endLine, numLines)
            
        for lineIndex in range(self.__topLine, endLine):
            y = lineIndex - self.__topLine + 1
            line = self.lineAtIndex(lineIndex)
            isSelected = lineIndex == self.selectedLine
            self.drawLineAt(line, (y, 1), isSelected)

        if self.__shouldDrawScroller(numLines):
            self.__drawScroller(numLines)

    def __checkSelectedLine(self, numLines):
        if numLines <= 1:
            self.selectedLine = 0
        elif self.selectedLine >= numLines:
            self.selectedLine = numLines - 1
        else:
            return

        self.__notifySelectionChange()

    def __shouldDrawScroller(self, numLines):
        return (self.__canScrollDown(numLines) or self.__canScrollUp())

    def __canScrollDown(self, numLines):
        endLine = self.__topLine + self.size[0] - 3 # included
        return endLine < numLines - 1

    def __canScrollUp(self):
        return self.__topLine > 0

    def __drawScroller(self, numLines):
        self.__cleanScrollArea()
        
        x = self.size[1] - 2

        y, x = self.abs(1, x)
        self.addch(y, x, "\u25B2")

        y = self.abs(self.size[0] - 2, 0)[0]
        self.addch(y, x, "\u25BC")

        endLine = self.__topLine + self.size[0] - 3 #included

        visible = endLine - self.__topLine + 1
        scrollerLen = int(visible/numLines * (visible - 2))
        if scrollerLen == 0:
            scrollerLen = 1
        
        
        y = round(self.__topLine/numLines * (visible - 2))
        y = y + 2
        if y + scrollerLen - 1 > self.size[0] - 3 or endLine == numLines - 1:
            y = self.size[0] - 2 - scrollerLen

        y = self.abs(y, 0)[0]
        for i in range(0, scrollerLen):
            self.addch(y+i, x, curses.ACS_VLINE)

    def __cleanScrollArea(self):
        x = self.size[1] - 2
        y, x = self.abs(1, x)
        for i in range(0, self.size[0]-2):
            self.addch(y, x, ' ')
        

    # Events
    def acceptsFirstResponder(self):
        return True
    
    def respondsTo(self, key):
        numLines = self.numberOfLines()
        if key == curses.KEY_DOWN:
            return numLines > self.selectedLine + 1
        elif key == curses.KEY_UP:
            return self.selectedLine - 1 >= 0
        elif key == curses.KEY_NPAGE:
            return numLines > self.selectedLine + 1
        elif key == curses.KEY_PPAGE:
            return self.selectedLine - 1 >= 0
        return False

    def handleEvent(self, key):
        newLine = -1
        if key == curses.KEY_DOWN:
            newLine = self.selectedLine + 1
        elif key == curses.KEY_UP:
            newLine = self.selectedLine - 1
            
        elif key == curses.KEY_NPAGE:
            visible = self.size[0] - 2
            numLines = self.numberOfLines()
            newLine = self.selectedLine + visible
            if newLine > numLines - 1:
                newLine = numLines - 1
        elif key == curses.KEY_PPAGE:
            visible = self.size[0] - 2
            newLine = self.selectedLine - visible
            if newLine < 0:
                newLine = 0

        endLine = self.__topLine + self.size[0] - 2
        if newLine < self.__topLine:
            self.__topLine = newLine
        if endLine <= newLine:
            self.__topLine = newLine - self.size[0] + 3

        self.selectLine(newLine)

        
    

    
