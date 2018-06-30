'''
qtf.py

Now we try out making the quantum fourier transform
'''
import sys, math
import numpy as np
from numpy.fft import ifft
from math import pi

from pyquil.quil import Program
import pyquil.api as api
from pyquil.api import QVMConnection
from pyquil.gates import *

def exampleQft3(q0, q1, q2):
    p = Program()
    p.inst( H(q2),
            CPHASE(pi/2.0, q1, q2),
            H(q1),
            CPHASE(pi/4.0, q0, q2),
            CPHASE(pi/2.0, q0, q1),
            H(q0),
            SWAP(q0, q2) )
    return p

def qft3(q0, q1, q2):
	p = Program()
	p.inst(H(q2),
		   CPHASE(pi/2.0, q1, q2), 
		   H(q1),
		   CPHASE(pi/4.0, q0, q2), CPHASE(pi/2.0, q0, q1),
		   H(q0))
	return p

if __name__ == "__main__":
	print('hi')
	qvm = QVMConnection()
	state_prep = Program().inst(X(0), I(1), I(2))
	# wavefunction = qvm.wavefunction(state_prep)
	# print(wavefunction)

	wavefunction = qvm.wavefunction(state_prep + qft3(0, 1, 2))
	print(wavefunction.amplitudes)
	ifft([0, 1, 0, 0, 0, 0, 0, 0], norm="ortho")
