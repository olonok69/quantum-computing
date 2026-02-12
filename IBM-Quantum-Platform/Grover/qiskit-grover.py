from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

qreg_qregless = QuantumRegister(3, "qregless")
creg_c = ClassicalRegister(3, "c")
circuit = QuantumCircuit(qreg_qregless, creg_c)

# Initialize in uniform superposition
circuit.h(qreg_qregless[0])
circuit.h(qreg_qregless[1])
circuit.h(qreg_qregless[2])

# Oracle marking |101> and |110>
circuit.cz(qreg_qregless[0], qreg_qregless[2])
circuit.cz(qreg_qregless[1], qreg_qregless[2])

# Diffuser
circuit.h(qreg_qregless[0])
circuit.h(qreg_qregless[1])
circuit.h(qreg_qregless[2])

circuit.x(qreg_qregless[0])
circuit.x(qreg_qregless[1])
circuit.x(qreg_qregless[2])

circuit.h(qreg_qregless[2])
circuit.mcx([qreg_qregless[0], qreg_qregless[1]], qreg_qregless[2])
circuit.h(qreg_qregless[2])

circuit.x(qreg_qregless[0])
circuit.x(qreg_qregless[1])
circuit.x(qreg_qregless[2])

circuit.h(qreg_qregless[0])
circuit.h(qreg_qregless[1])
circuit.h(qreg_qregless[2])

# Measurement
circuit.measure(qreg_qregless[0], creg_c[0])
circuit.measure(qreg_qregless[1], creg_c[1])
circuit.measure(qreg_qregless[2], creg_c[2])
