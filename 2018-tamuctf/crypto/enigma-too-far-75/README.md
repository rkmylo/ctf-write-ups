## Enigma Too Far? (Crypto, 75pt)

> Agent Bob is working at a law firm and loved history. He could not figure out how to crack the python enigma emulator, even though it was broken before. Since he could not crack the python enigma emulator, he decided that it would be ok to to encrypt all his emails with the emulator before sending them. NOT A GOOD IDEA!! Can you crack it?
> 
> You have intercepted two messages. The first is
> 1. "IPUXZGICZWASMJFGLFVIHCAYEGT". The second is "LTHCHHBUZODFLJOAFNNAEONXPLDJQVJCZPGAVOLN"
> 2. You have decrpted the first message and found that it is "HOWDYAGGIESTHEWEATHERISFINE"
> 3. Assume that "I II III" are rotors.
> 4. Plugboard is "AV BS CG DL FU HZ IN KM OW RX"
> 
> What is the flag? (The flag is in a slightly different format.)

Since we are given the rotor positions and the plugboard, we only need to bruteforce the ring settings for the enigma machine based on the provded ciphertext-plaintext combination.

We used the [`py-enigma`](https://py-enigma.readthedocs.io/en/latest/index.html) package for Python3.

```
import sys
from enigma.machine import EnigmaMachine

def brute_ring_settings(ciphertext):
    for a in range(1, 26):
        for b in range(1, 26):
            for c in range(1, 26):
                machine = EnigmaMachine.from_key_sheet(
                   rotors='I II III',
                   reflector='B',
                   ring_settings=[a, b, c],
                   plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')
                plaintext = machine.process_text(ciphertext)
                if plaintext.startswith('HOWDY'):
                    print('[+] Ring settings: {}, {}, {}'.format(a, b, c))
                    return a, b, c
    return -1, -1, -1

a, b, c = brute_ring_settings('IPUXZGICZWASMJFGLFVIHCAYEGT')

if a < 0 or b < 0 or c < 0:
    print('[-] Failed')
    sys.exit(0)

machine = EnigmaMachine.from_key_sheet(
   rotors='I II III',
   reflector='B',
   ring_settings=[a, b, c],
   plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')
plaintext = machine.process_text('LTHCHHBUZODFLJOAFNNAEONXPLDJQVJCZPGAVOLN')
print('[+] Flag: ' + plaintext)
```

```
[+] Ring settings: 19, 2, 14
[+] Flag: PASSWORDISGIGEMXHISTGRYROCKSLEARNCRYPTOX
```
