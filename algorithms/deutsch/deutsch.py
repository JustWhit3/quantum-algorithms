from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer
from qiskit_aer import AerSimulator


def deutsch_function(case: int):
    if case not in [1, 2, 3, 4]:
        raise ValueError("'case' must be in 1, 2, 3 or 4.")

    func = QuantumCircuit(2)
    if case in [2, 3]:
        func.cx(0, 1)
    if case in [3, 4]:
        func.x(1)
    
    return func


def make_circuit(function: QuantumCircuit):
    n = function.num_qubits - 1 # Because last qubit is used as auxiliary qubit
    circuit = QuantumCircuit(n + 1, n)
    
    circuit.x(n)
    circuit.h(range(n + 1))
    
    circuit.barrier()
    circuit.compose(function, inplace = True)
    circuit.barrier()
    
    circuit.h(range(n))
    circuit.measure(range(n), range(n))

    return circuit


def algorithm(function: QuantumCircuit):
    circuit = make_circuit(function)
    
    result = AerSimulator().run(circuit, shots = 1, memory = True).result()
    measurements = result.get_memory()
    if measurements[0] == "0":
        return "constant"
    return "balanced"
    

if __name__ == "__main__":
    circuit = make_circuit(deutsch_function(3))
    fig = circuit_drawer(circuit, output='mpl', filename="img/circuit.png")
    print(algorithm(deutsch_function(3)))
    
