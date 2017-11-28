from z3 import *
from itertools import product

a, b, c, d, e = Ints('a b c d e')

s = Solver()

s.add(a > 0, a <= 9)
s.add(b > 0, b <= 9)
s.add(c > 0)
s.add(d > 0)
s.add(e > 0)

s.add(a + b == c)
s.add(c * c == d)
s.add(d + d == e)
s.add(e * e == 82944)

pairs = []

while True:
    if s.check() == unsat:
        break
    m = s.model()
    pairs.append([m[a], m[b]])
    s.add(a != m[a])

pairs = map(lambda x: str(x[0]) + str(x[1]), pairs)
print "[+] found {} pairs".format(len(pairs))

for p in pairs:
    print p

pairs = list(product(pairs, repeat=8))
print "[+] generated {} valid keys".format(len(pairs))

with open("grammar_keys.txt", "w") as f:
    for p in pairs:
        f.write("(%s,%s-%s,%s&%s,%s-%s,%s)\n" % p)
