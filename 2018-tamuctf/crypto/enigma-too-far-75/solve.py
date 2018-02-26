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

# PASSWORDISGIGEMXHISTGRYROCKSLEARNCRYPTOX