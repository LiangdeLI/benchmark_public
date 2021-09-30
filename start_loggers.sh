#!/usr/bin/env bash
LOG_DIR=${1:-"/mydata/logs"}
mkdir -p $LOG_DIR
TOOL=$2
TASK=$3
CORE=$4
RUN=$5
DISK_LOG_FILE=${LOG_DIR}/disk_${TOOL}_${TASK}_${CORE}_r${RUN}.log
CPU_LOG_FILE=${LOG_DIR}/cpu_${TOOL}_${TASK}_${CORE}_r${RUN}.log
MEM_LOG_FILE=${LOG_DIR}/mem_${TOOL}_${TASK}_${CORE}_r${RUN}.log

nohup bash mem_logger.sh $MEM_LOG_FILE &
nohup bash disk_logger.sh $DISK_LOG_FILE &
nohup bash cpu_logger.sh $CPU_LOG_FILE &