#!/usr/bin/env python

from sys import argv
from urllib import urlopen
from os import getpid, times
from time import time

def read(name):
	with open(name, 'r') as f:
		return f.read()

def get_cpu_stat(pid):
	stat_str = read('/proc/{}/stat'.format(pid))
	stat_list = stat_str.split(' ')
	return  float(stat_list[13]), float(stat_list[14])	

def get_mem_stat(pid):
	stat_str = read('/proc/{}/statm'.format(pid))
	(size, rss, shared, code, data, lib, dirty) = stat_str.split (' ')
	return float(size)

def get_ms_time():
	return int(round(time() * 1000))			
		
def print_cpu_stat(cpu_usr_l, cpu_sys_l, loops):
	print "\nCPU"	
	print "   User:   {} ticks".format(sum(cpu_usr_l)/loops)	
	print "   System: {} ticks".format(sum(cpu_sys_l)/loops)

def print_mem_stat(mem_size_l, loops):
	print "\nMemory"
	print " Total:    {} pages".format(sum(mem_size_l)/loops)

def print_load_time(load_time_l, loops):
	print "\nLoad time: {} ms".format(sum(load_time_l)/loops)
		
URL = argv[1]
loops = int(argv[2])

cpu_usr_l, cpu_sys_l = [], []
mem_size_l = []
load_time_l = []

for i in range(loops):
	start_secs = get_ms_time()
	page = urlopen(URL)
	stop_secs = get_ms_time()
	
	my_pid = getpid()
	
	load_time_l.append(stop_secs-start_secs)				
	cpu_utime, cpu_stime = get_cpu_stat(my_pid)
	mem_size = get_mem_stat(my_pid)
	
	cpu_usr_l.append(cpu_utime)
	cpu_sys_l.append(cpu_stime)
	mem_size_l.append(mem_size)

print "\nAVERAGE STATS for {} loops".format(loops)
print "--------------"
print_load_time(load_time_l, loops)	
print_cpu_stat(cpu_usr_l, cpu_sys_l, loops)
print_mem_stat(mem_size_l, loops)
