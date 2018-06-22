'''
Meyer-Penny Game!

Just to practice a bit
'''

import sys

mes = """=====================================================
Picard v.s. Q in the penny flipping game!
see
http://pyquil.readthedocs.io/en/latest/qvm.html#id3
for details on implementation.
=====================================================
You are stuck in a penny flipping game? Do you flip the coin or not?

"""
print(mes)

if len(sys.argv) < 2:
	print('enter a command line argument \n 0 if you want to not flip the coin and 1 if you want to flip')
	exit(1)
if int(sys.argv[1]) != 0 and int(sys.argv[1]) != 1:
	print('enter 0 if you want to not flip the coin and 1 if you want to flip')
	exit(1)
choice = int(sys.argv[1])
if choice == 1:
	print('you chose to flip the penny')
else:
	print('you chose to not flip the penny!')

###########################################
# Quantum Stuff


from pyquil.quil import Program
import pyquil.api as api

from pyquil.gates import I, H, X, Y, CNOT

qvm = api.QVMConnection()

penny_register = 0


if choice == 1:
	# You choose to flip the bit
	your_action = X(0)
else:
	# You choose to do nothing
	your_action = I(0)

prog = (Program().
	inst(
	# the bit starts out in Heads, represented as |1>
	X(0),
	# Q puts penny in superposition of states by applying the Hadamard gate
	H(0),
	# Your action
	your_action,
	# Q again applys the Hadamard gate
	H(0)).
	# measurement 
	measure(0, penny_register)
	)

result = qvm.run(prog, [0])
print(result)
if result[0][0] == 1:
	print('Looks like Q won and you\'re lost in space')
else:
	print('Wow!...\n How\'d you win?')


