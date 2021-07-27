import gates as gt

class Util():
    def loadGateData(gate):
        gate = gate.lower()
        data = gt.gates.get(gate)
        return data