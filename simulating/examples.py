"""
Example Usage Scripts for Quantum Circuit Simulator

This file demonstrates various ways to use the quantum simulator both
through the command-line interface and programmatically.
"""

# Import the simulator functions
import sys
sys.path.append('.')
from quantum_simulator import (
    get_ground_state,
    run_program,
    get_counts,
    visualize_results,
    parse_circuit_string
)
import json

def example_1_bell_state():
    """
    Example 1: Create and measure a Bell state
    
    The Bell state is a maximally entangled 2-qubit state:
    |Bell> = (|00> + |11>) / sqrt(2)
    """
    print("="*70)
    print("Example 1: Bell State")
    print("="*70)
    
    # Define circuit programmatically
    circuit = [
        {"gate": "h", "target": [0]},      # Hadamard on qubit 0
        {"gate": "cx", "target": [0, 1]}   # CNOT with control=0, target=1
    ]
    
    # Initialize quantum system
    qpu = get_ground_state(2)
    
    # Run circuit
    final_state = run_program(qpu, circuit)
    
    # Measure multiple times
    counts = get_counts(final_state, 1000)
    
    print(f"Results:\n{counts}\n")
    print("Expected: ~50% |00> and ~50% |11>\n")


def example_2_superposition():
    """
    Example 2: Single qubit in superposition
    
    Applying Hadamard creates equal superposition:
    |+> = (|0> + |1>) / sqrt(2)
    """
    print("="*70)
    print("Example 2: Single Qubit Superposition")
    print("="*70)
    
    circuit = [
        {"gate": "h", "target": [0]}
    ]
    
    qpu = get_ground_state(1)
    final_state = run_program(qpu, circuit)
    counts = get_counts(final_state, 1000)
    
    print(f"Results:\n{counts}\n")
    print("Expected: ~50% |0> and ~50% |1>\n")


def example_3_ghz_state():
    """
    Example 3: Three-qubit GHZ state
    
    GHZ state is a 3-qubit entangled state:
    |GHZ> = (|000> + |111>) / sqrt(2)
    """
    print("="*70)
    print("Example 3: GHZ State (3 qubits)")
    print("="*70)
    
    circuit = [
        {"gate": "h", "target": [0]},
        {"gate": "cx", "target": [0, 1]},
        {"gate": "cx", "target": [0, 2]}
    ]
    
    qpu = get_ground_state(3)
    final_state = run_program(qpu, circuit)
    counts = get_counts(final_state, 2000)
    
    print(f"Results:\n{counts}\n")
    print("Expected: ~50% |000> and ~50% |111>\n")


def example_4_custom_gates():
    """
    Example 4: Multiple different gates on different qubits
    
    Shows how different gates affect different qubits independently
    """
    print("="*70)
    print("Example 4: Multiple Gates")
    print("="*70)
    
    circuit = [
        {"gate": "h", "target": [0]},   # Hadamard on qubit 0 (superposition)
        {"gate": "x", "target": [1]},   # X gate on qubit 1 (flip to |1>)
        {"gate": "h", "target": [2]}    # Hadamard on qubit 2 (superposition)
    ]
    
    qpu = get_ground_state(3)
    final_state = run_program(qpu, circuit)
    counts = get_counts(final_state, 1000)
    
    print(f"Results:\n{counts}\n")
    print("Expected: qubit 1 is always |1>, qubits 0 and 2 are in superposition")
    print("Should see: ~25% each of |010>, |110>, |011>, |111>\n")


def example_5_using_string_parser():
    """
    Example 5: Using the string parser for circuit definition
    
    This is how the CLI internally processes circuit strings
    """
    print("="*70)
    print("Example 5: String-Based Circuit Definition")
    print("="*70)
    
    # Parse circuit from string (like CLI does)
    circuit_string = "h:0,cx:0-1,h:1,cx:1-0"
    circuit = parse_circuit_string(circuit_string)
    
    print(f"Circuit string: {circuit_string}")
    print(f"Parsed circuit: {circuit}\n")
    
    qpu = get_ground_state(2)
    final_state = run_program(qpu, circuit)
    counts = get_counts(final_state, 1000)
    
    print(f"Results:\n{counts}\n")


def example_6_with_visualization():
    """
    Example 6: Generate visualization programmatically
    
    Creates Bell state and generates interactive plots
    """
    print("="*70)
    print("Example 6: Bell State with Visualization")
    print("="*70)
    
    circuit = [
        {"gate": "h", "target": [0]},
        {"gate": "cx", "target": [0, 1]}
    ]
    
    qpu = get_ground_state(2)
    final_state = run_program(qpu, circuit)
    counts_json = get_counts(final_state, 1000)
    counts_dict = json.loads(counts_json)
    
    print(f"Results:\n{counts_json}\n")
    print("Generating visualization...")
    
    visualize_results(counts_dict, final_state, 2)
    print("Visualization saved to quantum_results.html\n")


def example_7_phase_gates():
    """
    Example 7: Demonstrating S and T phase gates
    
    Phase gates add phase to the |1> state without affecting probabilities
    """
    print("="*70)
    print("Example 7: Phase Gates (S and T)")
    print("="*70)
    
    # Create superposition then apply phase gate
    circuit = [
        {"gate": "h", "target": [0]},  # Create superposition
        {"gate": "s", "target": [0]}   # Apply S gate (π/2 phase)
    ]
    
    qpu = get_ground_state(1)
    final_state = run_program(qpu, circuit)
    counts = get_counts(final_state, 1000)
    
    print("Circuit: H then S gate")
    print(f"Results:\n{counts}")
    print("Note: Probabilities unchanged (50/50), but relative phase is different!\n")
    
    # Now with T gate
    circuit[1] = {"gate": "t", "target": [0]}
    final_state = run_program(qpu, circuit)
    counts = get_counts(final_state, 1000)
    
    print("Circuit: H then T gate")
    print(f"Results:\n{counts}")
    print("Note: Again 50/50, but with π/4 phase instead of π/2\n")


def main():
    """Run all examples"""
    print("\n")
    print("#"*70)
    print("# QUANTUM CIRCUIT SIMULATOR - EXAMPLE DEMONSTRATIONS")
    print("#"*70)
    print("\n")
    
    example_1_bell_state()
    example_2_superposition()
    example_3_ghz_state()
    example_4_custom_gates()
    example_5_using_string_parser()
    example_6_with_visualization()
    example_7_phase_gates()
    
    print("="*70)
    print("All examples completed!")
    print("="*70)
    print("\nTo run individual examples:")
    print("  python examples.py  # Run all examples")
    print("\nOr import and use specific functions:")
    print("  from examples import example_1_bell_state")
    print("  example_1_bell_state()")
    print()


if __name__ == "__main__":
    main()
