import os
import timeit
import argparse
from shutil import rmtree

parser = argparse.ArgumentParser()
parser.add_argument('--task', type=str, default="allele_freq", 
    help='The task going to do benchmark. Default: (allele_freq)')
parser.add_argument('--data', type=str, 
    help='The path to the data for benchmark.')
# parser.add_argument('--output', type=str,
#   help='The file to write output to.')
args = parser.parse_args()

# print("task: ", args.task)
# print("core: ", args.core)
# print("data: ", args.data)

import sgkit as sg
from sgkit.io.vcf import vcf_to_zarr
import hail as hl

plink_task_flag_map = {'allele_freq':'freq', 'hwe':'hardy'}

for core in [16,8,4,2,1]:
    
    procset = '0' if (core == 1) else '0-{}'.format(core-1)

    sgkit_log = "output/sgkit_"+args.task+"_"+str(core)+".txt"
    
    if os.path.exists(sgkit_log):
        os.remove(sgkit_log)

    hail_log = "output/hail_"+args.task+"_"+str(core)+".txt"

    if os.path.exists(hail_log):
        os.remove(hail_log)

    plink_log = "output/plink_"+args.task+"_"+str(core)+".txt"

    if os.path.exists(plink_log):
        os.remove(plink_log)

    for i in range(3):
        
        call = 'taskset -c {} python3 sgkit_{}.py --data {} --output {} --core {} --run {}'.format(
            procset, args.task, args.data, sgkit_log, core, i)

        print(call, flush=True)

        os.system(call)

        call = 'taskset -c {} python3 hail_{}.py --data {} --output {} --core {} --run {}'.format(
            procset, args.task, args.data, hail_log, core, i)

        print(call, flush=True)

        os.system(call)

        call = 'taskset -c {} ./plink/plink --bfile {} --{} --out plink_{}'.format(procset, args.data, plink_task_flag_map[args.task], args.task)
        print(call, flush=True)
        os.system('./start_loggers.sh /mydata/logs plink {} {} {}'.format(args.task, core, i))
        start_time = timeit.default_timer()
        os.system(call)
        time_taken = timeit.default_timer() - start_time
        os.system('./kill_loggers.sh')

        with open(plink_log, 'a+') as log:
            log.write(str(time_taken))
            log.write(" ")
            log.flush()
            os.fsync(log)
        
        if args.task == 'allele_freq':
            os.remove("plink_allele_freq.frq")

        if args.task == 'hwe':
            os.remove("plink_hwe.hwe")

        os.remove("plink_{}.log".format(args.task))
        os.remove("plink_{}.nosex".format(args.task))

# core = 4

# sgkit_log = "output/sgkit_"+args.task+"_"+str(core)+".txt"

# if os.path.exists(sgkit_log):
#     os.remove(sgkit_log)

# hail_log = "output/hail_"+args.task+"_"+str(core)+".txt"

# if os.path.exists(hail_log):
#     os.remove(hail_log)

# plink_log = "output/plink_"+args.task+"_"+str(core)+".txt"

# if os.path.exists(plink_log):
#     os.remove(plink_log)

# for i in range(5):
    
#     call = 'python3 sgkit_{}.py --data {} --output {}'.format(
#         args.task, args.data, sgkit_log)

#     print(call)

#     os.system(call)

#     call = 'python3 hail_{}.py --data {} --output {}'.format(
#         args.task, args.data, hail_log)

#     print(call)

#     os.system(call)

#     call = './plink/plink --vcf data/1kg.vcf.bgz --freq --out plink_allele_freq'
#     start_time = timeit.default_timer()

#     os.system(call)

#     time_taken = timeit.default_timer() - start_time

#     with open(plink_log, 'a+') as log:
#         log.write(str(time_taken))
#         log.write(" ")

    
#     os.remove("plink_allele_freq.frq")
#     os.remove("plink_allele_freq.log")
#     os.remove("plink_allele_freq.nosex")