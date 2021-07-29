import time
from Util import Util
from Simulation import Simulation as sim
from GateGroupBox import GateGroupBox
from PyQt5 import QtCore
from QbitLine import QbitLine
from Circuit import Circuit
import pyqtgraph as pg
import sys, csv
import numpy as np
from QLabelClickable import QLabelClickable
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import gates as gt


plot1 = None
plot2 = None

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
        verticalLytWdgt1 = QWidget()
        simulateButton = QPushButton(QIcon("images/play.png"), "Simular")
        
        '''Conexión al método de simulación'''
        simulateButton.clicked.connect(self.startSimulation)

        vBox1 = QVBoxLayout()
        vBox1.addWidget(simulateButton)
        verticalLytWdgt1.setLayout(vBox1)
        self.setCentralWidget(verticalLytWdgt1)
        

        horizontalLytWdgt1 = QWidget()
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
        verticalLytWdgt2 = QWidget()
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
        gateDialog.setWindowTitle("Información de la puerta cuántica")
        gateDialog.setWindowIcon(QIcon("./images/icon.jpg"))
        gateDialog.setGeometry(500, 500, 300, 300)

        self.loadGateInfoUI(gateDialog, gate) #Llamada a un método que disponga los elementos UI 
        gateDialog.show()
        gateDialog.exec()
    
    def loadGateInfoUI(self, dialog, gate):
        data = Util.loadGateData(gate) #Llamada a un método que nos devuelva la información de la puerta en un diccionario
        vBox = QVBoxLayout()
        
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

    def startSimulation(self):
        matrices = self.getAllMatrices()
        #TODO Crear circuito y cálculo
               
        currCircuit = Circuit()
        start_time = time.time()
        results = sim.simulate(currCircuit, 5)
        elapsed_time = time.time() - start_time
        
        print("Tiempo de ejecucion de la simulacion: %0.10f segundos." %elapsed_time)
        self.openResultDialog(results)
        
        
    def getAllMatrices(self):
        gates = gt.gates.values()
        matrices = []
        for gate in gates:
            matrices.append(gate.get('matrix'))
        
        return matrices

    def loadGateData(self, gate):
        gate = gate.lower()
        data = gt.gates.get(gate)
        return data

    def openResultDialog(self, results):
        resultDialog = QDialog()
        resultDialog.setModal(True)
        resultDialog.setWindowTitle("Resultados de la simulación")
        resultDialog.setWindowIcon(QIcon("./images/icon.jpg"))
        resultDialog.setGeometry(500, 500, 800, 500)

        self.loadResultUI(resultDialog, results) #Llamada a un método que disponga los elementos UI 
        resultDialog.show()
        resultDialog.exec()

    def loadResultUI(self, resultDialog : QDialog, results):
        vLayout = QVBoxLayout()
        resultWindow = pg.plot()
        resultWindow.setBackground('w')
        resultWindow.setXRange(0,16, 0.05)
        resultWindow.setYRange(0, 100, 0.05)
        plot1 = resultWindow.getPlotItem()
        plot1.showGrid(True, True)
        
        #Eje de la derecha

        plot2 = pg.ViewBox()
        plot1.showAxis('right')
        plot1.scene().addItem(plot2)
        plot1.getAxis('right').linkToView(plot2)
        plot2.setXLink(plot1)
        plot1.getAxis('right').setLabel('Frecuencia')
    

        qbits = 2 #results.get('qbits')
        xAxis = []
        for i in range(pow(2,qbits)):
            state = bin(i)[2:]
            if len(state) < qbits:
                state = state.zfill(2)
            xAxis.append(state)
        xdict = dict(enumerate(xAxis))
        plot1.getAxis('bottom').setTicks([xdict.items()])
        #plot2.getAxis('bottom').setTicks([xdict.items()])
        probabilities = [0,0, 50, 50]
        bargraph = pg.BarGraphItem(x=range(pow(2,qbits)), height = probabilities, width = 0.6, brush ='g')
        bargraph2 = pg.BarGraphItem(x=range(pow(2,qbits)), height = [0,0,1,1], width = 0.6, brush = 'r')
        plot1.addItem(bargraph)
        plot2.addItem(bargraph2)
        #updateViews()
        #plot1.vb.sigResized.connect(updateViews)

        vLayout.addWidget(QLabel("Vector de estados"))
        for i in range(pow(2,qbits)):
            stateStr = "" + str(xAxis[i]) + "    " + str(probabilities[i]) + "%" + "     " #+ str(results["resMatrix"])
            probLabel = QLabel(stateStr)
            vLayout.addWidget(probLabel)
        
        vLayout.setContentsMargins(5,5,5,5)
        vLayout.addWidget(resultWindow)
        resultDialog.setLayout(vLayout)


def updateViews():
    ## view has resized; update auxiliary views to match
    global plot1, plot2
    plot2.setGeometry(plot1.vb.sceneBoundingRect())
    
    ## need to re-update linked axes since this was called
    ## incorrectly while views had different shapes.
    ## (probably this should be handled in ViewBox.resizeEvent)
    plot2.linkedViewChanged(plot1.vb, plot2.XAxis)
    


if __name__ == '__main__':
 app = QApplication(sys.argv)
 window = Window()
 sys.exit(app.exec_())

 