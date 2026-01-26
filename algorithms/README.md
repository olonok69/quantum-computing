# Quantum Algorithms - Qiskit Implementation

This directory contains quantum algorithms implemented using IBM's Qiskit framework.

## Setup

The required packages are already installed in your virtual environment:
- `qiskit` (2.3.0)
- `qiskit-aer` (0.17.2)
- `matplotlib` (for visualizations)

## Available Scripts

### bell_state_qiskit.py

Creates and measures a Bell state using Qiskit.

**What it does:**
- Creates a 2-qubit Bell state: (|00⟩ + |11⟩)/√2
- Uses Hadamard gate on qubit 0
- Applies CNOT gate with control=0, target=1
- Measures both qubits 1000 times
- Generates a histogram visualization

**Usage:**
```bash
python algorithms\bell_state_qiskit.py
```

**Output:**
- Prints the quantum circuit diagram
- Shows measurement statistics
- Saves histogram as `bell_state_histogram.png`

**Expected Results:**
~50% |00⟩ and ~50% |11⟩ (perfect entanglement)

## Qiskit Version Notes

This code is updated for **Qiskit 1.x** and **qiskit-aer 0.17+**.

### Key Changes from Older Versions:
- Import changed from `qiskit.providers.aer.QasmSimulator` to `qiskit_aer.AerSimulator`
- Aer is now a separate package (`qiskit-aer`)
- The simulator is now `AerSimulator()` instead of `QasmSimulator()`

### Migration Guide

If you have old Qiskit code, update your imports:

**Old (Qiskit 0.x):**
```python
from qiskit.providers.aer import QasmSimulator
simulator = QasmSimulator()
```

**New (Qiskit 1.x):**
```python
from qiskit_aer import AerSimulator
simulator = AerSimulator()
```

## Comparison with Custom Simulator

You can compare this Qiskit implementation with the custom simulator:

**Custom Simulator:**
```bash
python simulating\quantum_simulator.py -q 2 -c "h:0,cx:0-1" --visualize
```

**Qiskit:**
```bash
python algorithms\bell_state_qiskit.py
```

Both should give similar results (~50/50 distribution between |00⟩ and |11⟩).

## Further Reading

- [Qiskit Documentation](https://docs.quantum.ibm.com/)
- [Qiskit Tutorials](https://learning.quantum.ibm.com/)
- [Bell State (Wikipedia)](https://en.wikipedia.org/wiki/Bell_state)
