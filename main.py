#!/usr/bin/python3

import sys
import os
import math
from random import randint

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
if cacheSize < 1 or cacheSize > 8192:
    sys.exit("Error: Cache out of range. 1KB to 8192KB(8MB)")


blockSize = sys.argv[sys.argv.index('-b') + 1]
try:
    blockSize = int(blockSize)
except ValueError:
    sys.exit("Error: Invalid block size, make sure it is an integer.")
if blockSize < 2 or blockSize > 64:
    sys.exit("Error: Block size out of range. 4 to 64 bytes")


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
print('Trace File: {}'.format(file))
print("\n***** Cache Input Parameters ***** \n")
print('Cache Size: \t\t\t{} KB'.format(cacheSize))
print('Block Size: \t\t\t{} bytes'.format(blockSize))
print('Associativity: \t\t\t{}'.format(associativity))
print('Replacement Policy: \t\t{}'.format(policy))

powerOf2 = [2 ** x  for x in range(0,28)]

offset = blockSize
totIndices = cacheSize * 2**10 / (blockSize * associativity)
indexSize = powerOf2.index(totIndices)
totBlocks = totIndices * associativity
tagBits = 32 - indexSize - powerOf2.index(blockSize)

overheadSize = ((tagBits + 1) * totBlocks)/8
memorySize = cacheSize * 2**10 + overheadSize
totRows = totBlocks/associativity
cost = (cacheSize + overheadSize/2**10) * 0.05

print("\n***** Cache Calculated Values *****\n")

print('Total # Blocks: \t\t{}'.format(int(totBlocks)))
print('Tag Size: \t\t\t{} bits'.format(tagBits))
print('Index Size: \t\t\t{} bits'.format(indexSize))
print('Total # Rows: \t\t\t{}'.format(int(totRows)))
print('Overhead Memory Size: \t\t{} bytes'.format(int(overheadSize)))
print('Implementation Memory Size: \t{:.2f} KB ({} bytes)'.format(float(memorySize/2**10), int(memorySize)))
print('Cost: \t\t\t\t${:.2f}'.format(cost))

#print first 20 addresses and the length
cacheDict = {}
cacheAccesses = 0
cacheHits = 0
compulsoryMiss = 0
conflictMiss = 0
cycleCount = 0
instructionCount = 0

with open(file) as f:
    for line in f:
        if line[0:4] == "dstM":
            if(line[6:14] != '00000000'):
                cycleCount += 1;
                cycleCount += (3*4)
                # dstM is not empty +1 for cycle count 
            if(line[33:41] != '00000000'):
                cycleCount += 1;
                cycleCount += (3*4)
                # srcM is not empty +1 for cycle count
        if(line[:3] == "EIP" and line[10:18] != '00000000'):
            instructionCount +=1
            cycleCount += 2
            # add 2 to cycle count for the instruction and 1 to the instruction count

            #Bytes to decimal
            length = str(int(math.pow(2,int(line[5:7])*8)-1))
            hex_address = line[10:18]

            # Keep track of the index so that when it does change, new access
            master_index = None
            hex_address_binary = bin(int(hex_address, 16))[2:].zfill(len(hex_address)*4)
            reads = int(line[5:7])
            offsetSize = len(hex_address_binary) - tagBits - indexSize
            for i in range(0,reads):
                tag = hex_address_binary[:tagBits].zfill(4-(tagBits%4)+tagBits)
                index = hex_address_binary[tagBits:tagBits+indexSize].zfill(4 -(indexSize%4)+indexSize)
                offset = hex_address_binary[tagBits+indexSize:].zfill(4-(offsetSize%4)+offsetSize)
                
                # Check to see if it is a new cache access.
                if master_index != index:
                    cacheAccesses += 1
                    # Checks to see if index has been accessed.
                    if index not in cacheDict:
                        cacheDict[index] = [tag]
                        compulsoryMiss += 1
                        cycleCount += (3 * (reads - i))
                    else:
                        
                        # Checks to see if the tag is in the cache row.
                        if tag not in cacheDict[index]:
                            # Checks to see if the cache row is full.
                            if len(cacheDict[index]) < associativity:
                                # If LRU, sends index to the back of the array
                                if policy == 'LRU':
                                    cacheDict[index].pop(0)
                                    cacheDict[index].append(tag)
                                compulsoryMiss += 1
                                cycleCount += (3 * (reads - i))
                            else:
                                # If RND, randomly selects element from row and pops it out.
                                if policy == 'RND':
                                    cacheDict[index].pop(randint(0,len(cacheDict[index] - 1)))
                                else:
                                    cacheDict[index].pop(0)
                                    
                                conflictMiss += 1
                                cycleCount += (3 * (reads - i))
                            cacheDict[index].append(tag)
                        else:
                            cacheHits += 1
                            cycleCount += 1
                master_index = index
                hex_address_binary = bin(int(hex_address_binary, 2) + 1)[2:].zfill(len(hex_address)*4)
print("\n\n***** Cache Calculated Values *****\n")

print("Total Cache Accesses:\t{}".format(cacheAccesses))
print("Cache Hits: \t{}".format(cacheHits))
print("Cache Misses: \t\t{}".format(compulsoryMiss + conflictMiss))
print("--- Compulsory Misses:\t{}".format(compulsoryMiss))
print("--- Conflict Misses:\t{}".format(conflictMiss))


hitRate = cacheHits / cacheAccesses
missRate =  1 - hitRate
cpi = cycleCount/instructionCount
# Convert blocksize to bits, recalulate overhead so that it is in bits, then convert to bytes
overheadAndBlockSize = ((blockSize * 8) + (tagBits + 1)) / 8
unusedKB = ((totBlocks - compulsoryMiss) * (overheadAndBlockSize)) / 1024
unusedCacheSpace = unusedKB / (memorySize/2**10)
waste = cost * unusedCacheSpace
print("\n\n***** *****  CACHE MISS RATE:  ***** *****\n")

print("Hit Rate:\t\t{:.4f}%".format(hitRate * 100))
print("Miss Rate:\t\t{:.4f}".format(missRate * 100))
print("CPI:\t\t\t{:.2f} Cycles/Instruction".format(cpi))
print("Unused Cache Space: {:.2f} KB / {} KB = {:.2f} %  Waste: ${:.2f}".format(unusedKB, memorySize/2**10, unusedCacheSpace * 100, waste))
print("Unused Cache Blocks:	{} / {}".format(int(totBlocks - compulsoryMiss), int(totBlocks)))