#OSINT2

##Description

Annual audits have flagged an employee who is sharing data outside the company in some secret manner. A quick OSINT revealed his personal email id, i.e. zakripper@mail.com.

Can you find the secret?

##Solution

By querying flickr for the specific email we get an account with a single photo in it: https://www.flickr.com/photos/162289309@N03

By downloading the photo and inspecting strings we get the flag

Flag: hackim18{'7h1515453cr3tm35543'}
