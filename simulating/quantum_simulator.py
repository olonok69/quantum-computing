"""
Quantum Circuit Simulator

This module provides a quantum circuit simulator that can simulate quantum gates,
create quantum states, and measure quantum systems. It supports standard single-qubit
gates (I, H, X, Y, Z, S, T) and the two-qubit CNOT (CX) gate.

Features:
    - Ground state initialization
    - Single and multi-qubit gate operations
    - CNOT gate implementation
    - Quantum measurement simulation
    - Statistical analysis of measurement outcomes
    - Visualization of results using Plotly

Usage:
    python quantum_simulator.py --qubits 2 --shots 1000 --circuit "h:0,cx:0-1"
    python quantum_simulator.py --qubits 3 --shots 500 --circuit "h:0,h:1,cx:0-2" --visualize

Author: Quantum Computing Research
Date: January 2026
"""

import numpy as np
import json
import argparse
from collections import Counter
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# A dictionary containing the standard quantum gates as 2x2 unitary matrices
# Gates supported:
#   - I (Identity): Does nothing to the qubit
#   - H (Hadamard): Creates superposition, maps |0> to (|0>+|1>)/sqrt(2)
#   - X (Pauli-X): Bit flip, maps |0> to |1> and vice versa (quantum NOT)
#   - Y (Pauli-Y): Bit and phase flip
#   - Z (Pauli-Z): Phase flip, maps |1> to -|1>
#   - S (Phase gate): Applies pi/2 phase rotation
#   - T (pi/8 gate): Applies pi/4 phase rotation
gates = {
    "i": np.identity(2),  # Identity gate
    "h": np.array([[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]]),  # Hadamard
    "x": np.array([[0, 1], [1, 0]]),  # Pauli-X (NOT gate)
    "y": np.array([[0, +1j], [-1j, 0]]),  # Pauli-Y
    "z": np.array([[1, 0], [0, -1]]),  # Pauli-Z
    "s": np.array([[1, 0], [0, np.exp(np.pi * +1j / 2)]]),  # Phase gate (sqrt(Z))
    "t": np.array([[1, 0], [0, np.exp(np.pi * +1j / 4)]]),  # T gate (sqrt(S))
}

def get_ground_state(num_qubits):
    """
    Initialize a quantum system in the ground state |00...0>.
    
    The ground state is the computational basis state where all qubits are in |0>.
    For n qubits, this creates a vector of length 2^n with all zeros except the first element.
    
    Args:
        num_qubits (int): Number of qubits in the quantum system
        
    Returns:
        numpy.ndarray: State vector of length 2^n representing |00...0>
        
    Example:
        >>> get_ground_state(2)
        array([1, 0, 0, 0])  # Represents |00>
    """
    vector = [0 for i in range(2**num_qubits)]
    vector[0] = 1  # Set the first amplitude to 1
    return np.array(vector)

def get_single_qubit_operator(total_qubits, gate, target):
    """
    Construct a full-system unitary operator for a single-qubit gate.
    
    This function creates a (2^n x 2^n) matrix that applies a single-qubit gate
    to a specific target qubit while leaving other qubits unchanged (applying identity).
    The operator is built using tensor products (Kronecker products) of the gate
    and identity matrices.
    
    Args:
        total_qubits (int): Total number of qubits in the quantum system
        gate (numpy.ndarray): The 2x2 unitary matrix of the gate to apply
        target (int): Index of the target qubit (0-indexed, where 0 is the first qubit)
        
    Returns:
        numpy.ndarray: Full system operator matrix of size 2^n x 2^n
        
    Example:
        For a 2-qubit system applying H to qubit 0:
        Result is H tensor I (Hadamard tensor Identity)
    """
    # Start tensor product with identity or the gate itself depending on target
    operator = gate if target == 0 else gates['i']

    for qubit in range(1, total_qubits):
        if qubit == target:
            # Tensor product with the gate
            operator = np.kron(operator, gate)
        else:
            # Tensor product with identity
            operator = np.kron(operator, gates['i'])
    
    return operator

def get_cx_operator(total_qubits, control, target):
    """
    Construct a full-system CNOT (Controlled-NOT) gate operator.
    
    The CNOT gate flips the target qubit if and only if the control qubit is |1>.
    It's implemented as: CNOT = |0><0| tensor I + |1><1| tensor X
    
    The construction uses projection operators:
    - P0x0 = |0><0|: Projects onto |0> state
    - P1x1 = |1><1|: Projects onto |1> state
    
    When control is |0>: target remains unchanged (identity applied)
    When control is |1>: target is flipped (X gate applied)
    
    Args:
        total_qubits (int): Total number of qubits in the system
        control (int): Index of the control qubit (0-indexed)
        target (int): Index of the target qubit (0-indexed)
        
    Returns:
        numpy.ndarray: Full system CNOT operator matrix of size 2^n x 2^n
        
    Example:
        For 2 qubits with control=0, target=1:
        |00> -> |00>, |01> -> |01>, |10> -> |11>, |11> -> |10>
    """
    # Projection operators for |0> and |1> states
    P0x0 = np.array([[1, 0], [0, 0]])  # |0><0|
    P1x1 = np.array([[0, 0], [0, 1]])  # |1><1|
    X = gates['x']  # Pauli-X gate

    # Case 1: Control qubit is |0> -> apply identity to all qubits
    operator1 = P0x0 if control == 0 else gates['i']

    for qubit in range(1, total_qubits):
        if qubit == control:
            operator1 = np.kron(operator1, P0x0)
        else:
            operator1 = np.kron(operator1, gates['i'])

    # Case 2: Control qubit is |1> -> apply X to target, identity to others
    operator2 = P1x1 if control == 0 else gates['i']

    for qubit in range(1, total_qubits):
        if qubit == control:
            operator2 = np.kron(operator2, P1x1)
        elif qubit == target:
            operator2 = np.kron(operator2, X)  # Apply X to target
        else:
            operator2 = np.kron(operator2, gates['i'])
    
    # Combine both cases: CNOT = (control is 0 -> I) + (control is 1 -> X on target)
    return operator1 + operator2

def get_operator(total_qubits, gate_unitary, target_qubits):
    """
    General wrapper function to generate the appropriate quantum gate operator.
    
    This function dispatches to the appropriate operator construction function
    based on the gate type. It handles both single-qubit gates and the CNOT gate.
    
    Args:
        total_qubits (int): Total number of qubits in the quantum system
        gate_unitary (str): Name of the gate ('h', 'x', 'y', 'z', 's', 't', 'i', or 'cx')
        target_qubits (list): List of target qubit indices
            - For single-qubit gates: [target]
            - For CNOT: [control, target]
            
    Returns:
        numpy.ndarray: Full system unitary operator matrix of size 2^n x 2^n
        
    Raises:
        KeyError: If gate_unitary is not a recognized gate name
    """
    # Dispatch to appropriate operator construction function
    if gate_unitary == 'cx':
        # Two-qubit CNOT gate requires control and target qubits
        return get_cx_operator(total_qubits, target_qubits[0], target_qubits[1])
    else:
        # Single-qubit gates require only one target qubit
        return get_single_qubit_operator(total_qubits, gates[gate_unitary], target_qubits[0])


def run_program(initial_state, program):
    """
    Execute a quantum circuit by sequentially applying gates to the quantum state.
    
    This is the main simulation engine. It takes an initial quantum state and
    a list of gate instructions, then applies each gate sequentially to evolve
    the quantum state according to the circuit design.
    
    The state evolution follows: |psi_final> = U_n ... U_2 U_1 |psi_initial>
    where U_i are the gate operators applied in sequence.
    
    Args:
        initial_state (numpy.ndarray): Initial state vector of length 2^n
        program (list): List of gate instructions, each a dict with:
            - 'gate' (str): Gate name ('h', 'x', 'cx', etc.)
            - 'target' (list): Target qubit indices
            
    Returns:
        numpy.ndarray: Final quantum state vector after all gates are applied
        
    Example:
        >>> program = [
        ...     {"gate": "h", "target": [0]},
        ...     {"gate": "cx", "target": [0, 1]}
        ... ]
        >>> initial = get_ground_state(2)
        >>> final = run_program(initial, program)
    """
    total_qubits = int(np.log2(len(initial_state)))

    state = initial_state
    
    # Apply each gate instruction sequentially
    # For each instruction:
    #   1. Get the full-system matrix operator for the gate
    #   2. Apply it to the current state vector (matrix-vector multiplication)
    #   3. Continue to next instruction
    for instruction in program: 
        gate = instruction['gate']
        targets = instruction['target']
        operator = get_operator(total_qubits, gate, targets)
        state = np.dot(operator, state)  # |psi_new> = U|psi_old>

    return state

def measure_all(state_vector):
    """
    Perform a measurement of all qubits in the computational basis.
    
    Quantum measurement collapses the state vector to one of the computational
    basis states (e.g., |00>, |01>, |10>, |11> for 2 qubits). The probability
    of measuring each state is given by the squared magnitude of its amplitude:
    P(state_i) = |alpha_i|^2
    
    This implements the Born rule from quantum mechanics.
    
    Args:
        state_vector (numpy.ndarray): Quantum state vector of length 2^n
        
    Returns:
        int: Index of the measured state in the computational basis
            (e.g., 0->|00>, 1->|01>, 2->|10>, 3->|11> for 2 qubits)
            
    Example:
        For state (|00> + |11>)/sqrt(2), measurement returns either 0 or 3
        with equal probability (50% each)
    """
    # Calculate measurement probabilities using Born rule: P = |psi|^2
    probabilities = np.abs(state_vector)**2
    
    # Randomly select a state according to probability distribution
    index = np.random.choice(a=len(state_vector), p=probabilities)

    return index

def get_counts(state_vector, num_shots):
    """
    Simulate multiple measurements to estimate the probability distribution.
    
    Since quantum measurement is probabilistic, we need multiple "shots" (measurements)
    to estimate the probability distribution of outcomes. This function performs
    num_shots measurements and counts the frequency of each result.
    
    The results are formatted as bit strings in little-endian order (rightmost bit
    is qubit 0), matching common quantum computing conventions.
    
    Args:
        state_vector (numpy.ndarray): Quantum state vector of length 2^n
        num_shots (int): Number of measurements to perform
        
    Returns:
        str: JSON string containing measurement statistics in format:
            {
                "00": count1,
                "01": count2,
                "10": count3,
                "11": count4,
                ...
            }
            where keys are bit strings (little-endian) and values are frequencies
            
    Example:
        For Bell state (|00> + |11>)/sqrt(2) with 1000 shots:
        {"00": 503, "11": 497}  (approximately 50/50 distribution)
    """
    results = []
    
    num_bits = int(np.log2(len(state_vector)))
    
    # Perform num_shots measurements
    for _ in range(num_shots):
        result = measure_all(state_vector)
        # Convert index to binary string and reverse for little-endian format
        # e.g., index 3 with 2 qubits -> "11" -> "11" (qubit 0 on right)
        results.append("{0:b}".format(result).zfill(num_bits)[::-1]) 

    # Count occurrences of each outcome
    stats = Counter(results)   

    return json.dumps(stats, sort_keys=True, indent=4)

def visualize_results(counts_dict, state_vector, num_qubits):
    """
    Create interactive visualizations of quantum circuit results using Plotly.
    
    This function generates three types of visualizations:
    1. Measurement counts bar chart: Shows frequency of each measurement outcome
    2. State vector amplitudes: Displays real and imaginary parts of amplitudes
    3. Probability distribution: Shows theoretical probabilities vs. measured frequencies
    
    Args:
        counts_dict (dict): Dictionary of measurement outcomes and their frequencies
        state_vector (numpy.ndarray): Final quantum state vector
        num_qubits (int): Number of qubits in the system
        
    Returns:
        None (displays plots and saves to HTML file)
    """
    # Parse counts from JSON if necessary
    if isinstance(counts_dict, str):
        counts_dict = json.loads(counts_dict)
    
    # Create subplots with 2 rows and 2 columns
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Measurement Counts (Observed Frequencies)',
            'State Vector Amplitudes (Real & Imaginary)',
            'Probability Distribution (Theoretical)',
            'Measurement vs Theoretical Probabilities'
        ),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # Plot 1: Measurement counts bar chart
    states = list(counts_dict.keys())
    counts = list(counts_dict.values())
    total_shots = sum(counts)
    
    fig.add_trace(
        go.Bar(
            x=states,
            y=counts,
            name='Measured Counts',
            marker_color='rgb(55, 126, 184)',
            text=counts,
            textposition='auto',
        ),
        row=1, col=1
    )
    
    # Plot 2: State vector amplitudes (real and imaginary parts)
    basis_states = [format(i, f'0{num_qubits}b')[::-1] for i in range(2**num_qubits)]
    real_parts = np.real(state_vector)
    imag_parts = np.imag(state_vector)
    
    fig.add_trace(
        go.Bar(
            x=basis_states,
            y=real_parts,
            name='Real Part',
            marker_color='rgb(77, 175, 74)',
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(
            x=basis_states,
            y=imag_parts,
            name='Imaginary Part',
            marker_color='rgb(228, 26, 28)',
        ),
        row=1, col=2
    )
    
    # Plot 3: Theoretical probabilities
    probabilities = np.abs(state_vector)**2
    
    fig.add_trace(
        go.Bar(
            x=basis_states,
            y=probabilities,
            name='Theoretical Probability',
            marker_color='rgb(152, 78, 163)',
            text=[f'{p:.4f}' for p in probabilities],
            textposition='auto',
        ),
        row=2, col=1
    )
    
    # Plot 4: Comparison between theoretical and measured
    measured_probs = {state: 0 for state in basis_states}
    for state, count in counts_dict.items():
        measured_probs[state] = count / total_shots
    
    measured_prob_values = [measured_probs[state] for state in basis_states]
    
    fig.add_trace(
        go.Scatter(
            x=basis_states,
            y=probabilities,
            mode='lines+markers',
            name='Theoretical',
            line=dict(color='rgb(152, 78, 163)', width=3),
            marker=dict(size=10)
        ),
        row=2, col=2
    )
    
    fig.add_trace(
        go.Scatter(
            x=basis_states,
            y=measured_prob_values,
            mode='lines+markers',
            name='Measured',
            line=dict(color='rgb(55, 126, 184)', width=3, dash='dash'),
            marker=dict(size=10)
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        title_text=f"Quantum Circuit Results Analysis ({num_qubits} Qubits, {total_shots} Shots)",
        showlegend=True,
        height=900,
        width=1400,
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Quantum State", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    
    fig.update_xaxes(title_text="Basis State", row=1, col=2)
    fig.update_yaxes(title_text="Amplitude", row=1, col=2)
    
    fig.update_xaxes(title_text="Basis State", row=2, col=1)
    fig.update_yaxes(title_text="Probability", row=2, col=1)
    
    fig.update_xaxes(title_text="Basis State", row=2, col=2)
    fig.update_yaxes(title_text="Probability", row=2, col=2)
    
    # Save to HTML file
    output_file = "quantum_results.html"
    fig.write_html(output_file)
    print(f"\n📊 Visualization saved to: {output_file}")
    
    # Show the plot
    fig.show()


def parse_circuit_string(circuit_str):
    """
    Parse a circuit string into a program list.
    
    Format: "gate1:target1,gate2:target2-target3,..."
    Examples:
        "h:0,cx:0-1" -> H gate on qubit 0, then CNOT with control=0, target=1
        "h:0,h:1,x:2" -> H on qubit 0, H on qubit 1, X on qubit 2
        
    Args:
        circuit_str (str): Circuit description string
        
    Returns:
        list: Program list with gate instructions
        
    Raises:
        ValueError: If circuit string format is invalid
    """
    if not circuit_str:
        return []
    
    program = []
    instructions = circuit_str.split(',')
    
    for instruction in instructions:
        instruction = instruction.strip()
        if ':' not in instruction:
            raise ValueError(f"Invalid instruction format: {instruction}. Expected 'gate:target(s)'")
        
        gate, targets_str = instruction.split(':', 1)
        gate = gate.lower().strip()
        
        # Parse target qubits (can be single "0" or multiple "0-1")
        if '-' in targets_str:
            targets = [int(t.strip()) for t in targets_str.split('-')]
        else:
            targets = [int(targets_str.strip())]
        
        program.append({"gate": gate, "target": targets})
    
    return program


def main():
    """
    Main function to run the quantum circuit simulator with command-line arguments.
    
    This function handles:
    - Command-line argument parsing
    - Circuit initialization and execution
    - Measurement and statistical analysis
    - Optional visualization of results
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Quantum Circuit Simulator - Simulate quantum gates and visualize results',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create Bell state with 2 qubits
  python quantum_simulator.py --qubits 2 --shots 1000 --circuit "h:0,cx:0-1"
  
  # Three-qubit GHZ state
  python quantum_simulator.py --qubits 3 --shots 500 --circuit "h:0,cx:0-1,cx:0-2" --visualize
  
  # Single qubit superposition
  python quantum_simulator.py --qubits 1 --shots 100 --circuit "h:0"
  
  # Multiple gates on different qubits
  python quantum_simulator.py --qubits 3 --shots 200 --circuit "h:0,x:1,h:2"

Available Gates:
  h  : Hadamard gate (creates superposition)
  x  : Pauli-X gate (NOT gate, bit flip)
  y  : Pauli-Y gate (bit and phase flip)
  z  : Pauli-Z gate (phase flip)
  s  : S gate (phase gate, sqrt(Z))
  t  : T gate (pi/8 gate, sqrt(S))
  i  : Identity gate (does nothing)
  cx : CNOT gate (controlled-NOT, requires two qubits)
        """
    )
    
    parser.add_argument(
        '--qubits', '-q',
        type=int,
        default=2,
        help='Number of qubits in the quantum system (default: 2)'
    )
    
    parser.add_argument(
        '--shots', '-s',
        type=int,
        default=1000,
        help='Number of measurement shots to perform (default: 1000)'
    )
    
    parser.add_argument(
        '--circuit', '-c',
        type=str,
        default='h:0,cx:0-1',
        help='Circuit description string. Format: "gate:target,gate:control-target,..."\n'
             'Example: "h:0,cx:0-1" creates a Bell state (default: "h:0,cx:0-1")'
    )
    
    parser.add_argument(
        '--visualize', '-v',
        action='store_true',
        help='Generate and display Plotly visualizations of results'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print detailed information about circuit execution'
    )
    
    args = parser.parse_args()
    
    # Print header
    print("=" * 70)
    print("🔬 QUANTUM CIRCUIT SIMULATOR 🔬".center(70))
    print("=" * 70)
    
    # Parse circuit
    try:
        my_circuit = parse_circuit_string(args.circuit)
    except ValueError as e:
        print(f"\n❌ Error parsing circuit: {e}")
        return
    
    if args.verbose:
        print(f"\n📋 Configuration:")
        print(f"   Number of qubits: {args.qubits}")
        print(f"   Number of shots: {args.shots}")
        print(f"   Circuit gates: {len(my_circuit)}")
        print(f"\n🔧 Circuit Instructions:")
        for i, instruction in enumerate(my_circuit, 1):
            gate = instruction['gate'].upper()
            targets = instruction['target']
            if len(targets) == 1:
                print(f"   {i}. {gate} gate on qubit {targets[0]}")
            else:
                print(f"   {i}. {gate} gate: control={targets[0]}, target={targets[1]}")
    
    # Create quantum computer (initialize qubits in ground state)
    print(f"\n🚀 Initializing {args.qubits}-qubit quantum system in state |{'0'*args.qubits}>...")
    my_qpu = get_ground_state(args.qubits)
    
    # Run circuit
    print(f"⚡ Executing quantum circuit...")
    final_state = run_program(my_qpu, my_circuit)
    
    if args.verbose:
        print(f"\n📊 Final State Vector:")
        basis_states = [format(i, f'0{args.qubits}b')[::-1] for i in range(2**args.qubits)]
        for i, (basis, amplitude) in enumerate(zip(basis_states, final_state)):
            if abs(amplitude) > 1e-10:  # Only show non-zero amplitudes
                real = np.real(amplitude)
                imag = np.imag(amplitude)
                prob = abs(amplitude)**2
                print(f"   |{basis}>: ({real:+.4f} {imag:+.4f}j) -> P = {prob:.4f}")
    
    # Perform measurements
    print(f"\n🎲 Performing {args.shots} measurements...")
    counts = get_counts(final_state, args.shots)
    
    # Display results
    print(f"\n📈 Measurement Results:")
    print(counts)
    
    # Generate visualization if requested
    if args.visualize:
        print(f"\n🎨 Generating visualizations...")
        visualize_results(counts, final_state, args.qubits)
    
    print("\n" + "=" * 70)
    print("✅ Simulation completed successfully!".center(70))
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
