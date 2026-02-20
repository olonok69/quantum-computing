# Quantum Computing Playground (ES)

Coleccion practica de scripts, notebooks y notas para explorar computacion cuantica con Qiskit, Cirq, PennyLane y un simulador propio basado en NumPy. El repo mezcla explicaciones para principiantes con demos ejecutables de Grover, Deutsch-Jozsa, Shor (ejemplo toy) y simulacion de state vector.

## Mapa del repositorio

```
.
├── algorithms/                 # Demos de algoritmos en Qiskit
├── DJ-Algorithm/               # Deutsch-Jozsa en Qiskit y Cirq
├── docs/                       # Guias introductorias (EN/ES)
├── fundamentals/               # Oraculo y diffuser estilo Grover
├── Grover/                     # Grover en Qiskit y Cirq
├── IBM-Quantum-Platform/       # QASM y ejemplos Qiskit para IBM
├── Notebook/                   # Notebooks (qOSF tasks, random walk)
├── optimize_quantum_circuit/   # Visualizacion de cost landscape en PennyLane
├── shor/                       # Shor (toy N=15) en Qiskit y Cirq
├── simulating/                 # Simulador NumPy + CLI + plots
├── quantum_results.html        # Salida Plotly (generada)
├── grover_circuit.png          # Salida de Grover en Qiskit
├── bell_state_histogram.png    # Histograma Bell-state en Qiskit
└── References.md               # Referencias externas y lecturas
```

## Inicio rapido

### 1) Crear y activar entorno virtual

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2) Instalar dependencias base

```powershell
python -m pip install qiskit qiskit-aer cirq pennylane matplotlib numpy plotly
```

### 3) Ejecutar algunas demos

```powershell
python fundamentals\main.py
python Grover\qiskit_grover.py
python DJ-Algorithm\main_qiskit.py
python simulating\quantum_simulator.py --visualize
```

## Documentacion

- docs/quantum_computing_explained.md: Introduccion en lenguaje sencillo con analogias y casos de uso.
- docs/computacion_cuantica_explicada.md: Version en espanol del mismo contenido.
- README.md: Vista general del repo en ingles.

## Algoritmos y demos por carpeta

### algorithms/
- bell_state_qiskit.py: Crea un Bell pair, lo mide y guarda bell_state_histogram.png.
- beel_state_cirq.py: Ejemplo de Bell state en Cirq.

### DJ-Algorithm/
- main_qiskit.py: Deutsch-Jozsa con oraculo balanced/constant, genera dj_circuit.png y dj_histogram.png.
- main.cirq.py: Deutsch-Jozsa en Cirq con 3 qubits de entrada + ancilla.
- dj_circuit.txt: Notas del circuito.

### Grover/
- qiskit_grover.py: Grover search con oraculo de 3 qubits que marca |101> y |110>, guarda grover_circuit.png.
- cirq_grover.py: Grover search con oraculo de 2 qubits y ancilla, imprime resultados.

### shor/
- shor_qiskit.py: Demo toy de Shor para N=15 con Qiskit Aer. Soporta parametros CLI para N (fijo a 15 en esta demo) y a (uno de 2,7,8,11,13).
  - Ejemplo: `python shor\shor_qiskit.py -n 15 -a 7`
- shor_cirq.py: Order-finding con Cirq usando arithmetic operations. Requiere una version de Cirq con soporte de ArithmeticGate.

### fundamentals/
- main.py: Construye un oracle estilo SAT (XOR clauses), un diffuser y ejecuta el circuito en Aer. Guarda el histograma en fundamentals/output/my_circuit.png.

### optimize_quantum_circuit/
- surface_plot.py: Visualiza cost landscape y trayectorias de optimizadores con PennyLane.
- hello_pennylane.ipynb: Notebook interactivo para variational circuits y optimizers.

### simulating/
- quantum_simulator.py: Simulador NumPy con CLI y visualizaciones Plotly.
- examples.py: Varios circuitos de ejemplo.
- QUICKSTART.md y README.md: Uso, argumentos de CLI y troubleshooting.

### IBM-Quantum-Platform/
- DJ-Algorithm/openqasm-dj.qasm: OpenQASM de Deutsch-Jozsa.
- DJ-Algorithm/qiskit-dj.py: Implementacion Qiskit para IBM.
- Grover/qiskit-grover.py y qiskit-grover.qasm: Grover en Qiskit y QASM.

### Notebook/
- qosf-simulator-task.ipynb: Experimentos del reto QOSF.
- quantum_random_walk.ipynb: Notebook de random walk.

## Simulador propio (simulating/)

El simulador acepta un string compacto de circuito:

```
python simulating\quantum_simulator.py -q 3 -s 1500 -c "h:0,h:1,cx:0-2,cx:1-2,x:0" --visualize
```

Gates soportadas: h, x, y, z, s, t, i, cx.

La salida incluye un dashboard Plotly en quantum_results.html con:
- Measurement counts
- State vector amplitudes
- Theoretical probabilities
- Measured vs theoretical comparison

## Notas de version

- Qiskit Aer es un paquete separado (qiskit-aer). Las demos usan AerSimulator en versiones nuevas.
- La demo de Shor en Cirq necesita ArithmeticGate. Si aparece un error sobre arithmetic operations, actualiza Cirq.

## Contribuir

- Mantener explicaciones claras y concretas.
- Agregar comentarios breves cuando el paso cuantico no sea obvio.
- Guardar imagenes generadas cerca de los scripts o en carpetas output/.

## Referencias

- References.md para lecturas recomendadas.
- Qiskit documentation: https://docs.quantum.ibm.com/
- Cirq documentation: https://quantumai.google/cirq
- PennyLane documentation: https://pennylane.ai/
