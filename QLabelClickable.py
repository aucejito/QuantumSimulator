from Util import Util
from enum import Enum
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow, QPushButton,
QLineEdit, QComboBox, QGroupBox, QTableView, QHeaderView, QHBoxLayout,
QFormLayout, QVBoxLayout, QDialog, QFileDialog, QAction)
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class GateType(Enum):
    single = 'single'
    double = 'double'
    triple = 'triple'

class QLabelClickable(QLabel):
    
    gate = 'gate1'
    gateType : GateType = None
    position = {'qbit':'-1', 'column':'-1'}
    qbit = -1
    clicked = pyqtSignal()

    def __init__(self, *args):
        QLabel.__init__(self, *args)
        self.setMaximumSize(50,50)
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignCenter)
        
    def mouseReleaseEvent(self):
        self.clicked.emit()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event : QtGui.QMouseEvent):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        
        pixmap = QPixmap(self.size())   
        drag = QDrag(self)
        mimedata = QMimeData()
        print(type(self.pixmap()))
        print(type(None))
        if(type(self.pixmap()) != type(None)):
            mimedata.setImageData(self.pixmap().toImage())
        drag.setMimeData(mimedata)
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)
    
        
