'''
practice.py
'''

from pyquil.quil import Program
from pyquil.gates import X
from pyquil.api import QVMConnection

qvm = QVMConnection()
p = Program()
p.inst(X(0)).measure(0, 1)

print(p)
print(qvm.run(p, [0, 1, 2], 3))