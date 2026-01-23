# Laboratorio de Computación Cuántica

Colección práctica de notas, scripts y notebooks para desmitificar conceptos de computación cuántica con analogías accesibles y ejemplos de código listos para ejecutar.

## Mapa del repositorio

```
.
├── docs/                     # Guías narrativas para audiencias no técnicas
├── fundamentals/             # Circuitos Qiskit y demos tipo Grover
├── optimize_quantum_circuit/ # Utilidades PennyLane para circuitos variacionales
├── simulating/               # Simulaciones con NumPy y álgebra lineal básica
└── Notebook/                 # Notebooks exploratorios (retos qOSF)
```

## Conceptos clave

Para una introducción basada en analogías revisa [docs/computacion_cuantica_explicada.md](docs/computacion_cuantica_explicada.md). Allí encontrarás:

- **Bits vs qubits:** analogía de la moneda girando para explicar superposición y colapso de medición.
- **Quantum gates:** cómo las rotaciones, superposición y entanglement amplían la lógica clásica.
- **Ventaja especializada:** por qué los ordenadores cuánticos destacan en problemas tipo laberinto (criptografía, química, optimización) pero no aceleran tareas cotidianas como navegar o reproducir vídeo.
- **Limitaciones actuales:** fragilidad, tasas de error y coste que hacen a los dispositivos actuales nicho pero prometedores.

## Puesta en marcha

1. **Crear entorno (Python 3.10+ recomendado):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```
2. **Instalar dependencias principales** (ajusta según tus experimentos):
   ```bash
   pip install qiskit qiskit-aer matplotlib numpy pennylane
   ```
3. **Ejecutar un circuito de ejemplo:**
   ```bash
   python fundamentals/main.py
   ```
4. **Abrir notebooks** desde VS Code o Jupyter en las carpetas `Notebook/` u `optimize_quantum_circuit/`.

## Destacados por carpeta

- **docs/**
  - [computacion_cuantica_explicada.md](docs/computacion_cuantica_explicada.md): guía en español que contrasta computación clásica y cuántica con tablas, analogías (moneda girando, laberinto, cocina) e impacto real.
  - quantum_computing_explained.md: versión en inglés para referencia cruzada.

- **fundamentals/**
  - [main.py](fundamentals/main.py): construye un oracle de satisfacibilidad tipo Grover con la función auxiliar `XOR`, aplica un diffuser personalizado y simula el circuito en Qiskit Aer, guardando el histograma en `fundamentals/output/my_circuit.png`.

- **simulating/**
  - [operations.py](simulating/operations.py): muestra cómo representar estados, gates Hadamard, variantes de CNOT y operadores multiqubit usando NumPy puro. Ideal para afianzar el álgebra tensorial sin frameworks pesados.
  - Scripts adicionales (`apply_gates.py`, `code_gates.py`, `code_numpy.py`) amplían estos experimentos en utilidades reutilizables.

- **optimize_quantum_circuit/**
  - [surface_plot.py](optimize_quantum_circuit/surface_plot.py): renderiza superficies de coste en 3D para circuitos variacionales de dos parámetros, incluyendo la trayectoria de optimizadores como Adam.
  - `hello_pennylane.ipynb`: notebook interactivo para ajustar plantillas y optimizadores con PennyLane.

- **Notebook/**
  - `qosf-simulator-task.ipynb`: avances hacia el reto de la Quantum Open Source Foundation, mostrando uso de simuladores y tareas personalizadas.

## Flujo de trabajo sugerido

1. **Absorbe la intuición** leyendo el material en `docs/`.
2. **Simula con NumPy** en `simulating/` para afianzar fundamentos de álgebra lineal.
3. **Escala con Qiskit** en `fundamentals/` para construir oracles y visualizar mediciones.
4. **Experimenta con circuitos variacionales** usando las utilidades de PennyLane en `optimize_quantum_circuit/`.
5. **Documenta aprendizajes** o nuevos experimentos en `docs/` o `Notebook/` para futuras colaboraciones.

## Guía de contribución

- Mantén un tono accesible; prioriza analogías y visuales para nuevas personas en el tema.
- Al añadir código, incluye comentarios breves que expliquen el flujo cuántico o la intención matemática.
- Guarda salidas de simulador (plots, histogramas) en `output/` dedicados para evitar recomputar tareas pesadas.

## Ideas de roadmap

- Completar la documentación en español hasta alcanzar paridad con la guía inglesa.
- Añadir tests o scripts de benchmark para las implementaciones de gates en `simulating/`.
  
- Incluir ejemplos híbridos PennyLane/Qiskit que muestren algoritmos variacionales en simuladores.
- Documentar pasos para ejecutar notebooks en hardware cuántico real cuando sea posible.

Recuerda: cada herramienta cuántica tiene su problema ideal; el truco está en elegir el escenario adecuado.
# links
- https://jonathan-hui.medium.com/qc-programming-with-quantum-gates-8996b667d256
