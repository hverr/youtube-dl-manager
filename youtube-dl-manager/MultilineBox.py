import curses

from Screen import Screen

class MultilineBox(Screen):
    def initialize(self):
        self.__topLine = 0
        self.selectedLine = 0
        
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

    # Displaying
    def drawLineAt(self, line, point, selected=False):
        """Can be overridden if special drawing is needed.

        point - (y, x) relative coordinates
        """
        maxWidth = self.size[1] - 2
        line = line[:maxWidth]
        y, x = self.abs(point[0], point[1])
        attr = curses.A_NORMAL
        if selected == True:
            attr = curses.A_REVERSE
        self.addstr(y, x, line, attr)
        
    def display(self):
        self.box()

        numLines = self.numberOfLines()

        endLine = self.__topLine + self.size[0] - 2 # not included
        endLine = min(endLine, numLines)
        for lineIndex in range(self.__topLine, endLine):
            y = lineIndex - self.__topLine + 1
            line = self.lineAtIndex(lineIndex)
            self.drawLineAt(line, (y, 1), lineIndex == self.selectedLine)

        
    

    
