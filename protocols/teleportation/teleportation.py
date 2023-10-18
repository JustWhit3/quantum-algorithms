from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import circuit_drawer, plot_histogram
from qiskit.circuit.library import UGate
from qiskit.result import marginal_distribution
from qiskit_aer import AerSimulator

from numpy import random, pi
import matplotlib.pyplot as plt


def make_circuit(Q, A, B, a, b):

    # Initialize A and B in the first bell state
    circuit = QuantumCircuit(Q, A, B, a, b)
    circuit.h(A)
    circuit.cx(A, B)
    circuit.barrier()
    
    # Construct the circuit
    circuit.cx(Q, A)
    circuit.h(Q)
    circuit.barrier()
    
    # Measure A and B qubits
    circuit.measure(A, a)
    circuit.measure(Q, b)
    circuit.barrier()
    
    # B apply gates only in certain conditions
    with circuit.if_test((a, 1)):
        circuit.x(B)
    with circuit.if_test((b, 1)):
        circuit.z(B)
    
    # Save circuit
    circuit_drawer(circuit, output='mpl', filename='img/circuit.png')
    return circuit


def test_circuit(circuit, Q, A, B, a, b):

    # Create a random gate
    random_gate = UGate(
        theta=random.random() * 2 * pi,
        phi=random.random() * 2 * pi,
        lam=random.random() * 2 * pi,
    )

    # Create the test circuit
    test_circuit = QuantumCircuit(Q, A, B, a, b)
    test_circuit.append(random_gate, Q)
    test_circuit.barrier()
    test_circuit = test_circuit.compose(circuit)
    test_circuit.barrier()
    test_circuit.append(random_gate.inverse(), B)
    result = ClassicalRegister(1, "Result")
    test_circuit.add_register(result)
    test_circuit.measure(B, result)
    
    # Save test circuit
    circuit_drawer(test_circuit, output='mpl', filename='img/test_circuit.png')
    
    # Run the Aer simulator
    results = AerSimulator().run(test_circuit).result()
    statistics = results.get_counts()
    filtered_statistics = marginal_distribution(statistics, [2])
    fig = plot_histogram(filtered_statistics)
    plt.tight_layout()
    fig.savefig("img/simulator.png")


if __name__ == "__main__":
    
    # Create the circuit
    Q = QuantumRegister(1, "Q")
    A = QuantumRegister(1, "A")
    B = QuantumRegister(1, "B")
    a = ClassicalRegister(1, "a")
    b = ClassicalRegister(1, "b")
    circuit = make_circuit(Q, A, B, a, b)
    
    # Test the circuit
    test_circuit(circuit, Q, A, B, a, b)
