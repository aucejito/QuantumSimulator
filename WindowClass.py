from GateGroupBox import GateGroupBox
from PyQt5 import QtCore
from QbitLine import QbitLine
import sys, csv

import numpy as np
from QLabelClickable import QLabelClickable
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import gates as gt

class Window(QMainWindow):

    imagePath = './images/'

    def __init__(self):
        super().__init__()
        self.initializeUI()
        
    def initializeUI(self):
        self.setWindowTitle("Quantum Simulator")
        self.setWindowIcon(QIcon("./images/icon.jpg"))
        self.setGeometry(500, 500, 900, 700)
        self.setupMenu()
        self.setupUI()
        self.show()

    def setupMenu(self):
        saveAct = QAction('Save', self)
        saveAct.setShortcut('Ctrl+S')
        #saveAct.triggered.connect(self.saveToFile)

        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.close)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        fileMenu.addAction(saveAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        exportMenu = menuBar.addMenu('Export')
        exportQASMAct = QAction('QASM', self)
        #exportQASMAct.triggered.connect(self.exportToQASM)
        exportMenu.addAction(exportQASMAct)
        

    def setupUI(self):
        verticalLytWdgt1 = QtWidgets.QWidget()
        simulateButton = QPushButton(QIcon("images/play.png"), "Simular")
        
        '''Conexión al método de simulación'''
        #simulateButton.clicked.connect(self.startSimulation)

        vBox1 = QVBoxLayout()
        vBox1.addWidget(simulateButton)
        verticalLytWdgt1.setLayout(vBox1)
        self.setCentralWidget(verticalLytWdgt1)
        

        horizontalLytWdgt1 = QtWidgets.QWidget()
        vBox1.addWidget(horizontalLytWdgt1)
        
        hbox1 = QHBoxLayout()
        horizontalLytWdgt1.setLayout(hbox1)

        gatesGroupBox = GateGroupBox("Puertas")
        vboxGatesLyt = QVBoxLayout()
        vboxGatesWdgt = QWidget()
        hbox1.addWidget(vboxGatesWdgt)
        vboxGatesLyt.addWidget(gatesGroupBox)
        gridGates = QGridLayout()

        deleteGates = QWidget()
        deleteGates.setAcceptDrops(True)
        deleteGates.setStyleSheet('background-color: rgba(255, 0, 0, 0.5)')
        vBoxDelGates = QVBoxLayout()
        vBoxDelGates.setAlignment(Qt.AlignCenter)
        trashIcon = QLabel()
        trashIcon.setStyleSheet('background-color: rgba(255, 0, 0, 0)')
        trashIcon.setPixmap(QPixmap("./images/trash.png"))
        trashIcon.setAlignment(Qt.AlignCenter)
        trashIcon.setMaximumSize(60,60)
        trashIcon.setScaledContents(True)
        trashIcon.setAcceptDrops(True)
        vBoxDelGates.addWidget(trashIcon)
        deleteGates.setLayout(vBoxDelGates)
        vboxGatesLyt.addWidget(deleteGates)
        gatesGroupBox.setLayout(gridGates)
        vboxGatesWdgt.setLayout(vboxGatesLyt)
        vboxGatesLyt.setStretch(0,5)
        vboxGatesLyt.setStretch(1,1)

        self.fillGridGates(gridGates)

        vBox2 = QVBoxLayout()
        verticalLytWdgt2 = QtWidgets.QWidget()
        verticalLytWdgt2.setLayout(vBox2)
        hbox1.addWidget(verticalLytWdgt2)
        hbox1.setStretch(0,1)
        hbox1.setStretch(1,5)
        line1 = QbitLine()
        line2 = QbitLine()
        vBox2.addWidget(line1)
        vBox2.addWidget(line2)
        vBox1.setStretch(0,1)
        vBox1.setStretch(1,1)


        '''
        #Group Box a la izquierda con las puertas cuánticas
        
        gatesGBox = QGroupBox("Puertas")
        groupBoxLytWidget1 = QGridLayout()
        horizontalLytWdgt1.setLayout(groupBoxLytWidget1)
        
        #Añadimos las puertas al groupBox
        labelHadamard = QLabel(gatesGBox)
        labelHadamard.setPixmap(QtGui.QPixmap("images/H.jpg"))
        groupBoxLytWidget1.addWidget(labelHadamard)
        #groupBoxLytWidget1.addWidget()

        #hBox1 = QHBoxLayout()
        #hBox1.addWidget(self, gatesGBox)
        #vBox1.addWidget(self, horizontalLytWdgt1)
'''
    
    def fillGridGates(self, grid):
        gateX = self.generateGateLabel('X')
        gateY = self.generateGateLabel('Y')
        gateZ = self.generateGateLabel('Z')
        gateH = self.generateGateLabel('H')
        gateCX = self.generateGateLabel('CX')
        gateID = self.generateGateLabel('ID')


        #Añadir puertas al grid
        grid.addWidget(gateX,1,1)
        grid.addWidget(gateY,1,2)
        grid.addWidget(gateZ,2,1)
        grid.addWidget(gateH,2,2)
        grid.addWidget(gateCX,3,1)
        grid.addWidget(gateID,3,2)


        gateX.clicked.connect(lambda:self.openGate('x'))
        gateY.clicked.connect(lambda:self.openGate('y'))
        gateZ.clicked.connect(lambda:self.openGate('z'))
        gateH.clicked.connect(lambda:self.openGate('h'))
        gateCX.clicked.connect(lambda:self.openGate('cx'))
        gateID.clicked.connect(lambda:self.openGate('id'))

    def generateGateLabel(self, gate):
        gateLabel = QLabelClickable(gate)
        imagePath = './images/'
        fullpath = imagePath + gate + '.jpg'
        pixmap = QPixmap(fullpath)
        gateLabel.setScaledContents(True)
        gateLabel.setPixmap(pixmap)
        gateLabel.setMaximumSize(50,50)
        gateLabel.setAlignment(Qt.AlignCenter)
        return gateLabel

    def openGate(self, gate):
        gateDialog = QDialog()
        gateDialog.setModal(True)
        gateDialog.setWindowTitle("Quantum Simulator")
        gateDialog.setWindowIcon(QIcon("./images/icon.jpg"))
        gateDialog.setGeometry(500, 500, 300, 300)

        # grid = QGridLayout()
        # name = QLabel("Hola")
        # grid.addWidget(name,1,0)
        # gateDialog.setLayout(grid)


        self.loadGateInfoUI(gateDialog, gate) #Llamada a un método que disponga los elementos UI 
        gateDialog.show()
        gateDialog.exec()
    
    def loadGateInfoUI(self, dialog, gate):
        data = self.loadGateData(gate) #Llamada a un método que nos devuelva la información de la puerta en un diccionario
        vBox = QVBoxLayout()
        vBox.addWidget(QLabel("Información de la puerta cuántica"), alignment=Qt.AlignCenter)
        
        #vBox.setStretch(1,100)
        
        gridInfo = QGridLayout()
        gridInfo.setColumnStretch(0,2)
        gridInfo.setColumnStretch(1,8)
        
        gridInfo.addWidget(QLabel("Nombre"),1,0)
        gridInfo.addWidget(QLabel("Icono"),2,0)
        gridInfo.addWidget(QLabel("Matriz"),3,0)

        gridInfo.addWidget(QLabel(data.get("name")),1,1)
        gatePixmap = QPixmap(data.get("symbol"))
        
        gateIcon = QLabel("Hola")
        gateIcon.setScaledContents(True)
        #gridInfo.addWidget(gateIcon.setPixmap(gatePixmap),2,1)
        gridInfo.addWidget(self.generateGateLabel(data.get('id').upper()),2,1)
        gridInfo.addWidget(QLabel(np.array2string(data.get("matrix"))),3,1)
        vBox.addLayout(gridInfo)
        vBox.setStretch(1,1)
        dialog.setLayout(vBox)
        #vBox1.addWidget(QLabel(data.get("name"))) TODO de los datos obtenidos obtenemos el nombre, la matrix,etc


    def loadGateData(self, gate):
        gate = gate.lower()
        data = gt.gates.get(gate)
        return data

if __name__ == '__main__':
 app = QApplication(sys.argv)
 window = Window()
 sys.exit(app.exec_())

 