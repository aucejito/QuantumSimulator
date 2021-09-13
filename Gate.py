import json
import numpy as np
from gates import gates

class Gate():

    id = ''
    name = ''
    symbol = ''
    matrix = None
    path_to_img = ''

    def __init__(self, gate):
        gate = gate.lower()
        data = gates.get(gate)
        self.id = data['id']
        self.name = data['name']
        self.symbol = data['name']
        self.matrix = data['matrix']
        self.path_to_img = None

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
