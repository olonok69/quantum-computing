# Quantum Computing Playground

A hands-on collection of notes, scripts, and notebooks for demystifying quantum computing concepts with approachable analogies and practical code examples.

## Repository Map

```
.
├── docs/                     # Narrative guides for non-technical audiences
├── fundamentals/             # Qiskit circuits and Grover-style search demos
├── optimize_quantum_circuit/ # PennyLane utilities for variational circuits
├── simulating/               # NumPy-based gate simulations and linear algebra
└── Notebook/                 # Exploratory Jupyter notebooks (qOSF tasks)
```

## Key Concepts at a Glance

For an analogy-first introduction, read [docs/quantum_computing_explained.md](docs/quantum_computing_explained.md). It covers:

- **Bits vs qubits:** spinning-coin analogy for superposition and measurement collapse.
- **Quantum gates:** how rotations, superposition, and entanglement extend classical logic.
- **Specialized advantage:** why quantum excels at maze-like problems (cryptography, chemistry, optimization) but not everyday browsing or media playback.
- **Current limitations:** fragility, error rates, and cost that make todays devices niche but promising.

## Getting Started

1. **Create an environment** (Python 3.10+ recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```
2. **Install core dependencies** (tailor as needed for your experiments):
   ```bash
   pip install qiskit qiskit-aer matplotlib numpy pennylane
   ```
3. **Run an example circuit**:
   ```bash
   python fundamentals/main.py
   ```
4. **Explore notebooks** by launching VS Code or Jupyter Lab and opening files in `Notebook/` or `optimize_quantum_circuit/`.

## Project Highlights

### docs/
- [quantum_computing_explained.md](docs/quantum_computing_explained.md) — Plain-language guide comparing classical vs quantum computing, with tables, analogies (spinning coin, maze, kitchen tools), and real-world impact areas.
- computacion_cuantica_explicada.md — Spanish translation/work-in-progress to broaden accessibility.

### fundamentals/
- [main.py](fundamentals/main.py) builds a Grover-style satisfiability oracle around the helper `XOR` function, applies a custom diffuser, and simulates the circuit via Qiskit Aer. Results are saved to `fundamentals/output/my_circuit.png` for quick inspection.

### simulating/
- [operations.py](simulating/operations.py) demonstrates how to express qubit states, Hadamard gates, CNOT variations, and custom multi-qubit operators using raw NumPy. Its a lightweight sandbox for understanding tensors without a full framework.
- Additional scripts (`apply_gates.py`, `code_gates.py`, `code_numpy.py`) extend these experiments into reusable helpers.

### optimize_quantum_circuit/
- [surface_plot.py](optimize_quantum_circuit/surface_plot.py) visualizes PennyLane cost landscapes by rendering 3D wireframes plus optimization trajectories (e.g., Adam optimizer paths) for two-parameter variational circuits.
- `hello_pennylane.ipynb` offers an interactive notebook to tweak templates and optimizers.

### Notebook/
- `qosf-simulator-task.ipynb` documents work toward the Quantum Open Source Foundation mentorship challenge, showcasing simulator use and custom tasks.

## Suggested Workflow

1. **Absorb the intuition** in `docs/` to align on mental models.
2. **Simulate with NumPy** in `simulating/` to cement linear algebra fundamentals.
3. **Scale up with Qiskit** via `fundamentals/` to build oracles and visualize measurement outcomes.
4. **Experiment with variational circuits** using PennyLane utilities inside `optimize_quantum_circuit/`.
5. **Document learnings** or new demos back into `docs/` or `Notebook/` for future collaborators.

## Contributing

- Keep prose approachable; favor analogies and visuals for new learners.
- When adding code, include brief comments describing the quantum workflow or mathematical intent.
- Share simulator outputs (plots, histograms) in `fundamentals/output/` or dedicated `output/` folders to keep results reproducible without rerunning heavy jobs.

## Roadmap Ideas

- Expand the Spanish documentation to parity with the English guide.
- Add tests or utility scripts for benchmarking gate implementations in `simulating/`.
- Include PennyLane/Qiskit hybrid examples that showcase variational algorithms on simulators.
- Document setup steps for running notebooks on real quantum hardware backends when available.

# links
- https://jonathan-hui.medium.com/qc-programming-with-quantum-gates-8996b667d256
