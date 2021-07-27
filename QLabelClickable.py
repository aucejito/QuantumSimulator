from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow, QPushButton,
QLineEdit, QComboBox, QGroupBox, QTableView, QHeaderView, QHBoxLayout,
QFormLayout, QVBoxLayout, QDialog, QFileDialog, QAction)
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class QLabelClickable(QLabel):
    
    clicked = pyqtSignal()

    def __init__(self, *args):
        QLabel.__init__(self, *args)
        
    def mouseReleaseEvent(self, ev):
        self.clicked.emit()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event : QtGui.QMouseEvent):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setImageData(self.pixmap().toImage())
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)