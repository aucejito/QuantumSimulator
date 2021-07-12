from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel, QMainWindow, QPushButton,
QLineEdit, QComboBox, QGroupBox, QTableView, QHeaderView, QHBoxLayout,
QFormLayout, QVBoxLayout, QDialog, QFileDialog, QAction)
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class QbitLine(QFrame):
    def __init__(self, *args, **kwargs):
        QFrame.__init__(self, *args, **kwargs)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.pos()
        text = event.mimeData().text()
        self.setText(text)
        event.acceptProposedAction()