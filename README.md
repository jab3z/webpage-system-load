webpage-system-load
===================

Display average system statistics (load time, cpu, memory, net) for a process that loads a webpage
for a specified number of times


USAGE

      ./urlstat.py URL loops 
                
                  - display system statistics averages after loading the URL url for loops times 


SAMPLE RUN

	bal@balap:~$ ./urlstat.py http://google.com 3 
		  
	AVERAGE STATS for 3 loops:
	--------------

	Load time: 438 ms

	CPU
	   User:   3.33333333333 ticks
	   System: 2.66666666667 ticks

	Memory
	 Total:    3004.0 pages

	Net:
	   wlan0 received bytes  : 12935
	   wlan0 received packets: 19
	   eth0 received bytes  : 0
	   eth0 received packets: 0
