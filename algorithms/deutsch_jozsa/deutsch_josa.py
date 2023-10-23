from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer
import numpy as np
from qiskit_aer import AerSimulator


def dj_function(num_qubits):
    qc = QuantumCircuit(num_qubits + 1)
    if np.random.randint(0, 2):
        qc.x(num_qubits) # Flip the output qubit with 50% chance
    if np.random.randint(0, 2):
        return qc # Return constant circuit with 50% time
    
    # Next, choose half the possible input states
    on_states = np.random.choice(
        range(2**num_qubits),  # numbers to sample from
        2**num_qubits // 2,  # number of samples
        replace=False,  # makes sure states are only sampled once
    )
    
    def add_cx(qc, bit_string):
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == "1":
                qc.x(qubit)
        return qc
    
    for state in on_states:
        qc.barrier()
        qc = add_cx(qc, f"{state:0b}")
        qc.mct(list(range(num_qubits)), num_qubits)
        qc = add_cx(qc, f"{state:0b}")

    qc.barrier()

    fig = circuit_drawer(dj_function(3), output='mpl', filename="img/function.png")
    return qc

def compile_circuit(function: QuantumCircuit):
    n = function.num_qubits - 1
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    qc.compose(function, inplace = True)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    fig = circuit_drawer(qc, output='mpl', filename="img/circuit.png")
    
    return qc

def dj_algorithm(function: QuantumCircuit):
    qc = compile_circuit(function)

    result = AerSimulator().run(qc, shots=1, memory=True).result()
    measurements = result.get_memory()
    if "1" in measurements[0]:
        return "balanced"
    return "constant"

if __name__ == "__main__":
    
    print(dj_algorithm(dj_function(3)))