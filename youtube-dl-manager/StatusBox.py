import curses

from Screen import Screen

class StatusBox(Screen):
    STATUS_IDLE = 'idle'
    STATUS_DOWNLOADING = 'downloading'
    
    def initialize(self):
        self.status = self.STATUS_IDLE

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
            self.addstr(y, x, "downloading")
        else:
            raise Exception("Invalid status")

    # Events
    def acceptsFirstResponder(self):
        return False
