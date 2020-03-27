#!/usr/bin/python3

import sys
import os

"""
Your simulator will have the following input parameters: 
1. –f <trace file name> [ name of text file with the trace ] 
2. –s <cache size in KB> [ 1 KB to 8 MB ] 
3. –b <block size>  [ 4 bytes to 64 bytes ] 
4. –a <associativity>   [ 1, 2, 4, 8, 16 ] 
5. –r <replacement policy> [ RR or RND or LRU for bonus points] 

Sample command lines: 
    Sim.exe –f trace1.txt –s 1024 –b 16 –a 2 –r RR 
That would read the trace file named “trace1.txt”, 
configure a total cache size of 1 MB with a block size of 16 bytes/block. 
It would be 2-way set associative and use a replacement policy of Round Robin. 
We will assume a write-through policy.  Cost: $0.05 / KB 
"""

if len(sys.argv) != 11 and len(sys.argv) != 9:
    sys.exit("Error: Invalid number of arguments")

file = sys.argv[sys.argv.index('-f') + 1]
if not os.path.exists(file):
    sys.exit("Error: File does not exist.")

cacheSize = sys.argv[sys.argv.index('-s') + 1]
try:
    cacheSize = int(cacheSize)
except ValueError:
    sys.exit("Error: Invalid cache size, make sure it is an integer.")
if cacheSize < 2*10 and cacheSize > 2**23:
    sys.exit("Error: Cache out of range. 1KB(1024) to 8MB(8388608)")


blockSize = sys.argv[sys.argv.index('-b') + 1]
try:
    blockSize = int(blockSize)
except ValueError:
    sys.exit("Error: Invalid block size, make sure it is an integer.")
if blockSize < 4 and blockSize > 64:
    sys.exit("Error: Block size out of range. 4 to 16 bytes")


associativity = sys.argv[sys.argv.index('-a') + 1]
try:
    associativity = int(associativity)
except ValueError:
    sys.exit("Error: Invalid associativity, make sure it is an integer.")
if not associativity in [2**x for x in range(0,5)]:
    sys.exit("Error: Invalid Associativity")

policy = 'RR'
if '-r' in sys.argv:
    policy = sys.argv[sys.argv.index('-r') + 1]
    if policy not in ['RR', 'RND', 'LRU']:
        sys.exit("Error: Invalid replacement policy. (RR, RND, or LRU)")

print("Cache Simulator CS 3853 Spring 2020 - Group #12\n")
print(" ".join(sys.argv))
print(sys.argv)
print('Trace File: %s' % (file))
print('Cache Size: %d' % (cacheSize))
print('Block Size: %d' % (blockSize))
print('Associativity: %d-way' % (associativity))
print('R-Policy: %s' % (policy))
print('------------------------------------------')

print("Cache Size: {} KB".format(cacheSize))
print("Block Size: {} Bytes".format(blockSize) )
print("Associativity: {}".format(associativity))
print("Replacement Policy: " + policy)
print('------------------------------------------')

powerOf2 = [2 ** x  for x in range(0,28)]

offset = blockSize
totIndices = cacheSize * 2**10 / (blockSize * associativity)
indexSize = powerOf2.index(totIndices)
totBlocks = totIndices * associativity
tagBits = 32 - indexSize - powerOf2.index(blockSize)

overheadSize = ((tagBits + 1) * totBlocks)/8
memorySize = cacheSize * 2**10 + overheadSize

print('Tag Size: %d bits' % (tagBits))
print('Total #Blocks: %d KB (2^ %d)' % (totBlocks/2**10, powerOf2.index(totBlocks)))
print('Index Size: %d bits, Total Indices: %d KB' % (indexSize, totIndices/2**10))
print('Overhead Memory Size: %d bytes' % (overheadSize))
print('Implementation Memory Size: %d bytes' % (memorySize))
print('------------------------------------------')


print("Cache Hit Rate: {} %".format('nn.n'))
print("CPI: {}".format('nn.nn'))
print("Cost: ${}".format('nnnn.nn'))
print("Ununsed Cache Space: {} KB / {} %\n".format('nn', 'nn.n'))


with open(file, "r") as fp:
    lines = fp.readlines()
    lines = lines[0::3]
    
    for i in range(0,20):
        print("0x%x: (%d)" % (lines[i][10:18], lines[i][5:7]))
    #for line in lines:
    #    lines[lines.index(line)] = line[:17]

