import cirq

"""Simulate each of the circuits."""
simulator = cirq.Simulator()

"""Operations to query all possible functions on two bits.
Two of these functions are constant, and six of these functions are balanced.
"""
# Define three qubits to use.
q0, q1, q2, q3 = cirq.LineQubit.range(4)

# Define the operations to query each of the two constant functions.
constant = (
    [], 
    [cirq.X(q2)]
)

# Define the operations to query each of the six balanced functions.
balanced = (
    [cirq.CNOT(q0, q3), cirq.CNOT(q1, q3), cirq.CNOT(q2, q3), cirq.X(q3)]
)

def dj_circuit(oracle):
    # Phase kickback trick.
    yield cirq.X(q3), cirq.H(q3)

    # Get an equal superposition over input bits.
    yield cirq.H(q0), cirq.H(q1), cirq.H(q2)

    # Query the function.
    yield oracle

    # Use interference to get result, put last qubit into |1>.
    yield cirq.H(q0), cirq.H(q1), cirq.H(q2), cirq.H(q3)

    # Use a final OR gate to put result in final qubit.
    yield cirq.X(q0), cirq.X(q1), cirq.X(q2), cirq.X(q3), cirq.CCX(q0, q1, q2), cirq.CNOT(q2, q3)
    yield cirq.measure(q3)


"""Simulate the Deutsch-Jozsa circuit and check the results."""
print("Measurement on balanced function:")
oracle = balanced[0]
print('Balanced Circuit:')
print(cirq.Circuit(dj_circuit(oracle)))
result = simulator.run(cirq.Circuit(dj_circuit(oracle)), repetitions=1)
print(f'Measurement result on balanced: q{result}')

print("Measurement on constant function:")
oracle = constant[0]
print('\nConstant Circuit:')
print(cirq.Circuit(dj_circuit(oracle)))
result = simulator.run(cirq.Circuit(dj_circuit(oracle)), repetitions=1)
print(f'Measurement result on constant circuit: q{result}')
