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
print("Trace File: " + file)
print("Cache Size: {} KB".format(cacheSize))
print("Block Size: {} Bytes".format(blockSize) )
print("Associativity: {}".format(associativity))
print("Replacement Policy: " + replacement)

powerOf2 = [2 ** x  for x in range(0,17)]
powerOfBytes = [2**10, 2**20, 2**30]
totBlocks = cacheSize / blockSize
power = powerOf2.index(totBlocks)
print('Total #Blocks: %d KB (2^ %d)' % (totBlocks, power))

tagBits = 0
print('Tag Size: %d bits' % (tagBits))

totIndices = cacheSize / (blockSize * associativity)
indexSize = powerOf2.index(totIndices) + 10
print('Index Size: %d bits, Total Indices: %d KB' % (indexSize, totIndices))

overheadSize = 0
print('Overhead Memory Size: %d bytes' % (overheadSize))

memorySize = 0
print('Implementation Memory Size: %d bytes' % (memorySize))
