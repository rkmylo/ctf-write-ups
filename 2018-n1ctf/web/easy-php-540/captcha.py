import hashlib
from itertools import product

c = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_ []{}<>~`+=,.;:/?|'
captchas = [''.join(i) for i in product(c, repeat=3)]

print '[+] Genering {} captchas...'.format(len(captchas))
with open('captchas.txt', 'w') as f:
    for k in captchas:
        f.write(hashlib.md5(k).hexdigest()+' --> '+k+'\n')
