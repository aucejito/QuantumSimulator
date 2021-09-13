from Qbit import Qbit
from trashWidget import trashWidget
from numpy import append
from Circuit import Circuit
from QLabelClickable import QLabelClickable
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import copy
from gates import gates

blank = None

class QbitLine(QFrame):
    
    orderId = -1
    grid = QGridLayout()
    currColumn = 2
    circuit = None

    def __init__(self, circuit, order=-1, *args, **kwargs):
        QFrame.__init__(self, *args, **kwargs)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.orderId = order
        ini_state = QLabel("q" + str(self.orderId), self)
        ini_state.setFont(QFont('Arial',13))
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0,0,0,0)
        global blank
        blank = QLabel()
        blank.setPixmap(QPixmap('./images/dashedsquare.png'))
        blank.setMaximumSize(50,50)
        blank.setScaledContents(True)
        if(circuit.loaded == False):
            self.add_blanks()
        self.setAcceptDrops(True)
        print(circuit)
        self.circuit = circuit

    def add_blanks(self):
        self.grid.addWidget(blank, 0, 2)
        self.grid.addWidget(blank, 0, 0)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def setOrderId(self, id):
        self.orderId = id
        print(f'{self.orderId} is the id of the cubit')

    def dropEvent(self, event:QDropEvent):
        print(event.pos())
        event.acceptProposedAction()
        if event.mimeData().hasImage():
            newGate = QLabelClickable(event.source().gate.id)
            newGate.qbit = self.orderId
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
            new_gate = event.pos().x()

            while new_gate > self.grid.itemAtPosition(0, index).widget().geometry().center().x():
                print("{} > {} ??".format(event.pos().x(),self.grid.itemAtPosition(0, index).geometry().center().x()))
                index += 1
                if(self.grid.itemAtPosition(0, index) is None):
                    break

            print('index {}'.format(index))

            if(index == 0 and self.grid.count() == 1):
                index += 1
                self.grid.addWidget(newGate,0,index)
                newGate.position['column'] = index
                #self.grid.addWidget(blank, 0, 0) ¿??¿?¿¿?
                self.grid.addWidget(blank, 0, 2)
            elif(index == 0):
                itemsToMove = []
                for i in range(self.grid.count()):
                    print('i = {}'.format(i))
                    # if(self.grid.itemAtPosition(0, i) is None):
                    #     break
                    itemsToMove.append(self.grid.itemAtPosition(0,i).widget())
                #TODO probablemente haya que limpiar cada vez que se añade una puertas. Son pegatinas, se van superponiendo
                for i in range(len(itemsToMove)):
                    self.grid.addWidget(itemsToMove[i], 0, i+2)
                self.grid.addWidget(newGate,0, 1)
                
                newGate.position['column'] = 1
                self.grid.addWidget(blank, 0, 2)
                self.grid.addWidget(blank, 0, 0)
            elif(index < self.grid.count()):
                itemsToMove = []
                for i in range(index, self.grid.count()):
                    print('i = {}'.format(i))
                    # if(self.grid.itemAtPosition(0, i) is None):
                    #     break
                    itemsToMove.append(self.grid.itemAtPosition(0,i).widget())
                print("numero de items a mover: {}".format(len(itemsToMove)))
                posToMove = index+2
                for i in range(len(itemsToMove)):
                    self.grid.addWidget(itemsToMove[i], 0, posToMove)
                    posToMove +=  1 
                if(type(self.grid.itemAtPosition(0, index-1).widget()) == type(blank)):
                    self.grid.addWidget(newGate,0, index)
                    self.grid.addWidget(blank, 0, index+1)
                    newGate.position['column'] = index
                else:
                    self.grid.addWidget(newGate,0, index+1)
                    self.grid.addWidget(blank, 0, index)
                    newGate.position['column'] = index+1
            elif(index == self.grid.count()):
                self.grid.addWidget(newGate,0, index)
                newGate.position['column'] = index
                self.grid.addWidget(blank, 0, index+1)

            newGate.position['qbit'] = self.orderId
                
            print(self.grid.itemAtPosition(0,0))

            print(type(blank) == type(QLabel))
            print(type(QLabel))
            print(type(newGate))
            self.circuit.addGate(newGate.gate, newGate.position)
            # itemsToMove = []
            # print(index)
            # for i in range(index, self.grid.count()):
            #     if(self.grid.itemAtPosition(0, i) is None):
            #         break
            #     itemsToMove.append(self.grid.itemAtPosition(0,i).widget())
            
            
            # self.grid.addWidget(newGate,0,index)
            
            # for i in range(len(itemsToMove)):
            #     self.grid.addWidget(itemsToMove[i], 0, i)


            # #self.grid.addWidget(newGate, 0, index)
            # # if(index == 0):
            # #     itemsToMove.clear()
            # #     for i in range(self.grid.count()):
            # #         itemsToMove.append(self.grid.itemAtPosition(0,i).widget())
            # #         if(self.grid.itemAtPosition(0, index) is None):
            # #             break
            # #     for i in range(len(itemsToMove)):
            # #         self.grid.addWidget(itemsToMove[i], 0, i)

            # self.grid.addWidget(blank, 0, index-1)
            # self.grid.addWidget(blank, 0, index+1)
            # self.currColumn += 2
           

    #TODO: Limpiar qbit al borrar una puerta
    # def cleanQGrid(self):
    #     for i in range(1,len(self.grid.count())):
    #         currentSlot = self.grid.itemAtPosition(0,i).widget()
    #         previousSlot = self.grid.itemAtPosition(0,i-1).widget()
    #         if(type(currentSlot) == type(blank) and type(previousSlot) == type(blank)):
    #             self.grid.itemAtPosition(0, i).widget().setParent(None)
    #             self.grid.itemAtPosition(0, i-1).widget().setParent(None)
    #             itemsToMove = []
    #             for j in range(i+1, len(self.grid.count())):
    #                 itemsToMove.append(self.grid.itemAtPosition(0, j))
    #             for k in range(i-1,len(itemsToMove)):
    #                 self.grid.addWidget(itemsToMove[k])
                    
        print(self.orderId)
        print(self.grid.count())

    def add_gate(self, gate):
        if gate == 1:
            self.grid.addWidget(blank, 0, self.currColumn)
        else:
            new_gate = self.setup_gate(gate)
            self.grid.addWidget(new_gate, 0, self.currColumn)
            self.circuit.addGate(new_gate.gate, {"qbit":self.orderId, "column": self.currColumn})

        self.currColumn +=1
        
    def setup_gate(self, gate):
        newGate = QLabelClickable(gate)
        # newGate.gate = Gate(gate)
        newGate.qbit = self.orderId
        pathImage = gates[gate]["symbol"]
        newGate.setPixmap(QPixmap(pathImage))
        newGate.setScaledContents(True)
        newGate.setMaximumSize(50,50)
        newGate.setAlignment(Qt.AlignCenter)
        return newGate