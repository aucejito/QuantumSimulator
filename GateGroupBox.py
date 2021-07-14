from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class GateGroupBox(QGroupBox):

    def __init__(self, *args, **kwargs):
        QGroupBox.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)

    def dropEvent(self, event: QtGui.QDropEvent):
        event.acceptProposedAction()