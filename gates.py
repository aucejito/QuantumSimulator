import numpy as np

gates = {
    'x': {
        "id":"x",
        "name":"Pauli-X",
        "symbol":"./images/X.jpg",
        "matrix": np.array([[0,1],[1,0]])
    },
    'y': {
        "id":"y",
        "name":"Pauli-Y",
        "symbol":"./images/Y.jpg",
        "matrix": np.array([[0,-1j],[1j,0]])
    },
    'z': {
        "id":"z",
        "name":"Pauli-Z",
        "symbol":"./images/Z.jpg",
        "matrix": np.array([[1,0],[0,-1]])
    },
    'h': {
        "id":"h",
        "name":"Hadamard",
        "symbol":"./images/H.jpg",
        "matrix": 1/np.sqrt(2)*np.array([[1,1],[1,-1]])
    },
    'cx': {
        "id":"cx",
        "name":"Controlled Not (CNOT/CX)",
        "symbol":"./images/CX.jpg",
        "matrix": np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    },
    'id': {
        "id":"id",
        "name":"Identity",
        "symbol":"./images/ID.jpg",
        "matrix": np.array([[1,0],[0,1]])
    },
    'one':{
        "id":"one",
        "name":"Constant-One",
        "symbol":".",
        "matrix": np.array([0,1])
    },
    'zero':{
        "id":"zero",
        "name":"Constant-Zero",
        "symbol":".",
        "matrix": np.array([1,0])
    }
}
