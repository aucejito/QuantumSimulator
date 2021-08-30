from Util import Util
import numpy as np
from Circuit import Circuit as ct



class Simulation():

    results = None

    def simulate(self, circuit: ct, shots: int):

        # TODO: toda la lógica de la simulación
        # Bucle for por cada puerta, teniendo en cuenta las puertas de dos qbits.
        # Lo anterior ejecutarlo 'shots' veces y sacar la media.
        # for i in range(len(circuit.gates)):
        for qbit in circuit.gates:
            self.max = 0
            if len(qbit) > self.max:
                self.max = len(qbit)
        
        for qbit in circuit.gates:
            if len(qbit) < self.max:
                qbit.extend([int('1' * (self.max - len(qbit)))])

        transposed = list(map(list, zip(*circuit.gates)))
        
        print(transposed)

        res = None

        for qbit in circuit.gates:
            initial_res = 0
            for gate in qbit:
                if gate != 1:
                        matrix = gate.matrix
                        res: np.ndarray = np.matmul(matrix, circuit.initialState) if initial_res == 1  else np.matmul(matrix, res)        
                initial_res += 1

            res = res.tolist()
            density = []
            i = 0
            while i < len(res):
                density.append(res[i] / sum(res))
                i += 1

    

        results = {
            "numQbits": "0",
            "resMatrix": [],
            "prob": [],
            "freq": []
        }
        
        results["numQbits"] = len(circuit.gates)
        results["prob"] = density
        results["resMatrix"] = res

        return results
