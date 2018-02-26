#!/bin/sh

touch logs.txt
echo "Starting Server"
node server/server.js > logs.txt 2>&1 &
sleep 5s
echo "Pushing message"
python tests/queue.py
