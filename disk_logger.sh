#!/usr/bin/env bash

while true;
do
    disk_log=$(iostat -dm 1 1 | sed '1,2d')
    echo $disk_log >> $1;
    sleep 1;
done