#!/bin/sh

cp login.php /var/www/html/login.php
cp index.html /var/www/html/index.html
cp apache2.conf /etc/apache2/apache2.conf 

./db_gen.sh
service apache2 restart;
python tests/queue.py

