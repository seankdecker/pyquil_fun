'''
prisoner's dilemma game
for more information see
https://en.wikipedia.org/wiki/Prisoner%27s_dilemma
http://pyquil.readthedocs.io/en/latest/qvm.html#qvm

This is built off of the pyquil python library for quantum computing
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
	Here you are a prisoner and this is the dilemma:
	You, Y, and your buddy, B,  got caught robbing a bank.
	You and your buddy have two options. Either you
	stay silent or snitch on the other. What you and your buddy choose
	will result in different rewards for either of you.
	There are 4 possible outcomes for rewards:
	 
	               Y silent         Y snitches
	B silent    Y, B <- -1, -1   Y, B <- 0, -3 
	B snitches  Y, B <- -3, 0    Y, B <- -2, -2

	Classically, this results in a Nash Equilibrium in which
	both players snitch. The players can do better if they are allowed
	quantum decisions instead of only classical decisions. How I understand
	this is that quantum decisions allow the players an 2 extra dimensions
	on which to play the game. In a game in which their actions are entangled then,
	this allows for some sort of tranfer of information and subsequent interaction
	between the players' choices, even if the player are unaware of the actions of 
	the other player.

	For more information on the abstraction of this game into a quantum world
	see:
		https://arxiv.org/pdf/quant-ph/9806088.pdf

	To sum up we assume that we start in the state |CC> and then these decisions
	are maximally entangled with the operator J = exp(ipi/4(D x D))

	You and your buddy then make a decision which is equated to you both acting
	on your repective state with some operator.

	Then we act on the reulting 2 bit state with J^t and find what the result is

	Here, to prove the point, we only let you make a classical decision
	and then let your buddy make a quantum deicion. So you can only choose an 
	X or I gate. 

	Enter if you want to 'snitch' or if you stay 'silent'
	"""
	print(mes)

def parseChoice():
	if len(sys.argv) < 2:
		print('enter a command line argument \n \'snitch\' if you want to snitch or \'silent\' 1 if you want to keep quiet')
		exit(1)
	if str(sys.argv[1]) != 'snitch' and str(sys.argv[1]) != 'silent':
		print('enter a command line argument \n \'snitch\' if you want to snitch or \'silent\' 1 if you want to keep quiet')
		exit(1)
	choice = str(sys.argv[1])
	if choice == 'snitch':
		print('you chose to snitch! So you are applying a NOT gate')
	elif choice == 'silent':
		print('you chose to keep quiet! So you are applying an idenity gate')
	else:
		print("ERROR, idk what you typed")
		quit(1)
	return choice


######################################################################################
# Quantum Stuff
######################################################################################

def parseResult(result):
	for game in result:
		if game[0] == 1:
			if game[1] == 1:
				print('You both stayed quiet! You get -1 points')
			else:
				print('You stayed quiet, but your buddy snitched! You get -3 points')
		else:
			if game[1] == 1:
				print('You snitched on a silent friend! You get 0 points')
			else:
				print('You both are rats. -2 points')



def runGame(choice):
	qvm = api.QVMConnection()
	yourChoiceRegister = 0
	buddyChoiceRegister = 1
	
	p = Program()

	j = np.array([[1.0 / math.sqrt(2), 0, 0, 1.0j / math.sqrt(2)], 
				  [0, 1.0 / math.sqrt(2), 1.0j / math.sqrt(2), 0],
				  [0, 1.0j / math.sqrt(2), 1.0 / math.sqrt(2), 0],
				  [1.0j / math.sqrt(2), 0, 0, 1.0 / math.sqrt(2)]])
	p.defgate('J', j)

	jt = np.array([[1.0 / math.sqrt(2), 0, 0, -1.0j / math.sqrt(2)], 
				   [0, 1.0 / math.sqrt(2), -1.0j / math.sqrt(2), 0],
				   [0, -1.0j / math.sqrt(2), 1.0 / math.sqrt(2), 0],
				   [-1.0j / math.sqrt(2), 0, 0, 1.0 / math.sqrt(2)]])
	p.defgate('Jt', jt)

	if choice == 'snitch':
		yourAction = X(yourChoiceRegister)
	elif choice == 'silent':
		yourAction = I(yourChoiceRegister)

	print('your buddy will play the miracle move:')
	miracleMove = np.array([[ 1.0j / math.sqrt(2), 1.0/ math.sqrt(2)],
							 [-1.0 / math.sqrt(2), -1.0j/ math.sqrt(2)]])
	p.defgate('MIRACLE', miracleMove)
	buddyAction = (('MIRACLE', buddyChoiceRegister))

	p.inst(('J', 0, 1), yourAction, buddyAction, ('Jt', 0, 1), MEASURE(1, 1), MEASURE(0, 0))
	print(p)
	result = qvm.run(p, [0, 1], 90)
	print(result)

	parseResult(result)

if __name__ == "__main__":
	introduction()
	choice = parseChoice()
	runGame(choice)
	quit()
