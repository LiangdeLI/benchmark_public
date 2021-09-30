import glob
import sgkit as sg
from sgkit.io.vcf import vcf_to_zarr
import timeit
import _thread
import time

done = False

def print_time(delay=10):
    global done
    count = 0
    while not done:
        time.sleep(delay)
        count += delay
        print(count, " seconds passed", flush=True)

_thread.start_new_thread(print_time, (10,))

print("converting data to sgkit default version", flush=True)
start_time = timeit.default_timer()
vcf_to_zarr("/mydata/1kg.vcf.bgz", "/mydata/1kg.zarr", tempdir="/mydata/tmp")

time_taken = timeit.default_timer() - start_time
done = True
print("take: "+str(time_taken)+" seconds", flush=True)



# print("convert data to plink default version")
# start_time = timeit.default_timer()
# call = "./plink/plink --vcf /mydata/1kg.vcf.bgz --out /mydata/1kg"
# os.system(call)
# time_taken = timeit.default_timer() - start_time
# print("take: "+str(time_taken)+" seconds")