import os
import timeit
import argparse
import glob
from shutil import rmtree

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, 
    help='The path to the data for benchmark.')
parser.add_argument('--output', type=str,
    help='The file to write output to.')
parser.add_argument('--core', type=int,
    help='The number of cores using.')
parser.add_argument('--run', type=int,
    help='The count of runing.')
args = parser.parse_args()

import sgkit as sg
from sgkit.io.vcf import vcf_to_zarr

os.system('./start_loggers.sh /mydata/logs sgkit allele_freq {} {}'.format(args.core, args.run))
start_time = timeit.default_timer()

ds = sg.load_dataset(args.data + ".zarr")
allele_freq_sgkit = sg.variant_stats(ds)['variant_allele_frequency'].values

time_taken = timeit.default_timer() - start_time
os.system('./kill_loggers.sh')

with open(args.output, 'a+') as log:
    log.write(str(time_taken))
    log.write(" ")
    log.flush()
    os.fsync(log)

rmtree("temp.zarr")