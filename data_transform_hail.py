import glob
import hail as hl
import timeit

print("convert data to hail default version", flush=True)
hl.stop()
hl.init(tmp_dir="/mydata/tmp", local_tmpdir="/mydata/tmp")
start_time = timeit.default_timer()
hl.import_vcf("/mydata/1kg.vcf.bgz").write('/mydata/1kg.mt', stage_locally=False, overwrite=True)
time_taken = timeit.default_timer() - start_time
print("take: "+str(time_taken)+" seconds", flush=True)