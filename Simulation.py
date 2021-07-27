from Util import Util
import numpy as np
import Circuit as ct


class Simulation():

    def simulate(circuit: ct.Circuit, shots: int):

        # TODO: toda la lógica de la simulación
        # Bucle for por cada puerta, teniendo en cuenta las puertas de dos qbits.
        # Lo anterior ejecutarlo 'shots' veces y sacar la media.
        # for i in range(len(circuit.gates)):

        matrix = Util.loadGateData('h')
        matrix = matrix.get("matrix")
        res: np.ndarray = np.matmul(matrix, circuit.initialState)
        res.tolist()
        density = []
        i = 0
        while i < len(res):
            density.append(res[i] / sum(res))
            i += 1

        results = {
            "numQbits": "0",
            "prob": [],
        }

        results["numQbits"] = ct.Circuit()
        results["prob"] = density

        return results
