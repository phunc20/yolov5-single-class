import time
import os
import asyncio
import re

t0 = time.time()

dir_from = "coco/labels/train2017"
L_filenames = os.listdir(dir_from)
dir_to = os.path.join("koko", os.path.basename(dir_from.rstrip('/')))
print("dir_to = {}".format(dir_to))
os.makedirs(dir_to, exist_ok=True)
preserve = 0  # The ID of the single class that we want to preserve

def rw_aux(filename):
    with open(os.path.join(dir_from, filename), 'r') as from_:
        from_lines = from_.readlines()
    to_lines = []
    for line in from_lines:
        obj_id = int(line.split(' ')[0])
        if obj_id == preserve:
            # I proposed 2 solutions of replacement here.
            # Sol.01
            #to_lines.append(re.sub("^{} ".format(obj_id), "0 ", line))
            # Sol.02
            to_lines.append(line.replace("{}".format(obj_id), '0', 1))
    #else:
    #    #print("{} contains no preserve={} class.".format(filename, preserve))
    #    #pass
    #    #return 1
    with open(os.path.join(dir_to, filename), 'w') as to_:
        to_.writelines(to_lines)

loop = asyncio.get_event_loop()

async def read_N_write(filename):
    print("{} START at {:.4f}".format(filename, time.time() - t0))
    #await loop.run_in_executor(None, requests.get, url)
    await loop.run_in_executor(None, rw_aux, filename)
    print("{} FINISH at {:.4f}".format(filename, time.time() - t0))

tasks = []

for filename in L_filenames:
    task = loop.create_task(rw_aux(filename))
    tasks.append(task)

#url = "https://www.google.com.tw/"
#
#
#async def tx_rx(url):
#    print(f"Tx at {time.time() - t0:.4f}")
#    await loop.run_in_executor(None, requests.get, url)
#    print(f"Rx at {time.time() - t0:.4f}")
#
#
#for _ in range(10):
#    task = loop.create_task(tx_rx(url))
#    tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))
