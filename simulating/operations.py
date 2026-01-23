import numpy as np

state_vector = np.array([[1, 0]]).T # Initial state |0>
hadamard_gate = np.array([[1/np.sqrt(2), 1/np.sqrt(2)],[1/np.sqrt(2), -1/np.sqrt(2)]]) # Hadamard gate

superposition = np.dot(hadamard_gate, state_vector) # Apply Hadamard gate to create superposition
# print("Superposition state: ")
# print(superposition)
##########################################################################################################

# CNOT gate examples
cnot_1 = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]) # first qubit target, second qubit control

cnot_2 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]) # first qubit control, second qubit target


state_vector = np.kron(np.array([[1, 0]]), np.array([[0, 1]])).T
# print("Input: ")
# print(state_vector)

output = np.dot(cnot_1, state_vector)
# print("Output, when first qubit is the target, second is control: ")
# print(output)
##########################################################################################################

# Applying gates to larger systems Resizing single-qubit gates
pauli_x = np.array([[0,1],[1,0]])
print("Operator before growing: ")
print(pauli_x)

#starting tensor product with identity or the gate itself
operator = np.identity(2)

current = operator

for qubit in range(1, 3):
  if qubit == 1:
      #tensor product with identity
      current = np.kron(current, operator)
      print('here')
  else:
      #tensor product with the gate
      current = np.kron(current, pauli_x)

print("Operator after growing: ")
print(current)

# Applying the grown operator to a 3-qubit state
zero = np.array([[1, 0]]).T

state_vector = np.kron(zero, np.kron(zero, zero))
print("Initial State: ")
print(state_vector)

final = np.dot(current, state_vector)
print("Result after applying our operator: ")
print(final)