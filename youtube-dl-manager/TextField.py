import curses
import curses.ascii

from Screen import Screen

class TextField(Screen):
    def initialize(self):
        self.__value = ""
        self.__firstVisibleCharacter = 0

        # Relative to the first visible character
        # This means values from 0 to width - 1
        self.__cursorPosition = 0

    # Value
    def getValue(self):
        return self.__value

    def setValue(self, v):
        self.__value = str(v)
        strLen = len(self.__value)
        if strLen >= self.size[1]:
            self.__firstVisibleCharacter = strLen - self.size[1] + 1
            self.__cursorPosition = self.size[1] - 1
        else:               
            self.__firstVisibleCharacter = 0
            self.__cursorPosition = strLen
        

    # Displaying
    def __getVisibleString(self):
        maxWidth = self.size[1]

        if self.isFirstResponder():
            fc = self.__firstVisibleCharacter
            lc = fc + maxWidth
            return self.__value[fc:lc]

        return self.__value[:maxWidth]
    
    def display(self):
        self.clean()

        maxWidth = self.size[1]
        s = self.__getVisibleString()
        y, x = self.abs(0,0)

        attr = curses.A_UNDERLINE
        if self.isFirstResponder():
            attr = attr | curses.A_BOLD
        self.addstr(y, x, s, attr)
        strLen = len(s)
        for i in range(strLen, maxWidth):
            self.addch(y, x + i, ' ', curses.A_UNDERLINE)

        y, x = self.abs(0, self.__cursorPosition)
        self.move(y, x)

    # Events
    def makeFirstResponder(self, *args, **kwargs):
        curses.curs_set(1)
        super(TextField, self).makeFirstResponder(*args, **kwargs)

    def resignFirstResponder(self, *args, **kwargs):
        curses.curs_set(0)
        super(TextField, self).resignFirstResponder(*args, **kwargs)

    def respondsTo(self, key):
        allowed = [curses.KEY_LEFT, curses.KEY_RIGHT,
                   curses.KEY_PPAGE, curses.KEY_NPAGE,
                   curses.KEY_HOME, curses.KEY_END,
                   curses.KEY_DL, curses.ascii.DEL]
        if key in allowed:
            return True
        
        return curses.ascii.isprint(chr(key))

    def handleEvent(self, key):
        if key == curses.KEY_RIGHT:
            self.__moveRight()
        elif key == curses.KEY_LEFT:
            self.__moveLeft()
        elif key == curses.KEY_PPAGE or key == curses.KEY_HOME:
            self.__moveToFirst()
        elif key == curses.KEY_NPAGE or key == curses.KEY_END:
            self.__moveToLast()
        elif key == curses.KEY_DL:
            self.setValue("")
            self.update()
        elif key == curses.ascii.DEL:
            self.__deleteChar()
        elif curses.ascii.isprint(chr(key)):
            self.__insertChar(chr(key))

    def __moveLeft(self):
        if self.__cursorPosition == 1:
            if self.__firstVisibleCharacter > 0:
                self.__firstVisibleCharacter -= 1
            elif self.__firstVisibleCharacter == 0:
                self.__cursorPosition = 0
        elif self.__cursorPosition > 1:
            self.__cursorPosition -= 1

        self.update()

    def __moveRight(self):
        lc = self.__firstVisibleCharacter + self.size[1] - 1
        if self.__cursorPosition == self.size[1] - 1:
            if lc < len(self.__value):
                self.__firstVisibleCharacter += 1
        else:
            if self.__cursorPosition < len(self.__value):
                self.__cursorPosition += 1

        self.update()


    def __moveToFirst(self):
        self.__firstVisibleCharacter = 0
        self.__cursorPosition = 0
        self.update()

    def __moveToLast(self):
        strLen = len(self.__value)
        if strLen >= self.size[1]:
            self.__firstVisibleCharacter = strLen - self.size[1] + 1
            self.__cursorPosition = self.size[1] - 1
        else:
            self.__firstVisibleCharacter = 0
            self.__cursorPosition = strLen
        self.update()

    def __deleteChar(self):
        toDelete = self.__firstVisibleCharacter + self.__cursorPosition - 1
        if toDelete < 0:
            return
        
        new = self.__value[:toDelete] + self.__value[toDelete+1:]
        self.__value = new
        
        if self.__cursorPosition == self.size[1] - 1:
            if self.__firstVisibleCharacter > 0:
                self.__firstVisibleCharacter -= 1
            else:
                self.__cursorPosition -= 1
            self.update()
        else:
            self.__moveLeft()

    def __insertChar(self, c):
        pos = self.__firstVisibleCharacter + self.__cursorPosition
        new = self.__value[:pos] + str(c) + self.__value[pos:]
        self.__value = new
        self.__moveRight()
        

        
