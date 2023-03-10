from django.http import JsonResponse
from django.shortcuts import render
import json

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, IBMQ
from qiskit.tools.monitor import job_monitor

IBMQ.enable_account('XXXX')
provider = IBMQ.get_provider(hub='ibm-q')

def home(request):
    return render(request, 'index.html', {})

def random(request):

    print(request.body)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode);

    device = body['device']

    min = int(body['min'])
    max = int(body['max'])

    backend = provider.get_backend(device)

    if device == "ibmq_qasm_simulator":
        num_q = 32
    else:
        num_q = 5

    q = QuantumRegister(num_q, 'q')
    c = ClassicalRegister(num_q, 'c')

    circuit = QuantumCircuit(q, c)
    circuit.h(q)  # Applies hadamard gate to all qubits
    circuit.measure(q, c)  # Measures all qubits


    job = execute(circuit, backend, shots=1)

    print('Executing Job...\n')
    job_monitor(job)
    counts = job.result().get_counts()

    print('RESULT: ', counts, '\n')
    print('Press any key to close')

    result = int(counts.most_frequent(), 2)

    result1 = min + result % (max+1 - min)

    print(result1)

    response = JsonResponse({'result': result1})
    return response