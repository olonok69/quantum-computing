# Quantum Computing Playground

A hands-on collection of scripts, notebooks, and notes that explore quantum computing concepts using Qiskit, Cirq, PennyLane, and a custom NumPy-based simulator. This repo mixes beginner-friendly explanations with runnable demos for Grover, Deutsch-Jozsa, Shor (toy example), and state-vector simulation.

## Repository Map

```
.
├── algorithms/                 # Qiskit-based algorithm snippets
├── DJ-Algorithm/               # Deutsch-Jozsa in Qiskit and Cirq
├── docs/                       # Beginner-friendly guides (EN/ES)
├── fundamentals/               # Grover-style oracle and diffuser demos
├── Grover/                     # Grover in Qiskit and Cirq
├── IBM-Quantum-Platform/       # QASM and Qiskit examples for IBM platform
├── Notebook/                   # Jupyter notebooks (qOSF tasks, random walk)
├── optimize_quantum_circuit/   # PennyLane cost landscape visualization
├── shor/                       # Shor (toy N=15) in Qiskit and Cirq
├── simulating/                 # Custom NumPy simulator + CLI + plots
├── quantum_results.html        # Plotly output (generated)
├── grover_circuit.png          # Qiskit Grover circuit output
├── bell_state_histogram.png    # Qiskit Bell-state histogram output
└── References.md               # External references and reading list
```

## Quick Start

### 1) Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2) Install core dependencies

```powershell
python -m pip install qiskit qiskit-aer cirq pennylane matplotlib numpy plotly
```

### 3) Run a few demos

```powershell
python fundamentals\main.py
python Grover\qiskit_grover.py
python DJ-Algorithm\main_qiskit.py
python simulating\quantum_simulator.py --visualize
```

## Documentation

- docs/quantum_computing_explained.md: Plain-language introduction with analogies and use cases.
- docs/computacion_cuantica_explicada.md: Spanish version of the same guide.
- README.es.md: Spanish overview of the repo structure and highlights.

## Algorithms and Demos by Folder

### algorithms/
- bell_state_qiskit.py: Builds a Bell pair, measures it, and saves a histogram to bell_state_histogram.png.
- beel_state_cirq.py: Cirq-based Bell-state example.

### DJ-Algorithm/
- main_qiskit.py: Deutsch-Jozsa with a balanced/constant oracle, outputs dj_circuit.png and dj_histogram.png.
- main.cirq.py: Deutsch-Jozsa in Cirq using a small 3-qubit input + ancilla.
- dj_circuit.txt: Notes for the circuit layout.

### Grover/
- qiskit_grover.py: Grover search with a 3-qubit oracle marking |101> and |110>, saves grover_circuit.png.
- cirq_grover.py: Grover search with a 2-qubit oracle and ancilla, prints sampled results.

### shor/
- shor_qiskit.py: Shor toy demo for N=15 using Qiskit Aer. Supports CLI parameters for N (fixed to 15 in this demo) and a (one of 2,7,8,11,13).
  - Example: `python shor\shor_qiskit.py -n 15 -a 7`
- shor_cirq.py: Shor order-finding circuit using Cirq arithmetic operations. Requires a Cirq version that provides ArithmeticGate support.

### fundamentals/
- main.py: Builds a Grover-style SAT oracle (XOR clauses), a diffuser, and runs the circuit in Aer. Saves a histogram to fundamentals/output/my_circuit.png.

### optimize_quantum_circuit/
- surface_plot.py: PennyLane-based cost-landscape visualization and optimizer trajectories.
- hello_pennylane.ipynb: Interactive notebook for variational circuits and optimizers.

### simulating/
- quantum_simulator.py: A full-featured NumPy simulator with CLI and Plotly visualizations.
- examples.py: Multiple prebuilt circuits.
- QUICKSTART.md and README.md: Usage, CLI arguments, and troubleshooting.

### IBM-Quantum-Platform/
- DJ-Algorithm/openqasm-dj.qasm: OpenQASM version of Deutsch-Jozsa.
- DJ-Algorithm/qiskit-dj.py: Qiskit implementation for IBM platform.
- Grover/qiskit-grover.py and qiskit-grover.qasm: Grover in Qiskit and QASM.

### Notebook/
- qosf-simulator-task.ipynb: Notes and experiments for the QOSF task.
- quantum_random_walk.ipynb: Random walk exploration notebook.

## Custom Simulator (simulating/)

The custom simulator supports a compact circuit string format:

```
python simulating\quantum_simulator.py -q 3 -s 1500 -c "h:0,h:1,cx:0-2,cx:1-2,x:0" --visualize
```

Gates supported: h, x, y, z, s, t, i, cx.

Outputs include an interactive Plotly dashboard saved as quantum_results.html with:
- Measurement counts
- State vector amplitudes
- Theoretical probabilities
- Measured vs theoretical comparison

## Notes on Versions

- Qiskit Aer is a separate package (qiskit-aer). The Qiskit demos use AerSimulator in newer versions.
- The Cirq Shor demo relies on ArithmeticGate support. If you see an error about arithmetic operations, upgrade Cirq.

## Contributing

- Keep explanations approachable and concrete.
- Add small comments for non-obvious quantum steps.
- Place generated images and plots next to their related scripts or in output/ folders.

## References

- References.md for curated reading.
- Qiskit documentation: https://docs.quantum.ibm.com/
- Cirq documentation: https://quantumai.google/cirq
- PennyLane documentation: https://pennylane.ai/
