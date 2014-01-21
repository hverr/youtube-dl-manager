from MultilineBox import MultilineBox

class QueueBox(MultilineBox):
    def initialize(self):
        super(QueueBox, self).initialize()
        self.mediaObjects = []

    def numberOfLines(self):
        return 10

    def lineAtIndex(self, index):
        return "Hello World from " + str(index)
