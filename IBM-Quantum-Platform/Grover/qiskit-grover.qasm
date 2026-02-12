OPENQASM 2.0;
include "qelib1.inc";

qreg qregless[3];
creg c[3];

// Initialize in uniform superposition
h qregless[0];
h qregless[1];
h qregless[2];

// Oracle marking |101> and |110>
cz qregless[0], qregless[2];
cz qregless[1], qregless[2];

// Diffuser
h qregless[0];
h qregless[1];
h qregless[2];

x qregless[0];
x qregless[1];
x qregless[2];

h qregless[2];
ccx qregless[0], qregless[1], qregless[2];
h qregless[2];

x qregless[0];
x qregless[1];
x qregless[2];

h qregless[0];
h qregless[1];
h qregless[2];

// Measurement
measure qregless[0] -> c[0];
measure qregless[1] -> c[1];
measure qregless[2] -> c[2];
