import numpy as np

class Circuit():
    initialState = None
    states = []
    gates = []

    def __init__(self) -> None:
        self.initialState = np.array([1,0])

    def addGate(self, gate):
        self.gates.append(gate)

    def removeGate(self, gate):        
        self.gates.remove(gate) #TODO corregir, esto borra la primera ocurrencia de gate

    # def calculate(self):
    #     pass