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
both players snitch. We can do better with Quantum Computation
"""

print(mes)