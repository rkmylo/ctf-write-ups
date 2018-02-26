#!/bin/bash
USER=${1// /}
PASS=${2// /}
echo -e "$PASS\n$PASS" | passwd "$USER"
