import matplotlib.pyplot as plt 
from PyQt5.QtCore import pyqtSignal
import matplotlib as mpl
from qiskit import result
from Circuit import Circuit
from qiskit.tools.monitor import job_monitor
from qiskit import *
from qiskit.result import Counts
#IBMQ.save_account('c96142dc9ba95ead8c9746ed6f2b05f31608e9cfe347563a1b3c2ea7e0fd7ec67829832d8bab02ba1b4cb5a7ffb8d24bb1cf176c308a93611cfe1369f1b4761d')

class QiskitRun():
    
    qc = None
    provider = None
    real_device = None
    job_info = 'Hola'
    
    def __init__(self) -> None:
        pass
   
    def setup(self):
        # IBMQ.load_account()
        # self.provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
        # self.real_device = self.provider.get_backend('ibmq_santiago')
        pass

    def create_circuit(self, circuit : Circuit):
        print("serialized: ", circuit.serialized)
        self.qbits = len(circuit.serialized[0]) #Número de cúbits
        self.qc = QuantumCircuit(self.qbits) #Inicialización del circuito
        for column in circuit.serialized: 
            curr_qbit = 0 
            for item  in column:    #transformación de nuestras puertas a Qiskit
                if item == 1:
                    pass
                else:
                    if item.id == 'x': 
                        self.qc.x(curr_qbit)
                    elif item.id == 'y':
                        self.qc.y(curr_qbit)
                    elif item.id =='z':
                        self.qc.z(curr_qbit)
                    elif item.id == 'h':
                        self.qc.h(curr_qbit)
                    elif item.id == 'c':
                        self.qc.control(curr_qbit)
                curr_qbit += 1 % self.qbits
        self.qc.measure_all() #Añadimos una medición al final de cada cúbit
        
        self.qc.draw(output="mpl")
        plt.show()
    
    
    def run_circuit(self):
        aer_sim = Aer.get_backend('aer_simulator')
        qobj = assemble(self.qc, shots=8192)
        self.job = aer_sim.run(qobj)
        # self.job = execute(self.qc, backend=self.real_device)
        # self.job_info = job_monitor(self.job)

    def get_results(self):
        self.results = self.job.result()
        return self.results.get_counts(self.qc)

    def results_formatting(self):
        count = Counts(self.results.get_counts(self.qc))
        results_list = count.int_outcomes()
        print("formatted",results_list)
        
        counts_final = []
        for ele in range(pow(2,self.qbits)):
            counts_final.append(results_list.get(ele, 0))

        probabilities = []
        for elem in counts_final:
            probabilities.append(round((elem / sum(counts_final))*100,2))
        
        
        print("Contador: ", counts_final)
        print("Probabilidades: ", probabilities)
    
        self.results = {
            "numQbits": "0",
            "resMatrix": [],
            "prob": [],
            "freq": []
        }
        
        self.results["numQbits"] = self.qbits
        self.results["prob"] = probabilities
        self.results["resMatrix"] = None