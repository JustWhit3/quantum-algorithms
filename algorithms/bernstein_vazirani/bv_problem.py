from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer
import sys
sys.path.append("..")
from deutsch_jozsa.deutsch_josa import compile_circuit
from qiskit_aer import AerSimulator


def bv_function(s):
    qc = QuantumCircuit(len(s) + 1)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(index, len(s))
    circuit_drawer(qc, output='mpl', filename="img/bv_function.png")
    return qc


def bv_algorithm(function: QuantumCircuit):
    qc = compile_circuit(function)
    circuit_drawer(qc, output='mpl', filename="img/circuit.png")
    result = AerSimulator().run(qc, shots=1, memory=True).result()
    return result.get_memory()[0]


if __name__ == "__main__":
    print(bv_algorithm(bv_function("01001")))