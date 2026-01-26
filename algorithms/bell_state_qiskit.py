"""
Bell State Creation using Qiskit

This script demonstrates how to create a Bell state (maximally entangled state)
using IBM's Qiskit framework. The Bell state is: (|00> + |11>) / sqrt(2)

Updated for Qiskit 1.x and qiskit-aer 0.17+
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Use Aer's simulator (updated for Qiskit 1.x)
simulator = AerSimulator()

# Create a Quantum Circuit acting on 2 qubits with 2 classical bits for measurement
circuit = QuantumCircuit(2, 2)

# Add a H gate on qubit 0
circuit.h(0)

# Add a CX (CNOT) gate on control qubit 0 and target qubit 1
circuit.cx(0, 1)

# Map the quantum measurement to the classical bits
circuit.measure([0, 1], [0, 1])

print("="*70)
print("BELL STATE CREATION WITH QISKIT")
print("="*70)
print("\nQuantum Circuit:")
print(circuit.draw(output='text'))

# Compile the circuit for the simulator
# (transpile optimizes the circuit for the backend)
compiled_circuit = transpile(circuit, simulator)

# Execute the circuit on the simulator with 1000 shots
print("\nExecuting circuit with 1000 shots...")
job = simulator.run(compiled_circuit, shots=1000)

# Grab results from the job
result = job.result()

# Get measurement counts
counts = result.get_counts(circuit)
print("\n" + "="*70)
print("MEASUREMENT RESULTS")
print("="*70)
print(f"\nTotal counts: {counts}")
print(f"\nState |00>: {counts.get('00', 0)} times ({counts.get('00', 0)/10:.1f}%)")
print(f"State |11>: {counts.get('11', 0)} times ({counts.get('11', 0)/10:.1f}%)")
print("\nExpected: ~50% |00> and ~50% |11> (Bell state)")
print("="*70)

# Optional: Create histogram visualization
try:
    print("\nGenerating histogram visualization...")
    fig = plot_histogram(counts)
    plt.savefig('bell_state_histogram.png', dpi=300, bbox_inches='tight')
    print("Histogram saved as 'bell_state_histogram.png'")
except Exception as e:
    print(f"Note: Could not save histogram visualization: {e}")

print("\n✅ Bell state successfully created and measured!")
