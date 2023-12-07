#!/usr/bin/env bash
SLEEP=15
if busstop -h >/dev/null 2>&1; then
    :
else
    echo "'busstop' is not installed.  Please install using 'pip install tfl_bus_monitor'." && exit 1
fi

while true; do
    output=$(busstop -t 2>/dev/null) 
    if [ -n "${output}" ]; then
        clear && echo "${output}"
    fi
sleep "${SLEEP}"
output=''
done
