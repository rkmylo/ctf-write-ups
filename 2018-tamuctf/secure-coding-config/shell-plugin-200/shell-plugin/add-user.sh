#!/bin/bash

mkdir /home/$1
useradd -G ctf-users --home /home/$1 -s /bin/bash $1

chown $1:$1 /home/$1

echo -e "$2\n$2" | passwd $1

