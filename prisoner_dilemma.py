'''
prisoner's dilemma game
for more information see
https://en.wikipedia.org/wiki/Prisoner%27s_dilemma
http://pyquil.readthedocs.io/en/latest/qvm.html#qvm
'''

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
quantum decisions instead of only classical decisions

Here, to prove the point, we only let you make a classical decision
and then let your buddy make a quantum deicion

Enter if you want to 'snitch' or if you stay 'silent'
"""

print(mes)


if len(sys.argv) < 2:
	print('enter a command line argument \n \'snitch\' if you want to snitch or \'silent\' 1 if you want to keep quiet')
	exit(1)
if str(sys.argv[1]) != 'snitch' and str(sys.argv[1]) != 'silent':
	print('enter a command line argument \n \'snitch\' if you want to snitch or \'silent\' 1 if you want to keep quiet')
	exit(1)
choice = str(sys.argv[1])
if choice == 'snitch':
	print('you chose to snitch!')
	choice = 1
elif choice == 'silent':
	choice = 0
	print('you chose to keep quiet!')

quit(0)

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


