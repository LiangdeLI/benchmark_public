#!/usr/bin/env bash

while true;
do
    cpu="$[100-$(vmstat 1 2|tail -1|awk '{print $15}')]"
    echo $cpu >> $1;
    sleep 1;
done