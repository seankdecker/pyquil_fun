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

from squanch import *

def string_to_bits(msg):
    # Return a string of 0's and 1's from a message
    bits = ""
    for char in msg: bits += "{:08b}".format(ord(char))
    return bits

def bits_to_string(bits):
    # Return a message from a binary string
    msg = ""
    for i in range(0, len(bits), 8):
        digits = bits[i:i + 8]
        msg += chr(int(digits, 2))
    return msg

msg = "Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! Hello, Bob! "
bits = string_to_bits(msg)

class Alice(Agent):
    def run(self):
        for qsys, bit in zip(self.stream, self.data):
            q, = qsys.qubits
            if bit == "1": X(q)
            self.qsend(bob, q)


class Bob(Agent):
    def run(self):
        bits = ""
        for _ in self.stream:
            q = self.qrecv(alice)
            bits += str(q.measure())
        self.output(bits)

mem = Agent.shared_hilbert_space(1, len(bits))
out = Agent.shared_output()

alice = Alice(mem, data = bits)
bob = Bob(mem, out = out)

alice.qconnect(bob)

# alice.start()
# bob.start()

# alice.join()
# bob.join()

# received_msg = bits_to_string(out["Bob"])
# print("Alice sent: '{}'. Bob received: '{}'.".format(msg, received_msg))

Simulation(alice, bob).run()
received_msg = bits_to_string(out["Bob"])
print("Alice sent: '{}'. Bob received: '{}'.".format(msg, received_msg))



