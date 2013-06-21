#!/usr/bin/env python

from sys import argv
from urllib import urlopen
from os import getpid, times

def read(name):
	with open(name, 'r') as f:
		return f.read()
		
class url_info:
	def __init__(self, pid):
		self.id = pid
		self.cpu_utime = 0
		self.cpu_stime = 0
		self.cpu_avg_utime = 0
		self.cpu_avg_stime = 0
				
def print_cpu_stat(pid):
	stat_str = read('/proc/{}/stat'.format(pid))
	stat_list = stat_str.split(' ')		
	print "\nCPU"	
	print "   User:   {} ticks".format(stat_list[13])	
	print "   System: {} ticks".format(stat_list[14])

def print_mem_stat(pid):
	stat_str = read('/proc/{}/statm'.format(pid))
	(size, rss, shared, code, data, lib, dirty) = stat_str.split (' ')
	print "\nMemory"
	print " Total used: {} pages".format(size)

def get_cpu_stat(pid):
	stat_str = read('/proc/{}/stat'.format(pid))
	stat_list = stat_str.split(' ')
	usr_mem = stat_list[13]
	sys_mem = stat_list[14]	
		
URL = argv[1]
loops = int(argv[2])

for i in range(loops):
	page = urlopen(URL)
	
my_pid = getpid()	
print_cpu_stat(my_pid)
print_mem_stat(my_pid)
