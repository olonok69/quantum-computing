import numpy as np

# Define a simple quantum gate (Pauli-X gate) and apply it to a qubit state
state_vector = np.array([[1, 0]]).T
# print("Initial State: ")
# print(state_vector)

pauli_x = np.array([[0, 1], [1, 0]])
# print("Applying the Pauli-X Gate, defined as follows: ")
# print(pauli_x)

final_state = np.dot(pauli_x, state_vector) # taking the product of the gate and state vector 
print("The final state after application is: ")
print(final_state)

# Define a Hadamard gate and apply it to a qubit state to create superposition
state_vector = np.array([[1, 0]]).T
hadamard_gate = np.array([[1/np.sqrt(2), 1/np.sqrt(2)],[1/np.sqrt(2), -1/np.sqrt(2)]])

superposition = np.dot(hadamard_gate, state_vector)
print("Superposition state: ")
print(superposition)

# Define CNOT gate matrices
cnot_1 = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]) # first qubit target, second qubit control

cnot_2 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]) # first qubit control, second qubit target


state_vector = np.kron(np.array([[1, 0]]), np.array([[0, 1]])).T
print("Input: ")
print(state_vector)

# Resizing single-qubit gates#
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


zero = np.array([[1, 0]]).T

state_vector = np.kron(zero, np.kron(zero, zero))
print("Initial State: ")
print(state_vector)

final = np.dot(current, state_vector)
print("Result after applying our operator: ")
print(final)