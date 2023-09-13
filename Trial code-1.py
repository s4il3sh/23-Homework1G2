from qiskit import QuantumCircuit, transpile, Aer, execute

# Define the classical numbers to be added
number1 = 30
number2 = 2

# Determine the number of qubits needed to represent the numbers
max_value = max(number1, number2)
num_qubits = max(1, (max_value.bit_length() + 1))

# Create a quantum circuit with enough qubits
qc = QuantumCircuit(num_qubits * 2, num_qubits)

# Encode the classical numbers into quantum states
for i in range(num_qubits):
    if (number1 >> i) & 1:
        qc.x(i)  # Apply X gate for 1 bits in number1
    if (number2 >> i) & 1:
        qc.x(i + num_qubits)  # Apply X gate for 1 bits in number2

# Perform the addition by applying CNOT gates
for i in range(num_qubits - 1):
    qc.ccx(i, i + num_qubits, i + num_qubits + 1)
    qc.cx(i, i + num_qubits)

# Measure the result
qc.measure(range(num_qubits, num_qubits * 2), range(num_qubits))

# Simulate the circuit
simulator = Aer.get_backend('qasm_simulator')
compiled_circuit = transpile(qc, simulator)
job = execute(compiled_circuit, simulator, shots=1)
result = job.result()

# Get the measurement result
counts = result.get_counts(qc)
result_decimal = int(list(counts.keys())[0], 2)

# Print the result
print(f"The result of {number1} + {number2} is {result_decimal}")

#adding counts code to visualize clearly the binary number.
print(counts)
plot_histogram(counts)
