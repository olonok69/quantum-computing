# Simulating Quantum Gates in Python
import numpy as np
import math

# Basis states |0> and |1>
zero = np.array([[1, 0]]).T
one = np.array([[0, 1]]).T

# Single-qubit gates (2x2 matrices)
identity = np.eye(2)
pauli_x = np.array([[0, 1], [1, 0]])
pauli_y = np.array([[0, -1j], [1j, 0]])
pauli_z = np.array([[1, 0], [0, -1]])
hadamard = (1 / math.sqrt(2)) * np.array([[1, 1], [1, -1]])


cnot_1 = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]) # first qubit target, second qubit control

cnot_2 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]) # first qubit control, second qubit target


def apply(gate: np.ndarray, state: np.ndarray) -> np.ndarray:
	"""Apply a gate matrix to a state vector (supports 1+ qubits)."""
	return gate @ state


if __name__ == "__main__":
	print("|0> =\n", zero)
	print("|1> =\n", one)
	print("CNOT when first qubit is the target and second is control: ")
	print(cnot_1)
	print("CNOT when second qubit is the target, and first is control: ")
	print(cnot_2)
	# print("Identity|0> =\n", apply(identity, zero))
	# print("X|0> (should be |1>) =\n", apply(pauli_x, zero))
	# print("Y|0> (phase-added |1>) =\n", apply(pauli_y, zero))
	# print("Z|0> (unchanged) =\n", apply(pauli_z, zero))
	# print("H|0> (superposition) =\n", apply(hadamard, zero))
	# print("H|1> (superposition) =\n", apply(hadamard, one))
	#print("CNOT|01> =\n", apply(cnot_1, np.kron(zero, one)))
	print("CNOT|10> =\n", apply(cnot_2, np.kron(one, zero)))