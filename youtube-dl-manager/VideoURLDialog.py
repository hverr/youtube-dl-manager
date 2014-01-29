
from Alert import Alert

from TextField import TextField
from Button import Button

class VideoURLDialog(Alert):
    CONTENT_HEIGHT = 4

    def initialize(self):
        super(VideoURLDialog, self).initialize()

        self.textField = TextField(self, (3, 2))
        self.addChild(self.textField)

        self.addButton(Button("OK", self.handleOK, Button.SHORTCUT_ENTER))
        self.addButton(Button("Cancel", self.handleCancel, 'c'))

    # Drawing
    def layout(self):
        super(VideoURLDialog, self).layout()

        self.textField.size = (1, self.size[1] - 4)

    def display(self):
        super(VideoURLDialog, self).display()

        y, x = self.abs(1, 1)
        self.addstr(y, x, "Video URL or YouTube hash:")

    # Events
    def handleOK(self):
        pass

    def handleCancel(self):
        pass
