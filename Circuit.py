from QLabelClickable import QLabelClickable
from Gate import Gate
import numpy as np

class Circuit():
    initialState = None
    states = []
    gates = []
    

    def __init__(self) -> None:
        self.initialState = np.array([1,0])


    def addGate(self, gate, position):
        
        qbit = position['qbit']
        column = position['column']
        if len(self.gates) < qbit+1:
            for i in range((qbit+1)-len(self.gates)):
                pass
                #self.gates.append([])
        a = {column:gate}
        #self.gates[qbit].append(a)
        # print(self.gates[qbit])

    def removeGate(self, gate):        
        self.gates.remove(gate) #TODO corregir, esto borra la primera ocurrencia de gate

    # def calculate(self):
    #     pass

    # def reorder(self):
    #     for list in self.gates:
    #         items = list.items()
    #         for gate in items:
                
            
    def make(self, qbits_list):
        num_qbit = 0
        for qbit in qbits_list:
            num_gate = 0
            self.gates.append([])
            for widget in range(qbit.grid.count()):
                widget = qbit.grid.itemAt(num_gate).widget()
                if type(widget) == type(QLabelClickable('X')):
                    self.gates[num_qbit].append(widget.gate)
                else:
                    self.gates[num_qbit].append(1)
                num_gate += 1
            num_qbit += 1    
        print('Circuito: {}'.format(self.gates))
#OPCIÓN QUIRK    
    # def save_circuit():
    #     if self.gates.count() < qbit:
    #         for i in range(qbit-self.gates.count()):
    #             self.gates.append([])
    #     self.gates[column].append(gate)
