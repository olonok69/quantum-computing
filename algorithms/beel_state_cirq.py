import cirq

# Create a circuit
circuit = cirq.Circuit()

# Add two qubits in the circuit
(q0, q1) = cirq.LineQubit.range(2)

# Apply Hadamard to first qubit, 
# CNOT to second keeping first as control and second as target
circuit.append([cirq.H(q0), cirq.CNOT(q0, q1)])

# Add measurement step to both qubits
circuit.append([cirq.measure(q0), cirq.measure(q1)])

# Draw the circuit
print("Circuit:")
print(circuit)

# Get a simulator to run this circuit
simulator = cirq.Simulator()

# Simulate the circuit several times
result = simulator.run(circuit, repetitions=20)

# Display the results
print("Results:")
print(result)