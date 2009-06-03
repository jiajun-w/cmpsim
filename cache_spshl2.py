#!/usr/bin/python

#o---------------------------------------------------------------------------o
# Cache simulator 
# Author: Shatrugna Sadhu
# Email: ssadhu at cs dot ucsb dot edu
# Description: + A CMP Cache model with two levels of caching
#	         Each core has its own independent L1
#	       + There are 4 cores with 4 L1 caches each
#	       + Core 0 & 1 share L2 caches 0 
#	       + Core 2 & 3 share L2 caches 1
# Acknowledgement : Sushmit Biswas
#o---------------------------------------------------------------------------o


import os
import sys
import signal 
import string
import math

import random
import re

L1=[]
L2=[]
file_ext=0
i=0

#L1_cache_size=0TProof
#L1_cache_way=0
#L2_cache_size=0
#L2_cache_way=0

#o---------------------------------------------------------------------------o
class g1(object):
# Global constants
	def __init__(self, cac=None):
		self.cache = cac  # Instance of cache class
		self.hits=0
		self.misses=0

#o---------------------------------------------------------------------------o


#o---------------------------------------------------------------------------o
class g2(object):
# Global constants
	def __init__(self, cac=None):
		self.cache = cac  # Instance of cache class
		self.hits=0
		self.misses=0

#o---------------------------------------------------------------------------o

	
class Cache_l1:
	def __init__(self):
		self.lruValue    = {}
		self.clearCache()

   # Zero out cache blocks/flags/values
	def clearCache(self):
		for n in range(num_sets_l1):
			self.lruValue[n]={}
	
	def checkCacheHit(self, address):
		add=address
		index=(add >> log2)%(num_sets_l1)	

		if self.lruValue[index].has_key(address):
			return 1;
		else:
			return -1; #BS

	def incrementLRU(self, address):
		add=address
		index=(add >> log2)%(num_sets_l1)

		old_lru_val = self.lruValue[index][address]
	
		if old_lru_val == 0: # if this is the last accessed line, don't alter anything
			return 0;
			
# increment for all other in the set that has LRU counter < current block, then
# reset for current block
		for key, value in self.lruValue[index].iteritems():
			if value <= old_lru_val:
				self.lruValue[index][key]+=1;
				
		self.lruValue[index][address]=0;
		return 0;

	def storeLRUBlock(self, address):
		add=address
		index=(add >> log2)%(num_sets_l1)


		max_value = -1;
		max_value_key = -1;
			
		for key, value in self.lruValue[index].iteritems():
			if len(self.lruValue[index]) == L1_cache_way :
				if value > max_value:
					max_value_key = key;
					max_value = value;
			self.lruValue[index][key]+=1;
				
		if len(self.lruValue[index]) == L1_cache_way :
			del self.lruValue[index][max_value_key];
		
		self.lruValue[index][address]=0;
		return 0;

	def invalidate(self, address):
		add=address
		index=(add >> log2)%(num_sets_l1)

		if self.lruValue[index].has_key(address):
			del self.lruValue[index][address];		

		return 0;

class Cache_l2:
	def __init__(self):
		self.lruValue    = {}
		self.clearCache()

   # Zero out cache blocks/flags/values
	def clearCache(self):
		for n in range(num_sets_l2):
			self.lruValue[n]={}
	
	def checkCacheHit(self, address):
		add=address
		index=(add >> log2)%(num_sets_l2)

		if self.lruValue[index].has_key(address):
			return 1;
		else:
			return -1; #Heres the place where I should be adding L2

	def incrementLRU(self, address):
		add=address
		index=(add >> log2)%(num_sets_l2)

		old_lru_val = self.lruValue[index][address]
	
		if old_lru_val == 0: # if this is the last accessed line, don't alter anything
			return 0;
			
# increment for all other in the set that has LRU counter < current block, then
# reset for current block
		for key, value in self.lruValue[index].iteritems():
			if value <= old_lru_val:
				self.lruValue[index][key]+=1;
				
		self.lruValue[index][address]=0;
		return 0;

	def storeLRUBlock(self, address):
		add=address
		index=(add >> log2)%(num_sets_l2)

		max_value = -1;
		max_value_key = -1;
			
		for key, value in self.lruValue[index].iteritems():
			if len(self.lruValue[index]) == L2_cache_way :
				if value > max_value:
					max_value_key = key;
					max_value = value;
			self.lruValue[index][key]+=1;
				
		if len(self.lruValue[index]) == L2_cache_way :
			del self.lruValue[index][max_value_key];
		
		self.lruValue[index][address]=0;
		return 0;


# -----------------------------------------------------------------------------
def printSummary():
	"""
	Print results of program execution. This is called at the
	end of the program run to provide a summary of what
	settings were used and the resulting time. In addition,
	the command line number codes are converted to text for
	readability.
	"""
	temp_h = 0
	temp_m =0
	i = 0


	for i in range(0,4):
		temp_h=L1[i].hits+temp_h

	i = 0
	for i in range(0,4):
		temp_m=L1[i].misses+temp_m

	print ""
	print "o--------------------------o"
	print "|               Cache: L1"
	print "|          Cache size:", repr(L1_cache_size)
	print "| Cache associativity:", repr(L1_cache_way)
	print "|                Hits:", repr(temp_h)
	print "|              Misses:", repr(temp_m)
	print "|            Hit Rate: %3.2f" % (temp_h * 100.0/ (temp_h + temp_m))
	print "o--------------------------o"

	temp_h = 0
	temp_m =0
	i = 0

	for i in range(0,2):
		temp_h=L2[i].hits+temp_h

	i = 0
	for i in range(0,2):
		temp_m=L2[i].misses+temp_m


	print ""
	print "o--------------------------o"
	print "|               Cache: L2"
	print "|          Cache size:", repr(L2_cache_size)
	print "| Cache associativity:", repr(L2_cache_way)
	print "|                Hits:", repr(temp_h)
	print "|              Misses:", repr(temp_m)
	print "|            Hit Rate: %3.2f" % (temp_h * 100.0/ (temp_h + temp_m))
	print "o--------------------------o"

#	print len(g.cache.lruValue)
#	for i in range(len(g.cache.lruValue)):
#		print len(g.cache.lruValue[i])
	
def signal_handler(signal, frame):
	printSummary()
	sys.exit(0)

#o---------------------------------------------------------------------------o
def main():
	"""
	Main program; contains primary clock loop and core logic.
	associativity 0 = fully associative
	"""
	i=0
	j=0	

	count1 = 0
	count2 = 0
	count3 = 0
	count4 = 0
	



	if not len(sys.argv) == 7: # Check for command line arguments
		print "Usage: %s [ cache size L1 ] [ associativity L1 ] [ cache size L2 ] [ associativity L2 ] [ trace filename ] [ Block Size ]\n" % \
		os.path.basename(sys.argv[0])
		sys.exit(0)
	
	global L1_cache_size
	L1_cache_size=int(sys.argv[1])
	global L1_cache_way
	L1_cache_way=int(sys.argv[2])
	global L2_cache_size 
	L2_cache_size=int(sys.argv[3])
	global L2_cache_way
	L2_cache_way=int(sys.argv[4])
	global num_blocks_l1
	num_blocks_l1=(L1_cache_size*1024/int(sys.argv[6]))
	global num_blocks_l2
	num_blocks_l2=(L2_cache_size*1024/int(sys.argv[6]))
	global num_sets_l1
	num_sets_l1=(num_blocks_l1/L1_cache_way)
	global num_sets_l2
	num_sets_l2=(num_blocks_l2/L2_cache_way)
	global log2
	log2 = int(math.log(int(sys.argv[6]),2))


	inFile1 = sys.argv[5] # Input text file
	inFile2 = sys.argv[5] # Input text file
	inFile3 = sys.argv[5] # Input text file
	inFile4 = sys.argv[5] # Input text file
	
	infile1 = open(inFile1,"r")
#	infile2 = open(inFile2,"r")
#	infile3 = open(inFile3,"r")
#	infile4 = open(inFile4,"r")

	



#Setting up L1 cache
	for i in range (0,4):	
		L1.append(g1(Cache_l1()))

#Setting up L2 cache splits
	i=0
	for i in range(0,2):
		L2.append(g2(Cache_l2()))


	line = 0

	signal.signal(signal.SIGINT, signal_handler)


	while 1:
		global file_ext 
		file_ext = random.randint(0,3)
		
#		if file_ext==0:
		l = infile1.readline()
#		elif file_ext==1:
#		   l = infile2.readline()
#		elif file_ext==2:
#		   l = infile3.readline()
#		elif file_ext==3:
#		   l = infile4.readline()
	

		text = l.split(" ")
		if text[0] != '':
			text = text[1].split('\n')
			address=abs(int(text[0],16));
		else:
			address=0;
		
		line += 1
		if line % 10000 == 0:
			sys.stderr.write('processed queries: %d\r' %line)
			sys.stderr.flush()

		if address == 0:
			break # EOF, so shut down
			
# For speed, make these function calls once so
# we can just test the return values
		#print file_ext
		l1_cacheHit = L1[file_ext].cache.checkCacheHit(address)

# 		print address, cacheHit;
# Read reference --------------------------------------------------------
		if l1_cacheHit > 0:
# Data is in cache, so move on
			L1[file_ext].cache.incrementLRU(address)
			L1[file_ext].hits+=1
		else:
# Data is not in cache, so 
# L2 for whether it has it or not
# and fill the data from L2/memory
			L1[file_ext].cache.storeLRUBlock(address)
			L1[file_ext].misses+=1

			if file_ext==0 or file_ext==1:
				l2_check=0
			else:
				l2_check=1

			l2_cacheHit = L2[l2_check].cache.checkCacheHit(address)
			if l2_cacheHit > 0:
				L2[l2_check].cache.incrementLRU(address)
				L2[l2_check].hits+=1
			else:
				l2_cacheHit_n = L2[1-l2_check].cache.checkCacheHit(address)
				if l2_cacheHit_n > 0:
					L2[1-l2_check].cache.incrementLRU(address)
					L2[1-l2_check].hits+=1
				else:
					L2[l2_check].cache.storeLRUBlock(address)
					L2[l2_check].misses+=1
					if file_ext==1:
						L1[0].cache.invalidate(address)
					elif file_ext==0:
						L1[1].cache.invalidate(address)
					elif file_ext==2:
						L1[3].cache.invalidate(address)
					elif file_ext==3:
						L1[2].cache.invalidate(address)


		
					
# Display results of program run
	printSummary()
#	infile1.close();

if __name__ == "__main__": main()




