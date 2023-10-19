
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import circuit_drawer, plot_histogram
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

def make_circuit():
    
    # Initialize the cirucit in the first bell state
    rng = QuantumRegister(1, "Randomizer")
    A = QuantumRegister(1, "A")
    B = QuantumRegister(1, "B")
    A_c = ClassicalRegister(1, "Alice c")
    A_d = ClassicalRegister(1, "Alice d")
    circuit = QuantumCircuit(rng, A, B, A_d, A_c)
    circuit.h(A)
    circuit.cx(A, B)
    circuit.barrier()
    
    # Select c and d randomly
    circuit.h(rng)
    circuit.measure(rng, A_c)
    circuit.h(rng)
    circuit.measure(rng, A_d)
    circuit.barrier()
    
    # Apply Alice operations based on the bit value
    with circuit.if_test((A_d, 1), label="Z"):
        circuit.z(A)
    with circuit.if_test((A_c, 1), label="X"):
        circuit.x(B)
    circuit.barrier()
        
    # Perform last Bob actions and measurements
    circuit.cx(A, B)
    circuit.h(A)
    circuit.barrier()
    B_c = ClassicalRegister(1, "Bob c")
    B_d = ClassicalRegister(1, "Bob d")
    circuit.add_register(B_d)
    circuit.add_register(B_c)
    circuit.measure(A, B_d)
    circuit.measure(B, B_c)
    
    # Save the circuit
    circuit_drawer(circuit, output='mpl', filename='img/circuit.png')
    return circuit


def measure(circuit):
    result = AerSimulator().run(circuit).result()
    statistics = result.get_counts()
    fig = plot_histogram(statistics)
    plt.tight_layout()
    fig.savefig("img/simulator.png")


if __name__ == "__main__":
    circuit = make_circuit()
    measure(circuit)