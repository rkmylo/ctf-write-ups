from z3 import *

s = Solver()

flag = []
for i in range(25):
    c = Int("flag_{}".format(i))
    s.add(c >= 0x20, c <= 0x7e)
    flag.append(c)

s.add(flag[0]  + flag[9]  == 0x8b)
s.add(flag[1]  + flag[7]  == 0xce)
s.add(flag[2]  + flag[11] == 0xb0)
s.add(flag[3]  + flag[6]  == 0x89)
s.add(flag[4]  + flag[12] == 0x7b)
s.add(flag[5]  + flag[8]  == 0xb0)
s.add(flag[24] + flag[10] == 0xb0)
s.add(flag[13] + flag[22] + flag[23] == 0xee)
s.add(flag[14] + flag[20] + flag[16] == 0xbf)
s.add(flag[13] + flag[10] == 0x92)
s.add(flag[20] + flag[12] == 0x65)
s.add(flag[14] + flag[11] == 0x9d)
s.add(flag[23] + flag[7]  == 0x9a)
s.add(flag[15] + flag[10] == 0x99)
s.add(flag[19] + flag[12] == 0x99)
s.add(flag[18] + flag[8]  == 0x94)
s.add(flag[17] + flag[7]  == 0xad)
s.add(flag[21] + flag[11] == 0xe4)

# using only the above constraints, more than 1 models
# are found that satisfy the conditions
s.add(flag[0] == ord('T'))
s.add(flag[1] == ord('U'))
s.add(flag[2] == ord('C'))
s.add(flag[3] == ord('T'))
s.add(flag[4] == ord('F'))
s.add(flag[5] == ord('{'))
s.add(flag[24] == ord('}'))

if s.check() == sat:
    flag = map(lambda x: chr(int(str(s.model()[x]))), flag)
    print "".join(flag)

# TUCTF{5y573m5_0f_4_d0wn!}
