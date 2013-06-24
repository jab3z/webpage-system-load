#!/usr/bin/env python

from sys import argv
from urllib import urlopen
from os import getpid, times
from time import time

def read(name):
	with open(name, 'r') as f:
		return f.readlines()

def get_cpu_stat(pid):
	stat_str = read('/proc/{}/stat'.format(pid))[0]
	stat_list = stat_str.split(' ')
	return  float(stat_list[13]), float(stat_list[14])	

def get_mem_stat(pid):
	stat_str = read('/proc/{}/statm'.format(pid))[0]
	(size, rss, shared, code, data, lib, dirty) = stat_str.split (' ')
	return float(size)

def get_ms_time():
	return int(round(time() * 1000))			
		
def get_net_stat():
	# gets the received bytes and packets values
	# for wland and eth interfaces
	ret_l = []
	lines = read('/proc/net/dev')
	for line in lines:
		if 'wlan' in line or 'eth' in line:
				line_l = line.split()
				line_l[0] = line_l[0][:-1]  ;#discard trailing colon
				ret_l.append(line_l[:3])	;#get if name, bytes and packages	
	return ret_l			 

def compute_net_stats(start_stats, end_stats):
	ret_l = []
	for start_l, end_l in zip(start_stats, end_stats):
		interface  = end_l[0]
		bytes_stat = int(end_l[1]) - int(start_l[1])
		packs_stat = int(end_l[2]) - int(start_l[2])
		ret_l.append([interface, bytes_stat, packs_stat])
	return ret_l
		
def print_cpu_stat(cpu_usr_l, cpu_sys_l, loops):
	print "\nCPU"	
	print "   User:   {} ticks".format(sum(cpu_usr_l)/loops)	
	print "   System: {} ticks".format(sum(cpu_sys_l)/loops)

def print_mem_stat(mem_size_l, loops):
	print "\nMemory"
	print " Total:    {} pages".format(sum(mem_size_l)/loops)

def print_load_time(load_time_l, loops):
	print "\nLoad time: {} ms".format(sum(load_time_l)/loops)
	
def print_net_stat(net_stat_d, loops):
	print "\nNet:"
	for key, val in net_stat_d.iteritems():
		print("   {} received bytes  : {}".format(key, sum(val[0])/loops))
		print("   {} received packets: {}".format(key, sum(val[1])/loops))
	
def init_net_stat_d():
	ret_d = dict()
	# hold the netstat data in a dict that contains list of two lists for each 
	# interface. The two lists will represent received bytes and packets for 
	# the interface used as a key 
	net_stat = get_net_stat()
	for stat_l in net_stat:
		ret_d[stat_l[0]] = [[], []]
	return ret_d	
	
URL = argv[1]
loops = int(argv[2])

cpu_usr_l, cpu_sys_l = [], []
mem_size_l = []
load_time_l = []
net_stat_d = init_net_stat_d()

for i in range(loops):
	start_net_stat = get_net_stat()
	start_secs = get_ms_time()
	page = urlopen(URL)		
	stop_secs = get_ms_time()
	stop_net_stat = get_net_stat()

	my_pid = getpid()
	
	load_time_l.append(stop_secs-start_secs)				
	cpu_utime, cpu_stime = get_cpu_stat(my_pid)
	mem_size = get_mem_stat(my_pid)
	net_stat = compute_net_stats(start_net_stat, stop_net_stat)			
	
	cpu_usr_l.append(cpu_utime)
	cpu_sys_l.append(cpu_stime)
	mem_size_l.append(mem_size)
	for l in net_stat:
		key = l[0]
		net_stat_d[key][0].append(int(l[1]))	
		net_stat_d[key][1].append(int(l[2]))
	
print "\nAVERAGE STATS for {} loops".format(loops)
print "--------------"
print_load_time(load_time_l, loops)	
print_cpu_stat(cpu_usr_l, cpu_sys_l, loops)
print_mem_stat(mem_size_l, loops)
print_net_stat(net_stat_d, loops)
