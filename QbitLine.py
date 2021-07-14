from Circuit import Circuit
from QLabelClickable import QLabelClickable
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class QbitLine(QFrame):
    grid = QHBoxLayout()
    
    def __init__(self, *args, **kwargs):
        QFrame.__init__(self, *args, **kwargs)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        global grid
        grid = QHBoxLayout(self)
        grid.setContentsMargins(0,0,0,0)
        #grid.addWidget(QWidget(self).setStyleSheet("background-color: yellow"))
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def dropEvent(self, event:QDropEvent):
        pos = event.pos()
        event.acceptProposedAction()
        if event.mimeData().hasImage():
            newGate = QLabelClickable()
            newGate.setPixmap(QPixmap.fromImage(QImage(event.mimeData().imageData())))
            newGate.setScaledContents(True)
            newGate.setMaximumSize(50,50)
            newGate.setAlignment(Qt.AlignCenter)
            grid.addWidget(newGate)

            currentCircuit = Circuit()
            currentCircuit.addGate(event.mimeData().data)

            