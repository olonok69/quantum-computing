'''
Docstring for simulating.measurement
Simulating Measurement in Python
Explore how to simulate quantum measurements using Python and NumPy. Understand how to create quantum states and 
apply gates, then measure qubit states probabilistically. Gain hands-on experience with superposition and extracting 
quantum states, preparing you for classical simulation of quantum computers.
'''

import numpy as np
import math

state = np.array([[1/math.sqrt(2), 0-1j/math.sqrt(2)]]).T
print("State vector: ")
print(state)

one = np.array([[1, 0]]).T
conjugate_transpose = one.transpose() # taking the conjugate tranpose of the state we want to measure in

probability = np.abs(np.dot(conjugate_transpose, state))**2 # absolute value squared of inner product


# equal superposition measurement example
zero = np.array([[1, 0]]).T
hadamard = np.array([[1/np.sqrt(2), 1/np.sqrt(2)],[1/np.sqrt(2), -1/np.sqrt(2)]])

superposition = np.dot(hadamard, zero)

conjugate_transpose = np.array([[0, 1]])

measurement = np.abs(np.dot(conjugate_transpose, superposition))**2
print("Measurement result: ", measurement)

# Extracting the state
state_vector = np.array([[0, 1]]).T

# choose element from state_vector using weighted random and return its index
# flatten() converts the column vector into a 1-D array so probabilities sum correctly
probabilities = np.abs(state_vector.flatten())**2
probabilities = probabilities / probabilities.sum()

index = np.random.choice(a=len(state_vector), p=probabilities)

print("Measured state: ", index)


def measure(state_vector):
    # choose element from state_vector using weighted random and return its index
    probabilities = np.abs(state_vector.flatten())**2
    index = np.random.choice(a=len(state_vector), p=probabilities)
    return index

zero_count = one_count = 0
state_vector = np.array([[1, 0]]).T
hadamard = np.array([[1/np.sqrt(2), 1/np.sqrt(2)],[1/np.sqrt(2), -1/np.sqrt(2)]])
superposition = np.dot(hadamard, state_vector)

for _ in range(1000):
    result = measure(superposition) # measure the state and record the result
    if result == 0:
        zero_count +=1 
    elif result == 1:
        one_count += 1

print(f'0: {zero_count} | 1: {one_count}')      