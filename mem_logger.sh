#!/usr/bin/env bash

while true;
do
    mem=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
    echo $mem >> $1;
    sleep 1;
done