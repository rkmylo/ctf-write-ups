## XORbytes (Crypto, 100pt)

> Looks like there is a flag here...if only you could run the binary.
> 
> [hexxy](hexxy)

```
❯❯❯ file hexxy
hexxy: data
```

Running `strings` on the binary (combined with the challenge title), we quickly realized that this is an ELF binary XOR'd with a key (which seems quite small if you take into account the repeating patterns in the binary and the null bytes that are common to exist in ELF binaries). Since the first few bytes of ELF binaries are always the same, we can use this information to recover the key.

```
❯❯❯ hexdump -C hexxy | head -n1
00000000  2e 07 7d 21 31 6d 35 42  35 75 7a 50 6a 6a 44 34  |..}!1m5B5uzPjjD4|

❯❯❯ hexdump -C another_binary | head -n1
00000000  7f 45 4c 46 01 01 01 00  00 00 00 00 00 00 00 00  |.ELF............|
```

We can write our solver which will XOR the first 16 bytes of the encrypted file with the first 16 bytes of another ELF binary to recover the key and then use it  to decrypt `hexxy`. It is an assumption for our solver that the key is 16 bytes long.

```
import os

x = [0x2e, 0x07, 0x7d, 0x21, 0x31, 0x6d, 0x35, 0x42, 0x35, 0x75, 0x7a, 0x50, 0x6a, 0x6a, 0x44, 0x34]
y = [0x7f, 0x45, 0x4c, 0x46, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
key = ''.join(map(lambda x: chr(x[0]^x[1]), zip(x, y)))
#print key

hexxy = ''
with open('hexxy', 'rb') as f:
    hexxy = f.read()

hexxy_decrypted = ''
for i in range(0, len(hexxy), len(key)):
    for j in range(len(key)):
        if i+i >= len(hexxy):
            break
        hexxy_decrypted += chr(ord(hexxy[i+j])^ord(key[j]))

with open('hexxy_decrypted', 'wb') as f:
    f.write(hexxy_decrypted)

print os.system('strings hexxy_decrypted | grep -i gigem')
```

The decrypted file ([hexxy_decrypted](hexxy_decrypted)) was not functional after decryption as was the flag, and it seems that there might be more than one keys used. However, after we fixed a single letter in the flag, it was accepted by the system ¯\_(ツ)_/¯

```
GigEm{NibblerEatsNibbles}
```
