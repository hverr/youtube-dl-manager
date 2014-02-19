
from threading import RLock

class Notification(object):
    __queue = []
    __lock = RLock()
    __observers = [] # Tuples (observer, name)
    def __init__(self, name, sender=None, userInfo={}):
        """Create a notification that can be injected in the runloop.

        name - The name of the notification. Must be a string
        sender - A python object
        userInfo - A dictionary with user defined info
        """
        self.name = str(name)
        self.sender = sender
        self.userInfo = userInfo

    def __repr__(self):
        s = super(Notification, self).__repr__()
        s += " (" + self.name
        if self.sender != None:
            s += " from " + repr(self.sender)
        s += ")"
        return s

    def __str__(self):
        s = super(Notification, self).__repr__()
        s += " (" + self.name
        if self.sender != None:
            s += " from " + str(self.sender)
        s += ")"
        return s

    # Post notifications
    @staticmethod
    def post(notification):
        """Post a notification"""
        with Notification.__lock:
            Notification.__queue.append(notification)

    # Manager observers
    @staticmethod
    def addObserver(observer, notificationName):
        with Notification.__lock:
            if (observer, notificationName) in Notification.__observers:
                return
            Notification.__observers.append((observer,notificationName))

    def removeObserver(observer, notificationName=None):
        with Notification.__lock:
            if notificationName == None:
                i = 0
                while i < len(Notification.__observers):
                    if Notification.__observers[i][0] == observer:
                        del Notification.__observers[i]
                        i -= 1
                    i += 1

            else:
                try:
                    Notification.__observers.remove((observer, notificationName))
                except ValueError:
                    pass
                
            
    @staticmethod
    def nextNotification():
        """Should only be called by the main runloop manager."""
        with Notification.__lock:
            if len(Notification.__queue) == 0:
                return None
            n = Notification.__queue[0]
            del Notification.__queue[0]
            return n
        
