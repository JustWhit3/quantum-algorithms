from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer
from qiskit_aer.primitives import Sampler
import numpy as np
from numpy.random import randint
import matplotlib.pyplot as plt


def chsh_game(strategy):
    x, y = randint(0, 2), randint(0, 2)
    a, b = strategy(x, y)
    if (a != b) == (x & y):
        return 1  # Win
    return 0  # Lose


def chsh_circuit(x, y):
    
    # Build the circuit starting from |+> state
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.barrier()
    
    # Apply Alice actions
    if x == 0:
        circuit.ry(0, 0)
    else:
        circuit.ry(-np.pi/2, 0)
    circuit.measure(0, 0)
    
    # Apply Bob actions
    if y == 0:
        circuit.ry(-np.pi/4, 1)
    else:
        circuit.ry(np.pi/4, 1)
    circuit.measure(1, 1)
    
    # Save the circuit
    circuit_drawer(circuit, output='mpl', filename='img/circuit.png')
    plt.close()
    return circuit


def quantum_strategy(x, y):
    result = Sampler().run(chsh_circuit(x, y), shots=1).result()
    statistics = result.quasi_dists[0].binary_probabilities()
    bits = list(statistics.keys())[0]
    a, b = bits[0], bits[1]
    
    return a, b

def classical_strategy(x, y):
    if x == 0:
        a = 0
    elif x == 1:
        a = 1
        
    if y == 0:
        b = 1
    elif y == 1:
        b = 0

    return a, b


if __name__ == "__main__":
    NUM_GAMES = 1000
    
    # Quantum case
    TOTAL_SCORE_QUANTUM = 0
    for _ in range(NUM_GAMES):
        TOTAL_SCORE_QUANTUM += chsh_game(quantum_strategy)
    print("Fraction of quantum games won:", TOTAL_SCORE_QUANTUM / NUM_GAMES)
    
    # Classical case
    TOTAL_SCORE_CLASSIC = 0
    for _ in range(NUM_GAMES):
        TOTAL_SCORE_CLASSIC += chsh_game(classical_strategy)
    print("Fraction of classic games won:", TOTAL_SCORE_CLASSIC / NUM_GAMES)