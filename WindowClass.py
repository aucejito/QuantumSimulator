import logging
from QTextEditLogger import QTextEditLogger
from QiskitRun import QiskitRun
from Gate import Gate
import json
import time
from PyQt5.sip import delete
from trashWidget import trashWidget
from Util import Util
from Simulation import Simulation1 as sim
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
import ast


plot1 = None
plot2 = None

class Window(QMainWindow):

    imagePath = './images/'
    qbitCounter = 2
    currentCircuit = None
    qbitsList = []
    customGatesCounter = 0
    customGates = []

    def __init__(self):
        super().__init__()
        self.currentCircuit = Circuit()
        self.initializeUI()
        #deleteGates.deleted.connect(lambda:self.qbitCleanUp())
        
    def initializeUI(self):
        self.setWindowTitle("Quantum Simulator")
        self.setWindowIcon(QIcon("./images/icon.jpg"))
        self.setGeometry(500, 500, 1200, 700)
        self.setupMenu()
        self.setupUI()
        self.show()

    def setupMenu(self):
        saveAct = QAction('Guardar', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.triggered.connect(self.file_save)

        loadAct = QAction('Cargar', self)
        loadAct.setShortcut('Ctrl+L')
        loadAct.triggered.connect(self.file_load)

        newAct = QAction('Nuevo', self)
        newAct.setShortcut('Ctrl+N')
        newAct.triggered.connect(self.new_circuit)

        exitAct = QAction('Salir', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.close)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('Archivo')
        fileMenu.addAction(newAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(loadAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        runMenu = menuBar.addMenu('Ejecutar')
        runIBMAct = QAction('IBM', self)
        runIBMAct.triggered.connect(lambda:self.runIBMCircuit())
        runMenu.addAction(runIBMAct)
        
    def file_save(self):
        name = QFileDialog.getSaveFileName(self, 'Save File', filter="JSON files (*.json)")

        if self.currentCircuit.made == False:
            self.currentCircuit.make(self.qbitsList)



        saveDict = {
            "circuit":{
                
            },
            "customGates":{}
        }

        # columnGates = [[]]
        # for qbit in self.qbitsList:
        #     for j in range(qbit.grid.count()):
        #         if(type(qbit.grid.itemAtPosition(0, j).widget()) == type(QLabel())):
        #             columnGates.append('None')
        #         else:
        #             columnGates.append(qbit.grid.itemAtPosition(0, j).widget().gate)
        # print(columnGates)
        self.currentCircuit.save_circuit()
        saveDict['circuit'] = self.currentCircuit.saved_circuit
        saveDict["numqbits"] =  self.qbitCounter
        jsonString = json.dumps(saveDict)

        file = open(str(name[0]), 'w')
        file.write(jsonString)
        file.close()

    def file_load(self):
        name = QFileDialog.getOpenFileName(self,'Cargar Archivo', filter="JSON files (*.json)")
        file = open(str(name[0]), 'r')

        with file:
            text = file.read()

        print(text)
        dictionary = ast.literal_eval(text)
        qbits_loaded = dictionary["numqbits"]

        self.new_circuit()
        
        
        
        for times in range(qbits_loaded-2):
            self.addQbit(self.vBox2)

        for line in self.qbitsList:
            line.currColumn = 0
            for i in reversed(range(line.grid.count())): 
                line.grid.itemAt(i).widget().setParent(None)
            print( "NUM ELEMS EN QBIT", line.grid.count())


        

        for column in dictionary["circuit"]: 
            for item  in column:
                    index = column.index(item)
                    self.qbitsList[index].add_gate(item)
                   

    def new_circuit(self):
        self.close()
        self.qbitCounter = 0
        self.qbitsList.clear()
        self.currentCircuit = Circuit(True)
        self.__init__()
        
    def runIBMCircuit(self):
        self.currentCircuit.make(self.qbitsList)
        run = QiskitRun()
        run.create_circuit(self.currentCircuit)
        

        run.setup()
        run.run_circuit()
        print("results: ", run.get_results())
        run.results_formatting()
        self.openResultDialog(run.results)



    def setupUI(self):
        verticalLytWdgt1 = QWidget()
        simulateButton = QPushButton(QIcon("images/play.png"), "Simular")
        addQbitButton = QPushButton(QIcon("images/add.png"), "Añadir cúbit")
        customGateButton = QPushButton(QIcon("images/add.png"), "Crear puerta")

        
        '''Conexión al método de simulación'''
        simulateButton.clicked.connect(self.startSimulation)

        

        vBox1 = QVBoxLayout()
        
        buttonBarWidget = QWidget()
        buttonBarLayout = QHBoxLayout()
        vBox1.addWidget(buttonBarWidget)
        buttonBarWidget.setLayout(buttonBarLayout)
        buttonBarLayout.addWidget(simulateButton)
        buttonBarLayout.addWidget(addQbitButton)
        buttonBarLayout.addWidget(customGateButton)
        verticalLytWdgt1.setLayout(vBox1)
        self.setCentralWidget(verticalLytWdgt1)
        buttonBarLayout.setStretch(0, 4)
        buttonBarLayout.setStretch(1, 1)
        buttonBarLayout.setStretch(2,1)

        

        horizontalLytWdgt1 = QWidget()
        vBox1.addWidget(horizontalLytWdgt1)
        
        hbox1 = QHBoxLayout()
        horizontalLytWdgt1.setLayout(hbox1)

        gatesTabWidget = QTabWidget()
        gatesWidget = QWidget()
        customGatesWidget = QWidget()
        gridGates = QGridLayout()
        self.gridCustomGates = QGridLayout()

        gatesWidget.setLayout(gridGates)    
        customGatesWidget.setLayout(self.gridCustomGates)


        vboxGatesLyt = QVBoxLayout()
        vboxGatesWdgt = QWidget()
        hbox1.addWidget(vboxGatesWdgt)
        vboxGatesLyt.addWidget(gatesTabWidget)
        
        deleteGates = trashWidget()
        vboxGatesLyt.addWidget(deleteGates)
        #gatesTabWidget.setLayout(gridGates)
        vboxGatesWdgt.setLayout(vboxGatesLyt)
        vboxGatesLyt.setStretch(0,5)
        vboxGatesLyt.setStretch(1,1)

        self.fillGridGates(gridGates)

        self.vBox2 = QVBoxLayout()
        verticalLytWdgt2 = QWidget()
        verticalLytWdgt2.setLayout(self.vBox2)
        hbox1.addWidget(verticalLytWdgt2)
        hbox1.setStretch(0,1)
        hbox1.setStretch(1,5)
        self.line1 = QbitLine(self.currentCircuit,0)
        self.qbitsList.append(self.line1)
        self.line2 = QbitLine(self.currentCircuit,1)
        self.qbitsList.append(self.line2)
        self.vBox2.addWidget(self.line1)
        self.vBox2.addWidget(self.line2)
        vBox1.setStretch(0,1)
        vBox1.setStretch(1,10)
    
        gatesTabWidget.addTab(gatesWidget, "Puertas")
        gatesTabWidget.addTab(customGatesWidget, "Personalizadas")

        addQbitButton.clicked.connect(lambda:self.addQbit(self.vBox2))
        customGateButton.clicked.connect(lambda:self.createGate())

    #TODO: Limpar qbit al borrar puerta de ese qbit
    # def qbitCleanUp(self):
    #     qbitToReorder = self.deleteGates.gateToDelete.parent()
    #     qbitToReorder.cleanQGrid()

    def addQbit(self, layout):
        newQbitLine = QbitLine(self.currentCircuit, self.qbitCounter)
        #newQbitLine.setOrderId(self.qbitCounter)
        self.qbitCounter += 1
        layout.addWidget(newQbitLine)
        self.qbitsList.append(newQbitLine)

        
    def createGate(self):
        gateDialog = QDialog()
        gateDialog.setModal(True)
        gateDialog.setWindowTitle("Crear puerta cuántica")
        gateDialog.setWindowIcon(QIcon("./images/icon.jpg"))
        gateDialog.setGeometry(500, 500, 300, 300)

        self.createGateUI(gateDialog)

        gateDialog.show()
        gateDialog.exec()

    def createGateUI(self, dialog):
        vBox = QVBoxLayout()

        self.create_gate_dialog = dialog
        gridInfo = QGridLayout()
        
        gridInfo.addWidget(QLabel("Nombre"),1,0)
        gridInfo.addWidget(QLabel("Símbolo"),2,0)
        gridInfo.addWidget(QLabel("Matriz"),3,0)

        self.gateNameLE = QLineEdit()
        self.gateSymbolLE = QLineEdit()
        self.gateMatrixTE = QTextEdit()

        regex = QRegExp('[A-Z]{2,4}')
        validator = QRegExpValidator(regex, self)
        
        self.gateSymbolLE.setValidator(validator)
        self.gateSymbolLE.setPlaceholderText("ID")
        self.gateNameLE.setPlaceholderText("Identity")
        self.gateMatrixTE.setPlaceholderText("[[1,0],[0,1]]")

        gridInfo.addWidget(self.gateNameLE,1,1)
        gridInfo.addWidget(self.gateSymbolLE,2,1)
        gridInfo.addWidget(self.gateMatrixTE,3,1)

        gridInfo.addWidget(acceptButton := QPushButton("Aceptar"),4,1)

        acceptButton.clicked.connect(lambda:self.saveGate())
        vBox.addLayout(gridInfo)
        dialog.setLayout(vBox)

    def saveGate(self):

        new_Gate = Gate()
        new_Gate.id = self.customGatesCounter
        new_Gate.name = self.gateNameLE.text()
        new_Gate.symbol = self.gateSymbolLE.text()
        new_Gate.matrix = np.array(self.gateMatrixTE.toPlainText())
        img_ful_path = Util.generateGateImage(new_Gate)
        new_QLabel = QLabelClickable(new_Gate.symbol)
        new_QLabel.setPixmap(QPixmap(img_ful_path))
        
        if (len(self.customGates)%2 == 0):
            self.gridCustomGates.addWidget(new_QLabel,len(self.customGates),len(self.customGates)%2)        
        else: 
            self.gridCustomGates.addWidget(new_QLabel,len(self.customGates)-1,len(self.customGates)%2)
        
        self.customGates.append(new_Gate)
        self.create_gate_dialog.close()

    def fillGridGates(self, grid):
        gateX = self.generateGateLabel('X')
        gateY = self.generateGateLabel('Y')
        gateZ = self.generateGateLabel('Z')
        gateH = self.generateGateLabel('H')
        gateC = self.generateGateLabel('C')
        gateID = self.generateGateLabel('ID')

        #Añadir puertas al grid
        grid.addWidget(gateX,1,1)
        grid.addWidget(gateY,1,2)
        grid.addWidget(gateZ,2,1)
        grid.addWidget(gateH,2,2)
        grid.addWidget(gateC,3,1)
        grid.addWidget(gateID,3,2)


        gateX.clicked.connect(lambda:self.openGate('x'))
        gateY.clicked.connect(lambda:self.openGate('y'))
        gateZ.clicked.connect(lambda:self.openGate('z'))
        gateH.clicked.connect(lambda:self.openGate('h'))
        gateC.clicked.connect(lambda:self.openGate('c'))
        gateID.clicked.connect(lambda:self.openGate('id'))

    def generateGateLabel(self, gate):
        gateLabel = QLabelClickable(gate)
        self.image_path = './images/'
        fullpath = self.image_path + gate + '.jpg'
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
        #TODO Crear circuito y cálculo

        if self.currentCircuit.made == False:
            self.currentCircuit.make(self.qbitsList)  
        simul = sim()
        start_time = time.time()
        results = simul.simulate(self.currentCircuit, 5)
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
        qbits = results.get('numQbits')
        vLayout = QVBoxLayout()
        resultWindow = pg.plot()
        resultWindow.setBackground('w')
        resultWindow.setXRange(0,pow(2,qbits), 0.05)
        resultWindow.setYRange(0, 100, 0.05)
        plot1 = resultWindow.getPlotItem()
        plot1.showGrid(True, True)
        plot1.getAxis('left').setLabel('Porcentaje')
        plot1.getAxis('bottom').setLabel('Estados')
        #Eje de la derecha

        # plot2 = pg.ViewBox()
        # plot1.showAxis('right')
        # plot1.scene().addItem(plot2)
        # plot1.getAxis('right').linkToView(plot2)
        # plot2.setXLink(plot1)
        # plot1.getAxis('right').setLabel('Frecuencia')
    

        
        xAxis = []
        for i in range(pow(2,qbits)):
            state = bin(i)[2:]
            if len(state) < qbits:
                state = state.zfill(2)
            xAxis.append(state)
        xdict = dict(enumerate(xAxis))
        plot1.getAxis('bottom').setTicks([xdict.items()])
        #plot2.getAxis('bottom').setTicks([xdict.items()])
        probabilities = results.get('prob')
        bargraph = pg.BarGraphItem(x=range(pow(2,qbits)), height = probabilities, width = 0.6, brush ='g')
        #bargraph2 = pg.BarGraphItem(x=range(pow(2,qbits)), height = [0,0,1,1], width = 0.6, brush = 'r')
        plot1.addItem(bargraph)
        #plot2.addItem(bargraph2)
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

 
 