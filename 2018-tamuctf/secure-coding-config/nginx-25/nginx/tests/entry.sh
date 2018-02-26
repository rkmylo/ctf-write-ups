#!/bin/sh

cp default /etc/nginx/conf.d/default.conf
service nginx restart

python tests/queue.py
