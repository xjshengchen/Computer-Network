import socket
import select
from timeit import default_timer

inputfile = "input.jpg"
t_time = 0.5

agent = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('localhost', 7777)

agent.sendto('SENDER', addr)                          # setup
file = open(inputfile, "r")
text = file.read()
data_i = [text[i:i+1024] for i in range(0, len(text), 1024)]
n_line = len(data_i)
flag = [0] * (n_line + 1)

data, addr = agent.recvfrom(2048)                     # waiting for server 
if data != 'START':
	while 1:
		1

winSize = 1
base = 1
last = base + winSize
next = 1
threshold = 16

if inputfile.find(".") != -1:                         # filename
	agent.sendto(inputfile.split(".",1)[1], addr)
else:
	agent.sendto("", addr)

agent.setblocking(0)

while 1:                                              
	if base > n_line:                                 # END
		data = "fin"
		print "send\t" + data
		agent.sendto(data, addr)
		ready = select.select([agent], [], [], 0.01)
		if ready[0]:
			data, addr = agent.recvfrom(2048)
			print "recv\t" + data
			break
    
	while next < last:
		if next == base:                              # earliest
			start_time = default_timer()
		data = str(next) + ":" + data_i[next-1]
		agent.sendto(data, addr)
		if flag[next] == 0:                           # first send
			print "send\tdata\t#" + str(next) + ",\twinSize = " + str(winSize)
			flag[next] = 1
		else:                                         # resend
			print "resnd\tdata\t#" + str(next) + ",\twinSize = " + str(winSize)
		next = next + 1

	ready = select.select([agent], [], [], 0.01)
	if ready[0]:
		data, addr = agent.recvfrom(2048)
		print "recv\tack\t#" + data
		base = int(data) + 1        
	if default_timer() - start_time > t_time:               # timeout
		next = base
		threshold = max(winSize/2, 1)
		winSize = 1
		last = base + winSize
		print "time\tout,\t\tthreshold = " + str(threshold)
	if base == last:                                   # finish round
		base = last
		if winSize < threshold:
			winSize = winSize * 2
		else:
			winSize = winSize + 1
		if base + winSize <= n_line:
			last = base + winSize
		else:
			last = n_line + 1 

file.close()
agent.close()
