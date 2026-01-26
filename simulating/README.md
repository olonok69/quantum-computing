# Quantum Circuit Simulator

A comprehensive quantum circuit simulator with command-line interface and interactive visualizations using Plotly.

## Features

- **Complete documentation**: All functions and modules are fully documented
- **Command-line interface**: Easy-to-use CLI for running quantum circuits
- **Interactive visualizations**: Beautiful Plotly charts showing:
  - Measurement frequency distributions
  - State vector amplitudes (real and imaginary parts)
  - Theoretical probability distributions
  - Comparison between measured and theoretical probabilities
- **Multiple quantum gates**: Support for H, X, Y, Z, S, T, I, and CNOT gates
- **Flexible circuit design**: String-based circuit specification

## Installation

### Setup Virtual Environment with UV

```powershell
# Create virtual environment
uv venv

# Activate virtual environment
.venv\Scripts\activate

# Install required packages
uv pip install numpy plotly
```

## Usage

### Basic Command Structure

```bash
python quantum_simulator.py --qubits <N> --shots <M> --circuit "<gates>" [--visualize] [--verbose]
```

### Command-Line Arguments

- `--qubits, -q`: Number of qubits in the quantum system (default: 2)
- `--shots, -s`: Number of measurement shots (default: 1000)
- `--circuit, -c`: Circuit description string (default: "h:0,cx:0-1")
- `--visualize, -v`: Generate and display interactive Plotly visualizations
- `--verbose`: Print detailed execution information including state vectors
- `--help, -h`: Show help message

### Circuit Specification Format

Circuits are specified as comma-separated gate instructions:
```
"gate1:target1,gate2:target2,gate3:control-target,..."
```

- **Single-qubit gates**: `gate:qubit` (e.g., `h:0` applies Hadamard to qubit 0)
- **Two-qubit gates**: `gate:control-target` (e.g., `cx:0-1` applies CNOT with control=0, target=1)

### Available Gates

| Gate | Description | Usage |
|------|-------------|-------|
| `h` | Hadamard - Creates superposition | `h:0` |
| `x` | Pauli-X - Bit flip (NOT gate) | `x:1` |
| `y` | Pauli-Y - Bit and phase flip | `y:2` |
| `z` | Pauli-Z - Phase flip | `z:0` |
| `s` | S gate - π/2 phase rotation | `s:1` |
| `t` | T gate - π/4 phase rotation | `t:0` |
| `i` | Identity - Does nothing | `i:2` |
| `cx` | CNOT - Controlled-NOT | `cx:0-1` |

## Examples

### 1. Bell State (Default)
Creates the maximally entangled Bell state: (|00⟩ + |11⟩)/√2

```bash
python quantum_simulator.py
```

Or explicitly:
```bash
python quantum_simulator.py --qubits 2 --shots 1000 --circuit "h:0,cx:0-1"
```

Expected results: ~50% |00⟩ and ~50% |11⟩

### 2. Bell State with Visualization
```bash
python quantum_simulator.py --visualize --verbose
```

This will:
- Print detailed circuit information
- Show the final state vector
- Generate an HTML file with interactive plots
- Open the visualization in your browser

### 3. Three-Qubit GHZ State
Creates the Greenberger-Horne-Zeilinger state: (|000⟩ + |111⟩)/√2

```bash
python quantum_simulator.py -q 3 -s 2000 -c "h:0,cx:0-1,cx:0-2" --visualize
```

Expected results: ~50% |000⟩ and ~50% |111⟩

### 4. Single Qubit Superposition
```bash
python quantum_simulator.py -q 1 -s 500 -c "h:0"
```

Expected results: ~50% |0⟩ and ~50% |1⟩

### 5. Multiple Gates on Different Qubits
```bash
python quantum_simulator.py -q 3 -s 1000 -c "h:0,x:1,h:2" --verbose
```

This applies:
- Hadamard to qubit 0 (superposition)
- Pauli-X to qubit 1 (flip to |1⟩)
- Hadamard to qubit 2 (superposition)

### 6. Complex Circuit
```bash
python quantum_simulator.py -q 3 -s 1500 -c "h:0,h:1,cx:0-2,cx:1-2,x:0" --visualize
```

## Output

### Console Output

**Standard Mode:**
```
======================================================================
                    🔬 QUANTUM CIRCUIT SIMULATOR 🔬
======================================================================

🚀 Initializing 2-qubit quantum system in state |00>...
⚡ Executing quantum circuit...

🎲 Performing 1000 measurements...

📈 Measurement Results:
{
    "00": 507,
    "11": 493
}

======================================================================
                 ✅ Simulation completed successfully!
======================================================================
```

**Verbose Mode:**
Shows additional information including:
- Circuit configuration details
- Gate-by-gate execution
- Final state vector with amplitudes
- Probability calculations

### Visualization Output

When using `--visualize`, the simulator generates `quantum_results.html` containing four interactive plots:

1. **Measurement Counts**: Bar chart showing observed frequencies of each quantum state
2. **State Vector Amplitudes**: Real and imaginary parts of the state vector
3. **Theoretical Probabilities**: Expected probability distribution from |ψ|²
4. **Measured vs Theoretical**: Line plot comparing experimental results with theory

The plots are interactive - hover, zoom, and pan to explore the data!

## Understanding the Results

### Bit String Format
Results use **little-endian** format where the rightmost bit is qubit 0:
- `"00"` means qubit 0 = 0, qubit 1 = 0
- `"10"` means qubit 0 = 0, qubit 1 = 1
- `"01"` means qubit 0 = 1, qubit 1 = 0
- `"11"` means qubit 0 = 1, qubit 1 = 1

### Probability Distributions
The number of shots determines how accurately the measured distribution approximates the theoretical one. More shots → better approximation (but slower execution).

## Code Structure

The simulator consists of several key functions:

- `get_ground_state(num_qubits)`: Initialize quantum system in |0...0⟩
- `get_single_qubit_operator()`: Build operators for single-qubit gates
- `get_cx_operator()`: Build CNOT gate operator
- `get_operator()`: Wrapper to dispatch to appropriate operator constructor
- `run_program()`: Main simulation engine - applies gates sequentially
- `measure_all()`: Perform quantum measurement (Born rule)
- `get_counts()`: Run multiple measurements for statistical analysis
- `visualize_results()`: Generate interactive Plotly visualizations
- `parse_circuit_string()`: Parse circuit specification string
- `main()`: CLI entry point

## Theory

### State Vector Representation
An n-qubit system is represented as a complex vector of length 2ⁿ. Each element represents the probability amplitude of a computational basis state.

### Gate Application
Gates are applied as unitary matrix operators using tensor products (Kronecker products) to construct full-system operators from single-qubit gates.

### Measurement
Quantum measurement follows the Born rule: the probability of measuring state |i⟩ is P(i) = |αᵢ|², where αᵢ is the amplitude of that state.

## Troubleshooting

**Issue**: Module not found errors
**Solution**: Make sure you're in the activated virtual environment and have installed all dependencies:
```bash
.venv\Scripts\activate
uv pip install numpy plotly
```

**Issue**: Visualization doesn't open automatically
**Solution**: Manually open the `quantum_results.html` file in your browser

**Issue**: "Invalid instruction format" error
**Solution**: Check your circuit string format. Use colons and dashes correctly:
- Correct: `"h:0,cx:0-1"`
- Wrong: `"h-0,cx:0:1"`

## Advanced Usage

### Python API

You can also use the simulator programmatically:

```python
from quantum_simulator import *

# Define circuit
circuit = [
    {"gate": "h", "target": [0]},
    {"gate": "cx", "target": [0, 1]}
]

# Initialize and run
qpu = get_ground_state(2)
final_state = run_program(qpu, circuit)

# Measure
counts = get_counts(final_state, 1000)
print(counts)

# Visualize
visualize_results(counts, final_state, 2)
```

## License

Open source - feel free to use and modify!

## Contributing

Contributions welcome! Possible enhancements:
- Additional quantum gates (Toffoli, Fredkin, rotation gates)
- Noise models
- Quantum state tomography
- Circuit optimization
- Export to QASM format
- Integration with real quantum hardware APIs

## References

- Nielsen & Chuang, "Quantum Computation and Quantum Information"
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Quantum Computing Playground](https://quantumplayground.net/)
