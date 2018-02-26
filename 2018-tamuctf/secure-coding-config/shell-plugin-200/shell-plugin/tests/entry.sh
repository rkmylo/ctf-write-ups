#!/bin/bash

python script_server.py &
pushd ctfd/
    python serve.py & 
popd
sleep 5s
service ssh start
python tests/queue.py $(cat /proc/self/cgroup | grep docker | grep -o -E '[0-9a-f]{64}' | head -n 1)
