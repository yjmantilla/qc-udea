from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, execute,IBMQ
from qiskit.circuit.library import Permutation
from qiskit.tools.monitor import job_monitor

IBMQ.enable_account('XXXX')
provider = IBMQ.get_provider(hub='ibm-q')

backend = provider.get_backend('ibmq_qasm_simulator')


q = QuantumRegister(7, 'q')
c = ClassicalRegister(7, 'c')

########### PERMUTATION WITH PATTERN 7,0,6,1,5,2,4,3 
circuit = QuantumCircuit(q, c)

circuit.t(q[0])
circuit.s(q[1])
circuit.h(q[2])

circuit= circuit.compose(Permutation(num_qubits = 7, pattern = [0,6,1,5,2,4,3])) # not in-place

circuit.measure(q, c)

job = execute(circuit, backend, shots=100)
job_monitor(job)

counts = job.result().get_counts()

print(circuit)
print(counts)

