from PyQt4.QtCore import QObject


class Timer(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.timers = {}

    def timerEvent(self, event):
        f = self.timers.pop(event.timerId())
        self.killTimer(event.timerId())
        f()

    def add_delayed_call(self, time, f):
        timer_id = self.startTimer(time)
        self.timers[timer_id] = f

    def clear_pending_calls(self):
        while self.timers:
            timer_id, f = self.timers.popitem()
            self.killTimer(timer_id)