from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6 import uic
import sys
import numpy as np
from 

class UI(QMainWindow):

    circuit = np.array([1,0])

    def __init__(self):
        super().__init__()
        uic.loadUi("prueba.ui", self)
        

    def addGate2Circuit(self, gate):
        np.concatenate((self.circuit, gate))


    def simulate(self):
        result = self.circuit[0]
        for index, op in enumerate(self.circuit):
             if (index+1 < self.circuit.len and index - 1 >= 0):
                result = np.kron(result, self.circuit[index+1])

    def gateDropped(self0):
        self.

app = QApplication(sys.argv)
window = UI()
window.show()
sys.exit(app.exec())