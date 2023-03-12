from django.http import JsonResponse
from django.shortcuts import render
import json

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy
from qiskit.circuit.library import Permutation
IBMQ.enable_account('XXX')
#provider = IBMQ.get_provider(hub='ibm-q')

provider = IBMQ.get_provider(hub='ibm-q-education', group='uni-antioquia-2',project='quantum-alg')
ibmq_backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 7 and 
                                   not x.configuration().simulator and x.status().operational==True))

print("The least busy quantum computer now is",ibmq_backend)

def home(request):
    return render(request, 'index.html', {})

def random(request):

    print(request.body)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode);

    device = body['device']

    min = int(body['min'])
    max = int(body['max'])

    num_q = 7
    if device == "ibmq_qasm_simulator":
        backend = provider.get_backend('ibmq_qasm_simulator')
    elif device == 'least_busy_7qubits':
        backend = ibmq_backend

    q = QuantumRegister(num_q, 'q')
    c = ClassicalRegister(num_q, 'c')
    circuit = QuantumCircuit(q, c)
    circuit.t(q[0:4])
    circuit.s(q[0:4])
    circuit.h(q[0:4])
    circuit= circuit.compose(Permutation(num_qubits = num_q)) # not in-place

    circuit.measure(q, c)

    job = execute(circuit, backend, shots=1)

    print('Executing Job...\n')
    job_monitor(job)
    counts = job.result().get_counts()

    print('RESULT: ', counts, '\n')

    result = int(counts.most_frequent(), 2)

    result1 = min + result % (max+1 - min)

    print(result1)

    response = JsonResponse({'result': result1})
    return response