import numpy as np

# Representing the computational basis states#
zero = np.array([[1, 0]]).T 
one = np.array([[0, 1]]).T

print("State |0> is:") 
print(zero)
print("State |1> is:")
print(one)

print("Shape of state |0> is: ", zero.shape) 
print("Shape of state |1> is: ", one.shape)

# Representing a superposition state
import numpy as np
import math

eq_superposition = np.array([[1/math.sqrt(2), 1/math.sqrt(2)]]).T

print("Equal superposition state: ")
print(eq_superposition)

# Complex entries in the state vector

complex_state = np.array([[1/math.sqrt(2), 1j/math.sqrt(2)]]).T #adding the 'j' for complex numbers

print("A state with complex-valued entries: ")
print(complex_state)

# Multi-qubit states
import numpy as np

q1 = np.array([[1, 0]]).T
q2 = np.array([[1, 0]]).T

system = np.kron(q1, q2) #tensor product of q1 and q2
print("The system is in state: ")
print(system)

# more complex

import numpy as np

q1 = np.array([[0, 1]]).T
q2 = np.array([[1, 0]]).T
q3 = np.array([[0, 1]]).T

system = np.kron(q1, np.kron(q2, q3)) #tensor product of q1 and q2 and q3
print("The system is in state: ")
print(system)