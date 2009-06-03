#!/usr/bin/python

#o---------------------------------------------------------------------------o
# Cache simulator 
# Author: Susmit Biswas
# Email: susmit at cs dot ucsb dot edu
# Description: This is a very basic cache simulator that I wrote for my work.
# It does not distinguish between read and writes though that can be
# incorporated quite easily. It simulates caches with any associativity and
# size. I started with a code that I found online, but it was incorrect. So, I
# wrote my own simulator though the structure of the simulator is pretty much
# the same. Please let me know if you find anything wrong.
#o---------------------------------------------------------------------------o


import os
import sys
import signal 
import string
import math


#o---------------------------------------------------------------------------o
class g:
# Global constants
	CACHE_SIZE    = 0  # Number of blocks in cache
	CACHE_WAY         = 1  # For set associative, size of each set
	inFile       = ''      # Input text file

	cache         = 0  # Instance of cache class
# * Mapping Strategy:
#     0 -> Fully associative

	hits=0
	misses=0

#o---------------------------------------------------------------------------o

	
class Cache:
	def __init__(self):
		self.lruValue    = {}
		self.clearCache()

   # Zero out cache blocks/flags/values
	def clearCache(self):
		for n in range(32768):
			self.lruValue[n]={}
	
	def checkCacheHit(self, address):
		add=address
		index=int((add >> int((math.log(32,2))))%(32768))

		if self.lruValue[index].has_key(address):
			return 1;
		else:
			return -1;

	def incrementLRU(self, address):
		add=address
		index=int((add >> int((math.log(32,2))))%(32768))

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
		index=int((add >> int((math.log(32,2))))%(32768))


		max_value = -1;
		max_value_key = -1;
			
		for key, value in self.lruValue[index].iteritems():
			if len(self.lruValue[index]) == g.CACHE_WAY :
				if value > max_value:
					max_value_key = key;
					max_value = value;
			self.lruValue[index][key]+=1;
				
		if len(self.lruValue[index]) == g.CACHE_WAY :
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

	print ""
	print "o--------------------------o"
	print "|          Input file:", g.inFile
	print "|          Cache size:", repr(g.CACHE_SIZE)
	print "| Cache associativity:", repr(g.CACHE_WAY)
	print "|                Hits:", repr(g.hits)
	print "|              Misses:", repr(g.misses)
	print "|            Hit Rate: %3.2f" % (g.hits * 100.0/ (g.hits + g.misses))
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
	
	if not len(sys.argv) == 4: # Check for command line arguments
		print "Usage: %s [ cache size ] [ associativity] [ trace filename ]\n" % \
		os.path.basename(sys.argv[0])
		sys.exit(0)

	g.CACHE_SIZE   = int(sys.argv[1]) # Cache size
	g.CACHE_WAY	= int(sys.argv[2]) # Cache mapping (1, 2, 3)
	if g.CACHE_WAY == 0:
		g.CACHE_WAY = g.CACHE_SIZE
	g.inFile       = sys.argv[3]      # Input text file
	g.cache = Cache() # Set instance of cache class


	line = 0

	signal.signal(signal.SIGINT, signal_handler)

	infile = open(g.inFile,"r")
	while 1:
		print "Here"
		l = infile.readline()
		text=l.split(" ")
		if text[0] != '':
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
		cacheHit = g.cache.checkCacheHit(address)

# 		print address, cacheHit;
# Read reference --------------------------------------------------------
		if cacheHit > 0:
# Data is in cache, so move on
			g.cache.incrementLRU(address)
			g.hits+=1
		else:
# Data is not in cache, so pull it from
# lower memory and then store it in the
# cache
			g.cache.storeLRUBlock(address)
			g.misses+=1


# Display results of program run
	printSummary()
	infile.close();

if __name__ == "__main__": main()



