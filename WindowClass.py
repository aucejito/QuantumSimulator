import sys, csv
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow, QPushButton,
QLineEdit, QComboBox, QGroupBox, QTableView, QHeaderView, QHBoxLayout,
QFormLayout, QVBoxLayout, QDialog, QFileDialog, QAction)
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt

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

        
        
        
        '''Group Box a la izquierda con las puertas cuánticas
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

if __name__ == '__main__':
 app = QApplication(sys.argv)
 window = Window()
 sys.exit(app.exec_())