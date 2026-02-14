import fractions
import math
import random
import numpy as np
import sympy
from typing import Callable, List, Optional, Sequence, Union
import cirq

try:
    from cirq.ops.arithmetic_operation import ArithmeticGate as _ArithmeticBase
    _ARITHMETIC_IS_GATE = True
except Exception:
    try:
        from cirq.ops.arithmetic_operation import ArithmeticOperation as _ArithmeticBase
        _ARITHMETIC_IS_GATE = False
    except Exception:
        try:
            from cirq.ops import ArithmeticOperation as _ArithmeticBase
            _ARITHMETIC_IS_GATE = False
        except Exception:
            raise SystemExit(
                "Cirq arithmetic base not found. Install a Cirq version with "
                "ArithmeticGate or ArithmeticOperation."
            )

def _as_operation(op):
    if isinstance(op, cirq.Operation):
        return op
    if _ARITHMETIC_IS_GATE:
        if hasattr(op, "on_registers"):
            try:
                candidate = op.on_registers(*op.registers())
                if isinstance(candidate, cirq.Operation):
                    return candidate
            except Exception:
                pass
        try:
            flat_qubits = []
            for reg in op.registers():
                if isinstance(reg, Sequence) and reg and isinstance(reg[0], cirq.Qid):
                    flat_qubits.extend(reg)
            if flat_qubits:
                candidate = op.on(*flat_qubits)
                if isinstance(candidate, cirq.Operation):
                    return candidate
        except Exception:
            pass
    return None

"""Function to compute the elements of Z_n."""
def multiplicative_group(n: int) -> List[int]:
    """Returns the multiplicative group modulo n.

    Args:
        n: Modulus of the multiplicative group.
    """
    assert n > 1
    group = [1]
    for x in range(2, n):
        if math.gcd(x, n) == 1:
            group.append(x)
    return group

"""Example of defining an arithmetic (quantum) operation in Cirq."""
class Adder(_ArithmeticBase):
    """Quantum addition."""
    def __init__(self, target_register, input_register):
        self.input_register = input_register
        self.target_register = target_register

    def registers(self):
        return self.target_register, self.input_register

    def with_registers(self, *new_registers):
        return Adder(*new_registers)

    def apply(self, target_value, input_value):
        return target_value + input_value

"""Example of using an Adder in a circuit."""
# Two qubit registers.
qreg1 = cirq.LineQubit.range(2)
qreg2 = cirq.LineQubit.range(2, 4)

adder_op = _as_operation(Adder(input_register=qreg1, target_register=qreg2))
if adder_op is None:
    print("Skipping Adder demo: Cirq arithmetic operations are not supported.")
else:
    # Define the circuit.
    circ = cirq.Circuit(
        cirq.ops.X.on(qreg1[0]),
        cirq.ops.X.on(qreg2[1]),
        adder_op,
        cirq.measure_each(*qreg1),
        cirq.measure_each(*qreg2)
    )

    # Display it.
    print("Circuit:\n")
    print(circ)

    # Print the measurement outcomes.
    print("\n\nMeasurement outcomes:\n")
    print(cirq.sample(circ, repetitions=5).data)


"""Example of the unitary of an Adder operation."""
adder_unitary_op = _as_operation(
    Adder(target_register=cirq.LineQubit.range(2), input_register=1)
)
if adder_unitary_op is not None:
    cirq.unitary(adder_unitary_op).real


"""Defines the modular exponential operation used in Shor's algorithm."""
class ModularExp(_ArithmeticBase):
    """Quantum modular exponentiation.

    This class represents the unitary which multiplies base raised to exponent
    into the target modulo the given modulus. More precisely, it represents the
    unitary V which computes modular exponentiation x**e mod n:

        V|y⟩|e⟩ = |y * x**e mod n⟩ |e⟩     0 <= y < n
        V|y⟩|e⟩ = |y⟩ |e⟩                  n <= y

    where y is the target register, e is the exponent register, x is the base
    and n is the modulus. Consequently,

        V|y⟩|e⟩ = (U**e|y)|e⟩

    where U is the unitary defined as

        U|y⟩ = |y * x mod n⟩      0 <= y < n
        U|y⟩ = |y⟩                n <= y
    """
    def __init__(
        self, 
        target: Sequence[cirq.Qid],
        exponent: Union[int, Sequence[cirq.Qid]], 
        base: int,
        modulus: int
    ) -> None:
        if len(target) < modulus.bit_length():
            raise ValueError(f'Register with {len(target)} qubits is too small '
                             f'for modulus {modulus}')
        self.target = target
        self.exponent = exponent
        self.base = base
        self.modulus = modulus

    def registers(self) -> Sequence[Union[int, Sequence[cirq.Qid]]]:
        return self.target, self.exponent, self.base, self.modulus

    def with_registers(
            self,
            *new_registers: Union[int, Sequence['cirq.Qid']],
    ) -> _ArithmeticBase:
        if len(new_registers) != 4:
            raise ValueError(f'Expected 4 registers (target, exponent, base, '
                             f'modulus), but got {len(new_registers)}')
        target, exponent, base, modulus = new_registers
        if not isinstance(target, Sequence):
            raise ValueError(
                f'Target must be a qubit register, got {type(target)}')
        if not isinstance(base, int):
            raise ValueError(
                f'Base must be a classical constant, got {type(base)}')
        if not isinstance(modulus, int):
            raise ValueError(
                f'Modulus must be a classical constant, got {type(modulus)}')
        return ModularExp(target, exponent, base, modulus)

    def apply(self, *register_values: int) -> int:
        assert len(register_values) == 4
        target, exponent, base, modulus = register_values
        if target >= modulus:
            return target
        return (target * base**exponent) % modulus

    def _circuit_diagram_info_(
            self,
            args: cirq.CircuitDiagramInfoArgs,
    ) -> cirq.CircuitDiagramInfo:
        assert args.known_qubits is not None
        wire_symbols: List[str] = []
        t, e = 0, 0
        for qubit in args.known_qubits:
            if qubit in self.target:
                if t == 0:
                    if isinstance(self.exponent, Sequence):
                        e_str = 'e'
                    else:
                        e_str = str(self.exponent)
                    wire_symbols.append(
                        f'ModularExp(t*{self.base}**{e_str} % {self.modulus})')
                else:
                    wire_symbols.append('t' + str(t))
                t += 1
            if isinstance(self.exponent, Sequence) and qubit in self.exponent:
                wire_symbols.append('e' + str(e))
                e += 1
        return cirq.CircuitDiagramInfo(wire_symbols=tuple(wire_symbols))

"""Create the target and exponent registers for phase estimation,
and see the number of qubits needed for Shor's algorithm.
"""
n = 15
L = n.bit_length()

# The target register has L qubits.
target = cirq.LineQubit.range(L)

# The exponent register has 2L + 3 qubits.
exponent = cirq.LineQubit.range(L, 3 * L + 3)

# Display the total number of qubits to factor this n.
print(f"To factor n = {n} which has L = {L} bits, we need 3L + 3 = {3 * L + 3} qubits.")

"""See (part of) the unitary for a modular exponential operation."""
# Pick some element of the multiplicative group modulo n.
x = 5

# Display (part of) the unitary. Uncomment if n is small enough.
# cirq.unitary(ModularExp(target, exponent, x, n))

"""Function to make the quantum circuit for order finding."""
def make_order_finding_circuit(x: int, n: int) -> cirq.Circuit:
    """Returns quantum circuit which computes the order of x modulo n.

    The circuit uses Quantum Phase Estimation to compute an eigenvalue of
    the unitary

        U|y⟩ = |y * x mod n⟩      0 <= y < n
        U|y⟩ = |y⟩                n <= y

    Args:
        x: positive integer whose order modulo n is to be found
        n: modulus relative to which the order of x is to be found

    Returns:
        Quantum circuit for finding the order of x modulo n
    """
    L = n.bit_length()
    target = cirq.LineQubit.range(L)
    exponent = cirq.LineQubit.range(L, 3 * L + 3)
    modexp_op = _as_operation(ModularExp(target, exponent, x, n))
    if modexp_op is None:
        raise SystemExit(
            "Cirq arithmetic operations are not supported in this version. "
            "Install a newer Cirq release that includes ArithmeticGate."
        )
    return cirq.Circuit(
        cirq.X(target[L - 1]),
        cirq.H.on_each(*exponent),
        modexp_op,
        cirq.qft(*exponent, inverse=True),
        cirq.measure(*exponent, key='exponent'),
    )

"""Example of the quantum circuit for period finding."""
n = 15
x = 7
circuit = make_order_finding_circuit(x, n)
print(circuit)

"""Measuring Shor's period finding circuit."""
circuit = make_order_finding_circuit(x=5, n=6)
res = cirq.sample(circuit, repetitions=8)

print("Raw measurements:")
print(res)

print("\nInteger in exponent register:")
print(res.data)

def process_measurement(result: cirq.Result, x: int, n: int) -> Optional[int]:
    """Interprets the output of the order finding circuit.

    Specifically, it determines s/r such that exp(2πis/r) is an eigenvalue
    of the unitary

        U|y⟩ = |xy mod n⟩  0 <= y < n
        U|y⟩ = |y⟩         n <= y

    then computes r (by continued fractions) if possible, and returns it.

    Args:
        result: result obtained by sampling the output of the
            circuit built by make_order_finding_circuit

    Returns:
        r, the order of x modulo n or None.
    """
    # Read the output integer of the exponent register.
    exponent_as_integer = result.data["exponent"][0]
    exponent_num_bits = result.measurements["exponent"].shape[1]
    eigenphase = float(exponent_as_integer / 2**exponent_num_bits)

    # Run the continued fractions algorithm to determine f = s / r.
    f = fractions.Fraction.from_float(eigenphase).limit_denominator(n)

    # If the numerator is zero, the order finder failed.
    if f.numerator == 0:
        return None

    # Else, return the denominator if it is valid.
    r = f.denominator
    if x**r % n != 1:
        return None
    return r

"""Example of the classical post-processing."""
# Set n and x here
n = 6
x = 5

print(f"Finding the order of x = {x} modulo n = {n}\n")
measurement = cirq.sample(circuit, repetitions=1)
print("Raw measurements:")
print(measurement)

print("\nInteger in exponent register:")
print(measurement.data)

r = process_measurement(measurement, x, n)
print("\nOrder r =", r)
if r is not None:
    print(f"x^r mod n = {x}^{r} mod {n} = {x**r % n}")

def quantum_order_finder(x: int, n: int) -> Optional[int]:
    """Computes smallest positive r such that x**r mod n == 1.

    Args:
        x: integer whose order is to be computed, must be greater than one
           and belong to the multiplicative group of integers modulo n (which
           consists of positive integers relatively prime to n),
        n: modulus of the multiplicative group.
    """
    # Check that the integer x is a valid element of the multiplicative group
    # modulo n.
    if x < 2 or n <= x or math.gcd(x, n) > 1:
        raise ValueError(f'Invalid x={x} for modulus n={n}.')

    # Create the order finding circuit.
    circuit = make_order_finding_circuit(x, n)

    # Sample from the order finding circuit.
    measurement = cirq.sample(circuit)

    # Return the processed measurement result.
    return process_measurement(measurement, x, n)

"""Functions for factoring from start to finish."""
def find_factor_of_prime_power(n: int) -> Optional[int]:
    """Returns non-trivial factor of n if n is a prime power, else None."""
    for k in range(2, math.floor(math.log2(n)) + 1):
        c = math.pow(n, 1 / k)
        c1 = math.floor(c)
        if c1**k == n:
            return c1
        c2 = math.ceil(c)
        if c2**k == n:
            return c2
    return None


def find_factor(
    n: int,
    order_finder: Callable[[int, int], Optional[int]] = quantum_order_finder,
    max_attempts: int = 30
) -> Optional[int]:
    """Returns a non-trivial factor of composite integer n.

    Args:
        n: Integer to factor.
        order_finder: Function for finding the order of elements of the
            multiplicative group of integers modulo n.
        max_attempts: number of random x's to try, also an upper limit
            on the number of order_finder invocations.

    Returns:
        Non-trivial factor of n or None if no such factor was found.
        Factor k of n is trivial if it is 1 or n.
    """
    # If the number is prime, there are no non-trivial factors.
    if sympy.isprime(n):
        print("n is prime!")
        return None

    # If the number is even, two is a non-trivial factor.
    if n % 2 == 0:
        return 2

    # If n is a prime power, we can find a non-trivial factor efficiently.
    c = find_factor_of_prime_power(n)
    if c is not None:
        return c

    for _ in range(max_attempts):
        # Choose a random number between 2 and n - 1.
        x = random.randint(2, n - 1)

        # Most likely x and n will be relatively prime.
        c = math.gcd(x, n)

        # If x and n are not relatively prime, we got lucky and found
        # a non-trivial factor.
        if 1 < c < n:
            return c

        # Compute the order r of x modulo n using the order finder.
        r = order_finder(x, n)

        # If the order finder failed, try again.
        if r is None:
            continue

        # If the order r is even, try again.
        if r % 2 != 0:
            continue

        # Compute the non-trivial factor.
        y = x**(r // 2) % n
        assert 1 < y < n
        c = math.gcd(y - 1, n)
        if 1 < c < n:
            return c

    print(f"Failed to find a non-trivial factor in {max_attempts} attempts.")
    return None

"""Example of factoring via Shor's algorithm (order finding)."""
# Number to factor
n = 15

# Attempt to find a factor
p = find_factor(n, order_finder=quantum_order_finder)
q = n // p

print("Factoring N = pq =", n)
print("p =", p)
print("q =", q)

"""Check the answer is correct."""
print(f'Did we factor {n} correctly?', p * q == n)