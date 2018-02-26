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

# GigEm{NibblerEatsNibbles}