from itertools import product
import numpy as np
from Circuit import Circuit as ct
import math


class Simulation():

    states = []
    results = None
    max = 0
    def simulate(self, circuit: ct, shots: int):

        # TODO: toda la lógica de la simulación
        # Bucle for por cada puerta, teniendo en cuenta las puertas de dos qbits.
        # Lo anterior ejecutarlo 'shots' veces y sacar la media.
        # for i in range(len(circuit.gates)):
       
        final_states = []
        density = []
        res = None
        probs = []
        initial_res = 0
        control = False
        for column in circuit.serialized:
            for gate in column:
                if gate != 1:
                    if gate.id == 'c':
                        control = True
                    else:
                        if control:
                            prev_state = self.states[len(self.states)-len(column)]
                            res =  prev_state[0]if initial_res < len(column)  else [prev_state[0]*res[0], prev_state[1]*res[1]]
                        matrix = gate.matrix
                        res = np.matmul(matrix, circuit.initialState) if initial_res < len(column)  else np.matmul(matrix, res)
                        self.states.append(res)
                        circuit.qbits.update({column.index(gate):res.tolist()})
                initial_res += 1
            #final_states = list(circuit.qbits.values())
            print(final_states)
            
            for sublist in final_states:
                if(sublist!=1):
                    i=0
                    while i < len(sublist):
                        density.append(sublist[i] / sum(sublist))
                        i+= 1
            probs.append(density)
        # for qbit in circuit.gates:
        #     initial_res = 0
        #     for gate in qbit:
        #         if gate != 1:
        #                 matrix = gate.matrix
        #                 res: np.ndarray = np.matmul(matrix, circuit.initialState) if initial_res == 1  else np.matmul(matrix, res)        
        #         initial_res += 1

            # res = res.tolist()
            # print(res)
            # density = []
            # i = 0
            # while i < len(res):
            #     density.append(res[i] / sum(res))
            #     i += 1
            probabilities = []
        if(len(probs[0]) != 2):
            
            multiplied = []
            index1 = 0
            qbit1_prob0 = probs[0][0]
            qbit1_prob1 = probs[0][1]

            for item in probs[0]:
                multiplied.append(item)
            multiplied.pop(0)
            multiplied.pop(0)

            print("multi",multiplied)
            for times in range(len(multiplied)):
                probabilities.append(qbit1_prob0*multiplied[index1])
                probabilities.append(qbit1_prob1*multiplied[index1])
                index1+=1
        else:
            probabilities.append(probs[0][0])
            probabilities.append(probs[0][1])


        probfinal = []
        print("probabilidades ", probabilities)
        for item in probabilities:
            probfinal.append(int(item*100))

        print(probfinal)

        results = {
            "numQbits": "0",
            "resMatrix": [],
            "prob": [],
            "freq": []
        }
        
        results["numQbits"] = 1 if len(probfinal) == 2 else int(math.sqrt(len(probfinal)))
        results["prob"] = probfinal
        results["resMatrix"] = res


        print("resultados: ", results)
        return results

class Simulation1():

    results = None
    states = []
    current_state = []
    num_qbits = 0
    def setup(self, circuit : ct):
        qbits = []
        for column in circuit.serialized:
            counter = 0
            for item in reversed(column):
                if item == 1:
                    counter +=1
                else:
                    break
            qbits.append(len(column)-counter)
        self.num_qbits = max(qbits)

        #Initialize current_state
        for i in range(self.num_qbits):
            self.current_state.append = []

    def simulate(self, circuit : ct, shots: int):
        control = False
        initial_res = 0
        density = []
        probs = []
        cto = circuit.serialized
        for col in range(0, len(cto)):
            for gate in cto[col]:
                if gate != 1:
                    if gate.id == 'c':
                        control = True
                    else:
                        if control:
                            state = [circuit.qbits.get(cto[col-1].index(previous_gate)),circuit.qbits.get(cto[col].index(gate))]
                            
                        
                            controlled_gate = np.append(np.array([[1,0,0,0],[0,1,0,0]]), np.pad(gate.matrix, ((0,0),(2,0)), 'constant'))

                            #print("controlled: ", controlled_gate)
                            #res = np.matmul(state, )
                        else:
                            matrix = gate.matrix
                            res = np.matmul(matrix, circuit.initialState) if initial_res < len(cto[col])  else np.matmul(matrix, circuit.qbits.get(cto[col].index(gate)))
                        self.states.append(res)
                        circuit.qbits.update({cto[col].index(gate):res.tolist()})
                        previous_gate = gate
                initial_res += 1
        final_states = list(circuit.qbits.values())

        final_states_aux = []
        final_states.reverse()
        for item in final_states:
            if(item != 1):
                final_states_aux.append(item)

        final_states_aux.reverse()

        for sublist in final_states_aux:
            density = []
            if(sublist!=1):
                i=0
                while i < len(sublist):
                    density.append(np.absolute(sublist[i]) / sum(np.absolute(sublist)))
                    i+= 1
                probs.append(density)

        probabilities = []

        for item in self.lcomp(probs, len(probs)-1):
            probabilities.append(item*100)
    
        
        print("probabilities: ", probabilities)

        results = {
            "numQbits": "0",
            "resMatrix": [],
            "prob": [],
            "freq": []
        }
        
        results["numQbits"] = len(probs)
        results["prob"] = probabilities
        results["resMatrix"] = res

        return results

    def lcomp(self, l, i):
        if i == 0:
            return [l[i][0], l[i][1]]
        return [l[i][0] * x for x in self.lcomp(l, i-1)] + [l[i][1] * x for x in self.lcomp(l, i-1)]