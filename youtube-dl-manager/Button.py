import curses
import curses.ascii

from Screen import Screen

class Button(Screen):
    SHORTCUT_ENTER = chr(curses.ascii.LF)
    SHORTCUT_ENTER2 = chr(curses.ascii.CR)
    def __init__(self, title, handler, shortcut=None):
        super(Button, self).__init__(None, (0, 0))

        self.title = title
        self.handler = handler
        if shortcut != None:
            try:
                ord(shortcut)
            except TypeError:
                s = "Unsupported shortcut. Expected character but got '"
                s += str(shortcut) + "'"
        self.shortcut = shortcut

    def __repr__(self):
        return super(Button, self).__repr__() + "(<" + str(self.title) + ">)"

    # Drawing
    def neededWidth(self):
        return 2 + len(str(self.title))

    def display(self):
        s = "<" + str(self.title) + ">"
        attr = curses.A_NORMAL

        y, x = self.abs(0, 0)

        # Draw title
        if self.shortcut in [self.SHORTCUT_ENTER, self.SHORTCUT_ENTER2]:
            attr = attr | curses.A_BOLD
        if self.isFirstResponder():
            attr = attr | curses.A_REVERSE
        self.addstr(y, x, s, attr)

        # Underline shortcut
        sp = self.__shortcutPosition()
        if sp != None:
            attr = attr | curses.A_UNDERLINE
            self.addch(y, x + sp + 1, s[sp + 1], attr)

    def __shortcutPosition(self):
        if self.shortcut == None:
            return None
        i = 0
        sc = self.shortcut.lower()
        for c in str(self.title).lower():
            if c == sc:
                return i
            i += 1
        return None
