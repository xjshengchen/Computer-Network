import socket
import random

rate = 0.01
n_all = 0
n_loss = 0

agent = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr_agent = ('localhost', 7777)
agent.bind(addr_agent)                                # server listen at 7777

for i in range(2):                                    # setup
	data, addr = agent.recvfrom(2048)
	if data == 'SENDER':
		addr_sender = addr
		print "connected: SENDER from", addr_sender
	if data == 'RECEIVER':
		addr_receiver = addr
		print "connected: RECEIVER from", addr_receiver

data_start = 'START'
agent.sendto(data_start, addr_sender)                 # start 

data, addr = agent.recvfrom(2048)                     # filename
agent.sendto(data, addr_receiver)

while 1:                                              # listen
	data, addr = agent.recvfrom(2048)
	if addr == addr_sender:
		if data == "fin":                             # END
			print "get\t" + data
			agent.sendto(data, addr_receiver)
			print "fwd\t" + data
			continue

		n_all = n_all + 1
		num = int(data.split(":",1)[0])
		print "get\tdata\t#" + str(num)
		if random.random() < rate:                    # loss
			n_loss = n_loss + 1
			print "drop\tdata\t#" + str(num) + ",\tloss rate = " + str(n_loss/(n_all*1.0))
		else:                                         # good	
			agent.sendto(data, addr_receiver)
			print "fwd\tdata\t#" + str(num) + ",\tloss rate = " + str(n_loss/(n_all*1.0))
	
	if addr == addr_receiver:
		if data == "finack":                          # END
			print "get\t" + data
			agent.sendto(data, addr_sender)
			print "fwd\t" + data
			break

		print "get\tack\t#" + data
		agent.sendto(data, addr_sender)
		print "fwd\tack\t#" + data

agent.close()
