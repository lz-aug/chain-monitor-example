#!/bin/bash
set -ex
export PYTHONUNBUFFERED=x
if [ "${1:0:1}" = '-' ] || [ "${1:0:1}" = '' ]; then
        exec python3 ./src/main.py
fi

exec $@

