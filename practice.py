'''
practice.py
'''

# from pyquil.quil import Program
# from pyquil.gates import X
# from pyquil.api import QVMConnection

# qvm = QVMConnection()
# p = Program()
# p.inst(X(0)).measure(0, 1)

# print(p)
# print(qvm.run(p, [0, 1, 2], 3))



# from squanch import *

# def string_to_bits(msg):
#     # Return a string of 0's and 1's from a message
#     bits = ""
#     for char in msg: bits += "{:08b}".format(ord(char))
#     return bits

# def bits_to_string(bits):
#     # Return a message from a binary string
#     msg = ""
#     for i in range(0, len(bits), 8):
#         digits = bits[i:i + 8]
#         msg += chr(int(digits, 2))
#     return msg

# msg = "Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! "
# bits = string_to_bits(msg)

# class Alice(Agent):
#     def run(self):
#         for qsys, bit in zip(self.stream, self.data):
#             q, = qsys.qubits
#             if bit == "1": X(q)
#             self.qsend(bob, q)


# class Bob(Agent):
#     def run(self):
#         bits = ""
#         for _ in self.stream:
#             q = self.qrecv(alice)
#             bits += str(q.measure())
#         self.output(bits)

# mem = Agent.shared_hilbert_space(1, len(bits))
# out = Agent.shared_output()

# alice = Alice(mem, data = bits)
# bob = Bob(mem, out = out)

# alice.qconnect(bob)

# # alice.start()
# # bob.start()

# # alice.join()
# # bob.join()

# # received_msg = bits_to_string(out["Bob"])
# # print("Alice sent: '{}'. Bob received: '{}'.".format(msg, received_msg))

# Simulation(alice, bob).run()
# received_msg = bits_to_string(out["Bob"])
# print("Alice sent: '{}'. Bob received: '{}'.".format(msg, received_msg))


# import numpy as np
# import matplotlib.pyplot as plt
# from squanch import *

# class Alice(Agent):
#     '''Alice sends qubits to Bob using a shared Bell pair'''
    
#     def distribute_bell_pair(self, a, b):
#         # Create a Bell pair and send one particle to Bob
#         H(a)
#         CNOT(a, b)
#         self.qsend(bob, b)

#     def teleport(self, q, a):
#         # Perform the teleportation
#         CNOT(q, a)
#         H(q)
#         # Tell Bob whether to apply Pauli-X and -Z over classical channel
#         bob_should_apply_x = a.measure() # if Bob should apply X
#         bob_should_apply_z = q.measure() # if Bob should apply Z
#         self.csend(bob, [bob_should_apply_x, bob_should_apply_z])

#     def run(self):
#         for qsystem in self.stream:
#             q, a, b = qsystem.qubits # q is state to teleport, a and b are Bell pair
#             self.distribute_bell_pair(a, b)
#             self.teleport(q, a)

# class Bob(Agent):
#     '''Bob receives qubits from Alice and measures the results'''

#     def run(self):
#         measurement_results = []
#         for _ in self.stream:
#             # Bob receives a qubit from Alice
#             b = self.qrecv(alice) 
#             # Bob receives classical instructions from alice
#             should_apply_x, should_apply_z = self.crecv(alice)
#             if should_apply_x: X(b)
#             if should_apply_z: Z(b)
#             # Measure the output state
#             measurement_results.append(b.measure())
#         # Put results in output object
#         self.output(measurement_results)


# # Allocate memory and output structures
# mem = Agent.shared_hilbert_space(3, 10) # 3 qubits per trial, 10 trials
# out = Agent.shared_output()

# # Prepare the initial states
# stream = QStream.from_array(mem)
# states_to_teleport = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
# for state, qsystem in zip(states_to_teleport, stream):
#     q = qsystem.qubit(0)
#     if state == 1: X(q) # flip the qubits corresponding to 1 states

# # Make and connect the agents
# alice = Alice(mem, out)
# bob = Bob(mem, out)
# alice.qconnect(bob) # add a quantum channel
# alice.cconnect(bob) # add a classical channel

# # Run everything
# alice.start()
# bob.start()
# alice.join()
# bob.join()

# print("Teleported states {}".format(states_to_teleport))
# print("Received states   {}".format(out["Bob"]))



# angles = np.linspace(0, 2 * np.pi, 50)  # RX angles to apply
# num_trials = 250  # number of trials for each angle

# # Allocate memory and output structures
# mem = Agent.shared_hilbert_space(3, len(angles) * num_trials)
# out = Agent.shared_output()

# # Prepare the initial states in the stream
# stream = QStream.from_array(mem)
# for angle in angles:
#     for _ in range(num_trials):
#         q, _, _ = stream.next().qubits
#         RX(q, angle)

# # Make the agents and connect with quantum and classical channels
# alice = Alice(mem, out = out)
# bob = Bob(mem, out = out)
# alice.qconnect(bob)
# alice.cconnect(bob)

# # Run the simulation
# Simulation(alice, bob).run()

# # Plot the results
# results = np.array(out["Bob"]).reshape((len(angles), num_trials))
# observed = np.mean(results, axis = 1)
# expected = np.sin(angles / 2) ** 2
# plt.plot(angles, observed, label = 'Observed')
# plt.plot(angles, expected, label = 'Expected')
# plt.legend()
# plt.xlabel("$\Theta$ in $R_X(\Theta)$ applied to qubits")
# plt.ylabel("Fractional $\left | 1 \\right >$ population")
# plt.show()





from squanch import *
import numpy as np

_Z = np.array([[1, 0],[0, -1]])

def transport4(a, b, c, d, e):
	H(a)
	a_res = a.measure()
	H(b)
	b_res = b.measure()
	H(c)
	c_res = c.measure()
	H(d)
	d_res = d.measure()
	if (a_res == 1 or c_res == 1) and not (a_res == 1 and c_res == 1):
		Z(c)
	if (b_res == 1 or d_res == 1) and not (b_res == 1 and d_res == 1):
		X(c)
	return a_res, b_res, c_res, d_res

def testtransportlen4():
	results = []

	for _ in range(10):
		qsys = QSystem(5)
		a, b, c, d, e = qsys.qubits
		# prepare

		# X(a)
		# H(a)

		H(b)
		H(c)
		H(d)
		H(e)
		CU(a, b, _Z)
		CU(b, c, _Z)
		CU(c, d, _Z)
		CU(d, e, _Z)
		# measure
		a_res, b_res, c_res, d_res = transport4(a, b, c, d, e)

		H(e)
		X(e)
		e_res = c.measure()

		results.append((a_res, b_res, c_res, d_res, e_res))

	print(results)

def transport3(a, b, c):
	H(a)
	a_res = a.measure()
	H(b)
	b_res = b.measure()
	if a_res == 1:
		Z(c)
	if b_res == 1:
		X(c)
	return a_res, b_res

def testtransportlen3():
	results = []

	for _ in range(10):
		qsys = QSystem(4)
		a, b, c, d = qsys.qubits
		# prepare

		# X(a)
		# H(a)

		H(b)
		H(c)
		H(d)
		CU(a, b, _Z)
		CU(b, c, _Z)
		CU(c, d, _Z)
		# measure
		a_res, b_res = transport3(a, b, c)

		H(c)
		X(c)
		c_res = c.measure()

		results.append((a_res, b_res, c_res))

	print(results)

def transport2(a, b, c):
	H(a)
	a_res = a.measure()
	H(b)
	b_res = b.measure()
	if a_res == 1:
		Z(c)
	if b_res == 1:
		X(c)
	return a_res, b_res

def testtransportlen2():
	results = []

	for _ in range(10):
		qsys = QSystem(3)
		a, b, c = qsys.qubits
		# prepare

		X(a)
		H(a)

		H(b)
		H(c)
		CU(a, b, _Z)
		CU(b, c, _Z)
		# measure
		a_res, b_res = transport2(a, b, c)

		H(c)
		X(c)
		c_res = c.measure()

		results.append((a_res, b_res, c_res))

	print(results)

def transport1(a, b):
	H(a)
	a_res = a.measure()
	if a_res == 1:
		Z(b)
	# if a_res == 1:
	# 	X(b)
	return a_res

def testtransportlen1():
	results = []

	for _ in range(10):
		qsys = QSystem(2)
		a, b = qsys.qubits
		# prepare

		# X(a)
		# H(a)

		H(b)
		CU(a, b, _Z)
		# measure
		a_res = transport1(a, b)

		# H(b)
		# X(b)
		b_res = b.measure()

		results.append((a_res, b_res))

	print(results)


if __name__ == "__main__":
	testtransportlen4()













