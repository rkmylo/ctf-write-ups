#OSINT1

##Description

One of our systems has been infected by a ransomware.The message says My username is your password. Wait for further instructions.

We have been able to identify the JS file used to download the ransomware.

Here is the MD5: '151af957b92d1a210537be7b1061dca6'.
Can you help us to unlock the machine?

##Solution

We can find the relevant malware by looking up the hash at virustotal:

This results in the file 	DSAdaDSDA.js.

By looking up the file at https://www.hybrid-analysis.com/sample/50d6111ced473456a1c9e111c18bdb60f2f9f607800fd795c627751e79aacc9b?environmentId=100 we can see that it connects to a CnC with the username n923wUc.

Flag: hackim18{'n923wUc'}
