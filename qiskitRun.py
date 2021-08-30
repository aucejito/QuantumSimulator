from qiskit.tools.monitor import job_monitor
from qiskit import *
#IBMQ.save_account('c96142dc9ba95ead8c9746ed6f2b05f31608e9cfe347563a1b3c2ea7e0fd7ec67829832d8bab02ba1b4cb5a7ffb8d24bb1cf176c308a93611cfe1369f1b4761d')
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
real_device = provider.get_backend('ibmq_santiago')
qc = QuantumCircuit(2,2)
qc.x(0)
qc.cx(0,1)
print(qc.draw(output='text'))
qc.measure_all()

# qr = QuantumRegister(2, 'a') #cto.size
# qc.add_register(qr)

# #Add gates from OBJECT CIRCUIT
# for gate in gates:
#     if gate.id == 'h':
#         qc.h(gate.qbit)
#     elif gate.id == 'x':
#         qc.x(gate.qbit)
#     elif gate.id == 'y':
#         qc.y(gate.qbit)
#     elif gate.id == 'z':
#         qc.z(gate.qbit)
#     elif gate.id == 'cx':
#         qc.cx(gate.controlqbit, gate.targetqbit)

# #Job monitor
# job = execute(qc, backend=real_device)
# print(job_monitor(job))

# result = job.result()
# print(result.get_counts(qc))