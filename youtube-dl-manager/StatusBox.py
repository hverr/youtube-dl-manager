import curses

from Screen import Screen

class StatusBox(Screen):
    STATUS_IDLE = 'idle'
    STATUS_DOWNLOADING = 'downloading'
    
    def initialize(self):
        self.status = self.STATUS_IDLE
        self.currentObject = None # Set this to a string

    # Drawing
    def display(self):
        self.clean()
        self.box()

        self.__drawTitle()

    def __drawTitle(self):
        y, x = self.abs(0, 3)
        s = "Status: "
        self.addstr(y, x, s, curses.A_BOLD)
        x += len(s)
        if self.status == self.STATUS_IDLE:
            self.addstr(y, x, "idle")
        elif self.status == self.STATUS_DOWNLOADING:
            d = "downloading"
            self.addstr(y, x, d)
            if self.currentObject != None:
                self.addstr(y, x + len(d), " '" + self.currentObject + "'")
        else:
            raise Exception("Invalid status")

    # Events
    def acceptsFirstResponder(self):
        return False
