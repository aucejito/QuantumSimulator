from QLabelClickable import QLabelClickable
from Gate import Gate
import numpy as np

class Circuit():
    initialState = None
    states = []
    gates = []
    max = 0
    qbits = {}
    serialized = None
    made = False
    loaded = False

    def __init__(self, loaded = False) -> None:
        self.initialState = np.array([1,0])
        self.loaded = loaded


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

        qbits = {}
        for qbit in self.gates:
            if len(qbit) > self.max:
                self.max = len(qbit)
        
        for qbit in self.gates:
            self.qbits[self.gates.index(qbit)] = 1
            if len(qbit) < self.max:
                list_to_add = []
                for time in range(self.max+1 - len(qbit)):
                    list_to_add.append(1)
                qbit.extend(list_to_add)

        transposed = list(map(list, zip(*self.gates)))
        
        print(transposed)

        for list1 in transposed:
            if 1 == len(list(dict.fromkeys(list1))):
                transposed.remove(list1)

        print("trasnposed !: ",transposed)
        self.serialized = transposed

        self.made = True


    def save_circuit(self):
        res = []
        for col in self.serialized:
            aux = []
            for item in col:
               aux.append(item.id) if item != 1 else aux.append(1)
                    

            res.append(aux)

        self.saved_circuit = res
#OPCIÓN QUIRK    
    # def save_circuit():
    #     if self.gates.count() < qbit:
    #         for i in range(qbit-self.gates.count()):
    #             self.gates.append([])
    #     self.gates[column].append(gate)
