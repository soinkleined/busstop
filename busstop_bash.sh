#!/usr/bin/env bash
SLEEP=15
while true; do
    output=$(busstop -t 2>/dev/null) 
    if [ -n "${output}" ]; then
        clear && echo "${output}"
    fi
sleep "${SLEEP}"
output=''
done
