from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class trashWidget(QWidget):

    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        vBoxDeleteGates = QVBoxLayout()
        vBoxDeleteGates.setAlignment(Qt.AlignCenter)
        
        #Icono
        trashIcon = QLabel()
        trashIcon.setStyleSheet('background-color: rgba(255, 0, 0, 0)')
        trashIcon.setPixmap(QPixmap("./images/trash.png"))
        trashIcon.setAlignment(Qt.AlignCenter)
        trashIcon.setMaximumSize(60,60)
        trashIcon.setScaledContents(True)
        self.setStyleSheet('background-color: rgba(255, 0, 0, 0.5)')

        vBoxDeleteGates.addWidget(trashIcon)
        self.setLayout(vBoxDeleteGates)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def dropEvent(self, event:QDropEvent):
        print(event.pos())
        event.acceptProposedAction()
        # if event.mimeData().hasImage():
        #     newGate = QLabelClickable()
        #     newGate.setPixmap(QPixmap.fromImage(QImage(event.mimeData().imageData())))
        #     newGate.setScaledContents(True)
        #     newGate.setMaximumSize(50,50)
        #     newGate.setAlignment(Qt.AlignCenter)
        #     blank = QLabel()
        #     blank.setAcceptDrops(True)
        #     blank.setPixmap(QPixmap('./images/dashedsquare.png'))
        #     blank.setMaximumSize(50,50)
        #     blank.setScaledContents(True)
        #     self.grid.addWidget(newGate, 0, self.currColumn)
        #     #self.grid.addWidget(blank, 0, self.currColumn-1)
        #     self.grid.addWidget(blank, 0, self.currColumn+1)
        #     self.currColumn += 2
        #     currentCircuit = Circuit()
        #     currentCircuit.addGate(event.mimeData().data)