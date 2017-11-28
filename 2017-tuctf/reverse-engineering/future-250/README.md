## Future (Reverse Engineering, 250pt)

> Future me gave me this and told me to add it to TUCTF. I dunno, he sounded crazy. Anyway, Let's see what's so special about it.
> 
> NOTE: If you find a solution that was not intended, then msg me on Discord @scrub
>
> future - md5: 30a6b3fe92a65271bac7c4b83b303b55

Besides the [binary](future), we are also given the [source code](future.c) for this challenge. So let's start with the source!

The program asks for the flag that must be 25 characters long.

```c
    char flag[26];
    printf("What's the flag: ");
    scanf("%25s", flag);
    flag[25] = 0;

    if (strlen(flag) != 25) {
        puts("Try harder.");
        return 0;
    }
```

Then, the flag we input is put into a 5x5 matrix.

```c
void genMatrix(char mat[5][5], char str[]) {
    for (int i = 0; i < 25; i++) {
        int m = (i * 2) % 25;
        int f = (i * 7) % 25;
        mat[m/5][m%5] = str[f];
    }
}
```

The generated matrix is given below:

```
   0        1        2        3        4
0  flag[0]  flag[16] flag[7]  flag[23] flag[14]
1  flag[5]  flag[21] flag[12] flag[3]  flag[19]
2  flag[10] flag[1]  flag[17] flag[8]  flag[24]
3  flag[15] flag[6]  flag[22] flag[13] flag[4]
4  flag[20] flag[11] flag[2]  flag[18] flag[9]
```

Finally, a `auth` string is generated based on the matrix and checked against the hardcoded `pass`.

```c
auth[0] = mat[0][0] + mat[4][4];
auth[1] = mat[2][1] + mat[0][2];
auth[2] = mat[4][2] + mat[4][1];
auth[3] = mat[1][3] + mat[3][1];
auth[4] = mat[3][4] + mat[1][2];
auth[5] = mat[1][0] + mat[2][3];
auth[6] = mat[2][4] + mat[2][0];
auth[7] = mat[3][3] + mat[3][2] + mat[0][3];
auth[8] = mat[0][4] + mat[4][0] + mat[0][1];
auth[9] = mat[3][3] + mat[2][0];
auth[10] = mat[4][0] + mat[1][2];
auth[11] = mat[0][4] + mat[4][1];
auth[12] = mat[0][3] + mat[0][2];
auth[13] = mat[3][0] + mat[2][0];
auth[14] = mat[1][4] + mat[1][2];
auth[15] = mat[4][3] + mat[2][3];
auth[16] = mat[2][2] + mat[0][2];
auth[17] = mat[1][1] + mat[4][1];
```

```c
char pass[19] = "\x8b\xce\xb0\x89\x7b\xb0\xb0\xee\xbf\x92\x65\x9d\x9a\x99\x99\x94\xad\xe4\x00";
```

Putting all these into a Z3 solver gives us the flag.

```python
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
```
