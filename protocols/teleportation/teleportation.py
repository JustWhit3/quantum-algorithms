from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import circuit_drawer

if __name__ == "__main__":
    
    # Create the circuit
    Q = QuantumRegister(1, "Q")
    A = QuantumRegister(1, "A")
    B = QuantumRegister(1, "B")
    a = ClassicalRegister(1, "a")
    b = ClassicalRegister(1, "b")
    
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
    circuit_drawer(circuit, output='mpl', filename='circuit.png')