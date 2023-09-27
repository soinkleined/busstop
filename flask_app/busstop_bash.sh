#!/usr/bin/env bash
SLEEP=15
while true; do
    output=$(python tfl_bus_monitor/tfl_bus_monitor.py -t 2>/dev/null) 
    if [ -n "${output}" ]; then
        clear && echo "${output}"
    fi
sleep "${SLEEP}"
output=''
done
