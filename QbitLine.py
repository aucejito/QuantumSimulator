from numpy import append
from Circuit import Circuit
from QLabelClickable import QLabelClickable
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

blank = None

class QbitLine(QFrame):
    grid = QGridLayout()
    currColumn = 2
    
    def __init__(self, *args, **kwargs):
        QFrame.__init__(self, *args, **kwargs)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0,0,0,0)
        global blank
        blank = QLabel()
        blank.setPixmap(QPixmap('./images/dashedsquare.png'))
        blank.setMaximumSize(50,50)
        blank.setScaledContents(True)
        self.grid.addWidget(blank, 0, 2)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def dropEvent(self, event:QDropEvent):
        print(event.pos())
        event.acceptProposedAction()
        if event.mimeData().hasImage():
            newGate = QLabelClickable()
            newGate.setPixmap(QPixmap.fromImage(QImage(event.mimeData().imageData())))
            newGate.setScaledContents(True)
            newGate.setMaximumSize(50,50)
            newGate.setAlignment(Qt.AlignCenter)
            blank = QLabel()
            blank.setAcceptDrops(True)
            blank.setPixmap(QPixmap('./images/dashedsquare.png'))
            blank.setMaximumSize(50,50)
            blank.setScaledContents(True)
            
            index = 0
            while event.pos().x() > self.grid.getItemPosition(index)[1]:
                print(self.grid.getItemPosition(index)[2])
                index += 1


            itemsToMove = []
            for i in range(index, self.grid.count()):
                itemsToMove.append(self.grid.itemAtPosition(column=i))
            
            
            self.grid.addWidget(newGate,0,index)
            
            for i in range(len(itemsToMove)):
                self.grid.addWidget(itemsToMove[i])


            self.grid.addWidget(newGate, 0, index)
            self.grid.addWidget(blank, 0, index-1)
            self.grid.addWidget(blank, 0, index+1)
            self.currColumn += 2
            currentCircuit = Circuit()
            currentCircuit.addGate(event.mimeData().data)
        print(self.grid.count())
            