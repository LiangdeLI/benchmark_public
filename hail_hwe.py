import os
import timeit
import argparse
import glob

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

import hail as hl

hl.stop()
hl.init()

os.system('./start_loggers.sh /mydata/logs hail hwe {} {}'.format(args.core, args.run))
start_time = timeit.default_timer()

mt = hl.read_matrix_table(args.data + '.mt')

mt = hl.variant_qc(mt)
#mt = mt.filter_rows(mt.variant_qc.p_value_hwe > 1e-6)

time_taken = timeit.default_timer() - start_time
os.system('./kill_loggers.sh')

with open(args.output, 'a+') as log:
    log.write(str(time_taken))
    log.write(" ")
    log.flush()
    os.fsync(log)