'''
practice.py

testing to see if I can implement a 1 way quantum computer works in pyquil
'''

from pyquil.quil import Program
from pyquil.gates import *
from pyquil.api import QVMConnection

# measures qubit at index i in the basis of X
def measureX(i):
	p = Program()
	p.inst(H(i)).measure(i, i)
	return p

# after this propagation, we need to correct the final qubit
# the final qubit will be in the state X^{s_1 + s_3}Z^{s_0 + s_2}|\psi>
# where s_i is the result of measuring qubit i using measureX
# and |\psi> is the initial state of qubit 0
# after the steps prepareEntanglements() + measureX(0)  + measureX(1) + measureX(2) + measureX(3)
# in transportation

# After the corrections have been made, we should leave qubit 4 in the state |\psi>
def correctAndMeasure(i):
	thenX_branch = Program(X(i))
	elseX_branch = Program()
	thenZ_branch = Program(Z(i))
	elseZ_branch = Program()

	p = Program()
	p.inst().if_then(1, thenX_branch, elseX_branch).if_then(3, thenX_branch, elseX_branch).if_then(0, thenZ_branch, elseZ_branch).if_then(2, thenZ_branch, elseZ_branch).measure(i, i)
	return p

# prepares the state:
# |0> - |+> - |+> - |+> - |+>
# where - represents CZ entanglements and |1> and |+> are as usual
def prepareEntanglements():
	state_prep = Program().inst(I(0), H(1), H(2), H(3), H(4), CZ(0, 1), CZ(1, 2), CZ(2, 3), CZ(3, 4))
	return state_prep


if __name__ == "__main__":
	qvm = QVMConnection()
	
	# wavefunction = qvm.wavefunction(state_prep)
	# print(wavefunction)

	trasportation = prepareEntanglements() + measureX(0)  + measureX(1) + measureX(2) + measureX(3) + correctAndMeasure(4)

	print(trasportation)
	results = qvm.run(trasportation, [0, 1, 2, 3, 4], 10)
	print(results)

	# see if it all worked out
	for run in results:
		if run[4] == 1:
			print("Failed")
			quit(1)
	print("Okay cool, so it looks like it is working")
