import curses

from Screen import Screen

class MainScreen(Screen):
    # Drawing
    def display(self):
        self.__drawBox()

    def __drawBox(self):
        self.box()

        title = "Youtube DL Manager"
        y, x = self.absoluteCoordinates(0,3)
        self.addstr(y, x, title, curses.A_BOLD)
    
