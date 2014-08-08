import os
from datetime import timedelta, datetime, date, time
from gtk.gdk import pixbuf_new_from_file

from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.phonon import Phonon
import pynotify

from . import constants
from .timer import Timer


class TomodoroApp(QtGui.QWidget):

    def __init__(self):
        self.tick = 1000
        super(TomodoroApp, self).__init__()

        self.selected_time = self.remaining = constants.POMODORO
        self.timer = Timer(self)
        self.init_widgets()
        self.init_ui()
        self.image = pixbuf_new_from_file(os.path.join(os.path.dirname(__file__), 'icon.png'))

        self.phonon_output = Phonon.AudioOutput(Phonon.MusicCategory)
        self.phonon_media = Phonon.MediaObject()
        Phonon.createPath(self.phonon_media, self.phonon_output)
        self.phonon_media.setCurrentSource(
            Phonon.MediaSource(
                os.path.abspath(
                    os.path.join(os.path.dirname(__file__), 'buzzer.wav')
                    )
                )
            )

        pynotify.init('Tomodoro')

    def notify(self, title, message, urgency=pynotify.URGENCY_NORMAL):
        n = pynotify.Notification(title, message, "dialog-info")
        n.set_urgency(pynotify.URGENCY_NORMAL)
        n.set_timeout(pynotify.EXPIRES_DEFAULT)
        n.set_icon_from_pixbuf(self.image)
        n.show()
        self.phonon_media.play()
        return True

    def get_formatted_time(self, time):
        return str(time)[3:]

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def select_time(self, time):
        self.selected_time = time
        self.reset()
        self.start()

    def reset(self):
        self.stop()
        self.remaining = self.selected_time
        self.clock.setText(self.get_formatted_time(self.remaining))

    def start(self):
        self.timer.add_delayed_call(self.tick, self.countdown)

    def stop(self):
        self.timer.clear_pending_calls()

    def init_widgets(self):
        # Widgets
        self.clock = QtGui.QLabel(self.get_formatted_time(self.remaining))
        self.clock.resize(self.clock.sizeHint())
        self.clock.setFont(QtGui.QFont('SansSerif', 25))
        self.clock.setAlignment(Qt.AlignCenter)

        pomodoro_button = QtGui.QPushButton('Pomodoro')
        pomodoro_button.setToolTip('Work work')
        pomodoro_button.resize(pomodoro_button.sizeHint())
        pomodoro_button.clicked.connect(lambda: self.select_time(constants.POMODORO))

        short_break_button = QtGui.QPushButton('Short Break')
        short_break_button.setToolTip('05:00 minutes break')
        short_break_button.resize(short_break_button.sizeHint())
        short_break_button.clicked.connect(lambda: self.select_time(constants.SHORT_BREAK))

        long_break_button = QtGui.QPushButton('Long Break')
        long_break_button.setToolTip('15:00 minutes break')
        long_break_button.resize(long_break_button.sizeHint())
        long_break_button.clicked.connect(lambda: self.select_time(constants.LONG_BREAK))

        start_button = QtGui.QPushButton('Start')
        start_button.setToolTip('Work the shit out')
        start_button.resize(start_button.sizeHint())
        start_button.clicked.connect(self.start)

        reset_button = QtGui.QPushButton('Reset')
        reset_button.setToolTip('Reset countdown')
        reset_button.resize(reset_button.sizeHint())
        reset_button.clicked.connect(self.reset)

        # boxes
        control_box = QtGui.QHBoxLayout()
        control_box.setAlignment(Qt.AlignCenter)
        control_box.addWidget(start_button)
        control_box.addWidget(reset_button)

        time_box = QtGui.QHBoxLayout()
        time_box.setAlignment(Qt.AlignCenter)
        time_box.addWidget(pomodoro_button)
        time_box.addWidget(long_break_button)
        time_box.addWidget(short_break_button)

        vbox = QtGui.QVBoxLayout()
        vbox.setAlignment(Qt.AlignHCenter)
        vbox.addLayout(time_box)
        vbox.addWidget(self.clock)
        vbox.addLayout(control_box)
        vbox.geometry()

        self.setLayout(vbox)

    def init_ui(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Tomodoro')
        self.center()
        self.show()

    def countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= time(0, 0, 0):
            self.notify('Wololo!', 'Time\'s up!')
            self.clock.setText('Time\'s up!')
        else:
            self.remaining = (datetime.combine(date.today(), self.remaining) - timedelta(seconds=1)).time()
            self.clock.setText(self.get_formatted_time(self.remaining))
            self.start()
