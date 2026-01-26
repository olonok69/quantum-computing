# Quantum Simulator - Quick Start Guide

## ✅ What Has Been Completed

Your quantum simulator now includes:

1. **Complete documentation** - Every function has detailed docstrings explaining:
   - What it does
   - Parameters and return values
   - Examples of usage
   - Mathematical theory behind it

2. **Command-line interface** - Run circuits from the terminal:
   ```bash
   python quantum_simulator.py --qubits 2 --shots 1000 --circuit "h:0,cx:0-1"
   ```

3. **Interactive visualizations** using Plotly:
   - Measurement frequency bar charts
   - State vector amplitudes (real & imaginary)
   - Probability distributions
   - Measured vs theoretical comparisons

4. **Example scripts** - `examples.py` with 7 different quantum circuit demonstrations

## 🚀 Quick Start

### Activate the Virtual Environment

```powershell
cd d:\quantum
.venv\Scripts\activate
```

### Run Basic Examples

**1. Default Bell State:**
```bash
python simulating\quantum_simulator.py
```

**2. With Visualization:**
```bash
python simulating\quantum_simulator.py --visualize
```

**3. Verbose Mode (shows state vectors):**
```bash
python simulating\quantum_simulator.py --verbose
```

**4. Custom Circuit (3-qubit GHZ state):**
```bash
python simulating\quantum_simulator.py -q 3 -s 2000 -c "h:0,cx:0-1,cx:0-2" --visualize
```

**5. Run All Examples:**
```bash
cd simulating
python examples.py
```

### View Help

```bash
python simulating\quantum_simulator.py --help
```

## 📊 Visualizations

When you use `--visualize`, the simulator creates `quantum_results.html` with four interactive plots:

1. **Measurement Counts** - How many times each quantum state was measured
2. **State Amplitudes** - Real and imaginary parts of the quantum state
3. **Theoretical Probabilities** - What the theory predicts
4. **Measured vs Theory** - Comparison showing how well experiments match theory

Open `quantum_results.html` in any web browser to explore the interactive plots!

## 🎯 Common Use Cases

### Create a Bell State
```bash
python simulating\quantum_simulator.py -c "h:0,cx:0-1"
```
Result: ~50% |00⟩ and ~50% |11⟩

### Create Superposition
```bash
python simulating\quantum_simulator.py -q 1 -c "h:0"
```
Result: ~50% |0⟩ and ~50% |1⟩

### Apply Multiple Gates
```bash
python simulating\quantum_simulator.py -q 3 -c "h:0,x:1,h:2"
```
Result: Qubit 0 and 2 in superposition, qubit 1 flipped to |1⟩

### Large-Scale Simulation
```bash
python simulating\quantum_simulator.py -q 4 -s 5000 -c "h:0,cx:0-1,cx:1-2,cx:2-3" --visualize
```
Result: 4-qubit entangled state

## 📂 File Structure

```
simulating/
├── quantum_simulator.py   # Main simulator with CLI
├── examples.py            # 7 example demonstrations
└── README.md             # Comprehensive documentation
```

## 🔧 Available Gates

| Gate | Symbol | Description | Example |
|------|--------|-------------|---------|
| Hadamard | H | Creates superposition | `h:0` |
| Pauli-X | X | Bit flip (NOT gate) | `x:1` |
| Pauli-Y | Y | Bit + phase flip | `y:0` |
| Pauli-Z | Z | Phase flip | `z:2` |
| S gate | S | π/2 phase rotation | `s:1` |
| T gate | T | π/4 phase rotation | `t:0` |
| Identity | I | Does nothing | `i:2` |
| CNOT | CX | Controlled-NOT | `cx:0-1` |

## 💡 Tips

1. **More shots = More accuracy**: Use `-s 5000` for better statistical results
2. **Verbose mode is educational**: Add `--verbose` to see state vectors and probabilities
3. **Start simple**: Begin with 1-2 qubits, then scale up
4. **Visualizations help understanding**: Always use `--visualize` when learning
5. **Check the examples**: `examples.py` has 7 pre-built circuits to learn from

## 📖 Learn More

- See `README.md` for complete documentation
- See `examples.py` for programmatic usage
- Run `python quantum_simulator.py --help` for all options

## 🎓 Understanding Results

### Bit String Format (Little-Endian)
- `"00"` = qubit 0 is |0⟩, qubit 1 is |0⟩
- `"10"` = qubit 0 is |0⟩, qubit 1 is |1⟩
- `"01"` = qubit 0 is |1⟩, qubit 1 is |0⟩
- `"11"` = qubit 0 is |1⟩, qubit 1 is |1⟩

(Rightmost bit = qubit 0)

### Why Aren't Results Exactly 50/50?
Quantum measurement is probabilistic! With 1000 shots, you might get 487/513 instead of 500/500. This is normal. More shots = closer to theoretical probabilities.

## 🐛 Troubleshooting

**Q: Can't find module numpy/plotly**  
A: Make sure virtual environment is activated:
```bash
.venv\Scripts\activate
uv pip install numpy plotly
```

**Q: Visualization doesn't open**  
A: Manually open `quantum_results.html` in your browser

**Q: "Invalid instruction format" error**  
A: Check circuit syntax. Use `:` for targets and `-` for control-target pairs:
- ✅ Correct: `"h:0,cx:0-1"`
- ❌ Wrong: `"h-0,cx:0:1"`

## 🎉 Success!

You now have a fully documented, feature-rich quantum circuit simulator with:
- ✅ Complete documentation
- ✅ Command-line interface
- ✅ Interactive Plotly visualizations
- ✅ Multiple example scripts
- ✅ Professional code structure

Enjoy simulating quantum circuits! 🔬⚛️
