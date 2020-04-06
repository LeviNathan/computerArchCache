#!/usr/bin/python3

import sys
import os
import math

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

policyDict = {'RR': 'Round Robin', 'RND': 'Random', 'LRU': 'Least Recently Used'}

policy = 'RR'
if '-r' in sys.argv:
    policy = sys.argv[sys.argv.index('-r') + 1]
    if policy not in policyDict:
        sys.exit("Error: Invalid replacement policy. (RR, RND, or LRU)")
    else:
        policy = policyDict[sys.argv[sys.argv.index('-r') + 1]]

print("Cache Simulator - CS 3853 - Team 12\n")
print('Trace File: %s\n' % (file))
print("***** Cache Input Parameters ***** \n")
print('Cache Size: \t\t\t{} KB'.format(cacheSize))
print('Block Size: \t\t\t{} bytes'.format(blockSize))
print('Associativity: \t\t\t{}'.format(associativity))
print('Replacement Policy: \t\t{}\n'.format(policy))

powerOf2 = [2 ** x  for x in range(0,28)]

offset = blockSize
totIndices = cacheSize * 2**10 / (blockSize * associativity)
indexSize = powerOf2.index(totIndices)
totBlocks = totIndices * associativity
tagBits = 32 - indexSize - powerOf2.index(blockSize)

overheadSize = ((tagBits + 1) * totBlocks)/8
memorySize = cacheSize * 2**10 + overheadSize
totRows = totBlocks/associativity
cost = 0
print("***** Cache Calculated Values *****\n")

print('Total #Blocks: \t\t\t{}'.format(int(totBlocks)))
print('Tag Size: \t\t\t{} bits'.format(tagBits))
print('Index Size: \t\t\t{} bits'.format(indexSize))
print('Total # Rows: \t\t\t{}'.format(int(totRows)))
print('Overhead Memory Size: \t\t{} bytes'.format(int(overheadSize)))
print('Implementation Memory Size: \t{:.2f} KB ({} bytes)'.format(float(memorySize/2**10), int(memorySize)))
print('Cost: \t\t\t\t${:.2f}\n'.format(cost))

"""
#print first 20 addresses and the length
with open(file) as f:
    num_of_address = 0
    for line in f:
        if(line[:3] == "EIP" and num_of_address < 20):
            #Bytes to decimal
            length = str(int(math.pow(2,int(line[5:7])*8)))
            hex_address = line[10:18] 
            num_of_address += 1
            print("0x{}: ({})".format(hex_address, length))
"""