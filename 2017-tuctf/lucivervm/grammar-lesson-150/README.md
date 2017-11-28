## Grammar Lesson (LuciferVM, 150pt)

> I do declare this to challenge to be at least mildly engaging, and certainly useful going forwards

During the CTF, teams were provided with a VM (`LuciferVMTUCTF.ova`) containing several challenges and a special category had been added for those, namely the `LuciferVM` category. `Grammar Lesson` was one of those challenges.

The files for this challenge were located inside the `~hackerman/Games/keygen/` directory.

```
❯❯❯ ls -l
total 24
-rwxr-xr-x  1 hackerman  hackerman    46 Nov 21 01:44 Connect To Key Validator
-rw-r--r--  1 hackerman  hackerman   336 Nov 21 01:43 NoteToSelf
-rw-r--r--  1 hackerman  hackerman  1169 Nov 21 01:46 validation_requirements.txt
```

First of, we are given a description of what we are about to face:

```
❯❯❯ cat NoteToSelf
Greetings, Hackerman - It is I, Hackerman.

In my endeavours to hack into Dungeon of Infinity,
I stumbled upon what is rumored to be a serial key
validator for an as-yet unreleased game. I was also
able to obtain a copy of the validation criteria,
though I have yet to write a valid key generator
for the key validator.

Hackerman, out
```

We are also given a socket to connent to:

```
❯❯❯ cat "Connect To Key Validator"
#!/bin/bash
ncat grammarlesson.tuctf.com 6661
```

Finally, we have the serial key validator source code inside the `validation_requirements.txt` file:

```prolog
% tokenizer("key_string_here",T), checkkey(T,Z).
token(48,0).
token(49,1).
token(50,2).
token(51,3).
token(52,4).
token(53,5).
token(54,6).
token(55,7).
token(56,8).
token(57,9).

token(40,lt_paren).
token(41,rt_paren).
token(44,comma).
token(45,hyphen).
token(38,amper).

tokenizer([],[]).
tokenizer([H|T],[TK|TL]):-token(H,TK), tokenizer(T,TL).

rt_paren([rt_paren|S],S).
lt_paren([lt_paren|S],S).
comma([comma|S],S).
hyphen([hyphen|S],S).
amper([amper|S],S).

digit([0|S],S).
digit([1|S],S).
digit([2|S],S).
digit([3|S],S).
digit([4|S],S).
digit([5|S],S).
digit([6|S],S).
digit([7|S],S).
digit([8|S],S).
digit([9|S],S).

checkkey(S,R) :- lt_paren(S,S1), key(S1,S2,V1), rt_paren(S2,R), V1 is 82944.
key(S,R,V) :- oct(S,S1,V1), amper(S1,S2), oct(S2,R,V2), V is V1 * V2.
oct(S,R,V) :- quad(S,S1,V1), hyphen(S1,S2), quad(S2,R,V2), V is V1 + V2.
quad(S,R,V) :- pair(S,S1,V1), comma(S1,S2), pair(S2,R,V2), V is V1* V2.
pair(S,R,V) :- digit(S,S1,V1), digit(S1,R,V2), V is V1 + V2.

digit([0|S],S, 0).
digit([1|S],S, 1).
digit([2|S],S, 2).
digit([3|S],S, 3).
digit([4|S],S, 4).
digit([5|S],S, 5).
digit([6|S],S, 6).
digit([7|S],S, 7).
digit([8|S],S, 8).
digit([9|S],S, 9).
```

The code is written in **Prolog** and it begins with a comment describing how the main functionality is invoked:

```
% tokenizer("key_string_here",T), checkkey(T,Z).
```

The input key is "tokenized" and passed through the `checkkey` rule which must return `True` for valid keys. Even though the code looks a bit complicated at first, it really isn't. Also, keep in mind that the challenge only worths 150 pts. Below, we see the actual validation rules we have to obey:

```prolog
checkkey(S,R) :- lt_paren(S,S1), key(S1,S2,V1), rt_paren(S2,R), V1 is 82944.
key(S,R,V) :- oct(S,S1,V1), amper(S1,S2), oct(S2,R,V2), V is V1 * V2.
oct(S,R,V) :- quad(S,S1,V1), hyphen(S1,S2), quad(S2,R,V2), V is V1 + V2.
quad(S,R,V) :- pair(S,S1,V1), comma(S1,S2), pair(S2,R,V2), V is V1* V2.
pair(S,R,V) :- digit(S,S1,V1), digit(S1,R,V2), V is V1 + V2.
```

Reading the rules (`:-`) bottom up, they boil down to the following:

* `pair` if we have the combination of any two digits. e.g. `93`
* `quad` if we have two `pair`s combined with `comma`. e.g. `93,75`
* `oct` if we have two `quad`s combined with `hyphen`. e.g. `93,75-46,34`
* `key` if we have two `oct`s combined with an `amper`. e.g. `93,75-46,34&23,42-92,48`
* `checkkey` if we have a `key` enclosed in `lt_paren` and `rt_paren`. e.g. `(93,75-46,34&23,42-92,48)`

And we have the key format:

```
(P,P-P,P&P,P-P,P)
```

What we didn't interpret was the last fact from each of the above rules. Starting with the sum of **every** pair (`P`) with digits `a`, `b`, valid keys must satisfy the following conditions:

```
a + b == c
c * c == d
d + d == e
e * e == 82944
```

Only thing left to create our keygen is to find all valid pairs and generate keys according to the required format. The following script will generate all valid keys.

```python
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
```

The valid pairs are:

```
48, 39, 93, 84, 75, 66, 57
```

The script generated **5764801** valid keys. Sending a few of those to the server wins the flag.

```
# TUCTF{Gr4mm3r_1s_v3ry_imp0rtAnT!_4ls0_Pr0log_iz_c00l!}
```
