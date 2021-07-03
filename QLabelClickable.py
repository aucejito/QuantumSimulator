from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow, QPushButton,
QLineEdit, QComboBox, QGroupBox, QTableView, QHeaderView, QHBoxLayout,
QFormLayout, QVBoxLayout, QDialog, QFileDialog, QAction)
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtCore import QLine, QSize, Qt, pyqtSignal

class QLabelClickable(QLabel):
    
    clicked = pyqtSignal()

    def __init__(self, *args):
        QLabel.__init__(self, *args)

    def mouseReleaseEvent(self, ev):
        self.clicked.emit()