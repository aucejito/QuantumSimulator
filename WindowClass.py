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

        gatesGroupBox = QGroupBox("Puertas")
        hbox1.addWidget(gatesGroupBox)
        gridGates = QGridLayout()
        gatesGroupBox.setLayout(gridGates)
        gateH = QLabelClickable('H')
        gateH.setFrameShape(QtWidgets.QFrame.Box)
        gateH.setMaximumSize(50,50)
        gateH.setAlignment(Qt.AlignCenter)

        #Añadir puertas al grid
        gridGates.addWidget(gateH,1,1)
        gridGates.addWidget(QLabel("2"),1,2)
        gridGates.addWidget(QLabel("3"),2,1)
        gridGates.addWidget(QLabel("4"),2,2)

        gateH.clicked.connect(lambda:self.openGate("hadamard"))

        vBox2 = QVBoxLayout()
        verticalLytWdgt2 = QtWidgets.QWidget()
        verticalLytWdgt2.setLayout(vBox2)
        hbox1.addWidget(verticalLytWdgt2)
        hbox1.setStretch(0,1)
        hbox1.setStretch(1,5)
        line1 = QtWidgets.QFrame()
        line1.setAcceptDrops(True)
        line1.setFrameShape(QtWidgets.QFrame.HLine)
        line2 = QtWidgets.QFrame()
        line2.setAcceptDrops(True)
        line2.setFrameShape(QtWidgets.QFrame.HLine)
        vBox2.addWidget(line1)
        vBox2.addWidget(line2)


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
    
    def openGate(self, gate):
        if(gate == 'hadamard'): 
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
        data = self.loadGateData(gate) #Llamada a un método que nos devuelva la información de la puerta en un diccionario/JSON 
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
        gridInfo.addWidget(gateIcon.setPixmap(gatePixmap),2,1)
        gridInfo.addWidget(QLabel(np.array2string(data.get("matrix"))),3,1)

        dialog.setLayout(gridInfo)
        #vBox1.addWidget(QLabel(data.get("name"))) TODO de los datos obtenidos obtenemos el nombre, la matrix,etc


    def loadGateData(self, gate):
        gate = gate.lower()
        data = gt.gates.get('x')
        return data

if __name__ == '__main__':
 app = QApplication(sys.argv)
 window = Window()
 sys.exit(app.exec_())

 