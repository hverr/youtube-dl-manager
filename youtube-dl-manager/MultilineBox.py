from Screen import Screen

class MultilineBox(Screen):
    def initialize(self):
        self.__topLine = 0
        self.selectedRow = 0
        
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

    def selectRow(self, index):
        """Selects a row and redraws."""
        numLines = self.numberOfLines()
        if index >= numLines or index < 0:
            raise IndexError(index)

        self.selectedRow = index
        self.update()

    # Displaying
    def drawLineAt(self, line, point):
        """Can be overridden if special drawing is needed.

        point - (y, x) relative coordinates
        """
        maxWidth = self.size[1] - 2
        line = line[:maxWidth]
        y, x = self.abs(point[0], point[1])
        self.addstr(y, x, line)
        
    def display(self):
        self.box()

        numLines = self.numberOfLines()

        endLine = self.__topLine + self.size[0] - 2 # not included
        endLine = min(endLine, numLines)
        for lineIndex in range(self.__topLine, endLine):
            y = lineIndex - self.__topLine + 1
            line = self.lineAtIndex(lineIndex)
            self.drawLineAt(line, (y, 1))

        
    

    
