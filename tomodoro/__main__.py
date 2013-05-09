import platform
import sys

if platform.system() == 'Linux':
    sys.path.append('/usr/lib/python2.7/dist-packages/')

from PyQt4 import QtGui

from .tomodoro import TomodoroApp


app = QtGui.QApplication(sys.argv)
TomodoroApp()
sys.exit(app.exec_())