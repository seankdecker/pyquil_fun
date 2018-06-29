'''
Deutsh algorithm

To practice, let's make the deutsh algorithm
'''

import sys
import math
import numpy as np

from pyquil.quil import Program
import pyquil.api as api
from pyquil.gates import *


######################################################################################
# Message Stuff
######################################################################################

def introduction():
	mes = """
	We will implement Deutsch's algorithm for some practice with pyquil
	Enter the one bit gate that you would like to investigate with Deutsch's:

	choices: X, I, 1, 0
	"""
	print(mes)

def parseChoice():
	if len(sys.argv) < 2:
		print('enter a command line argument for the gate you want to investigate: \
			\n \'X\', \'I\', \'1\', or \'0\'')
		exit(1)
	if str(sys.argv[1]) != 'X' and str(sys.argv[1]) != 'I' and str(sys.argv[1]) != '0' and str(sys.argv[1]) != '1':
		print('enter a command line argument for the gate you want to investigate: \
			\n \'X\', \'I\', \'1\', or \'0\'')
		exit(1)
	# we set f to the function entered by the user
	if str(sys.argv[1]) == 'X':
		f = lambda x: (x + 1)%2
	elif str(sys.argv[1]) == 'I':
		f = lambda x: x
	elif str(sys.argv[1]) == '1':
		f = lambda x: 1
	elif str(sys.argv[1]) == '0':
		f = lambda x: 0
	return f


######################################################################################
# Quantum Stuff
######################################################################################

# We now define a 4 x 4 matrix that corresponds to a controlled f(x) on the second bit
# based on https://cs.uwaterloo.ca/~watrous/LectureNotes/CPSC519.Winter2006/04.pdf
# Note, we can't simply make a controlled U gate out of f() because f() does not
# define a unitary operator
def controlled(u):
	print('Your controlled f gate then corresponds to:')
	cu = np.array([[(f(0) + 1)%2, f(0)%2, 0, 0], 
				   [f(0)%2, (1 + f(0))%2, 0, 0], 
				   [0, 0, (1 + f(1))%2, f(1)%2], 
				   [0, 0, f(1)%2, (1 + f(1))%2]])
	print(cu)
	return cu

def parseResult(result):
	if result[0][0] == 1:
		print('looks like this is a balenced function!')
	else:
		print('it\'s a constant function!')


def runAlg(cf):
	qvm = api.QVMConnection()	
	p = Program()
	p.defgate('cF', cf)

	p.inst(
		# Prepare 0 as a superposition |0> + |1>
		# Prepare 1 as the Fourier Transform of |0> - |1>
		H(0), X(1), H(1),
		('cF', 0, 1), H(0), MEASURE(0, 0))
	print(p)
	result = qvm.run(p, [0], 10)
	print(result)
	parseResult(result)

if __name__ == "__main__":
	introduction()
	f = parseChoice()
	cf = controlled(f)
	runAlg(cf)
	quit()
