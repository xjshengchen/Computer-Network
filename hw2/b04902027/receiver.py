import socket

outputfile = "result"

agent = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('localhost', 7777)

agent.sendto('RECEIVER', addr)                          # setup

data, addr = agent.recvfrom(2048)                       # filename
if data != "":
	file = open(outputfile + "." + data, "a")
else:
	file = open(outputfile, "a")

exp_i = 1
dup_i = 0

buff = ""
buffSize = 32
buff_i = 0

def flush():
	global buff
	global buff_i 
	file.write(buff)                                
	print "flush"
	buff_i = 0
	buff = ""
	return

while 1:
	data, addr = agent.recvfrom(2048)

	if data == "fin":                                   # END
		print "recv\t" + data
		data = "finack"
		agent.sendto(data, addr)
		print "send\t" + data
		flush()
		break

	num = int(data.split(":",1)[0])
	data_i = data.split(":",1)[1]

	if num == exp_i:                                   # right data
		if buff_i < buffSize:                          # not full
			print "recv\tdata\t#" + str(num)
			buff = buff + data_i                       # buffering
			buff_i = buff_i + 1
			data = str(exp_i)
			agent.sendto(data, addr)
			print "send\tack\t#" + str(exp_i)
			dup_i = exp_i
			exp_i = exp_i + 1
		else:                                           # full
			print "drop\tdata\t#" + str(num)
			data = str(dup_i)
			agent.sendto(data, addr)
			print "send\tack\t#" + str(dup_i)
			flush()
	else:                                               # drop
		print "drop\tdata\t#" + str(num)
		data = str(dup_i)
		agent.sendto(data, addr)
		print "send\tack\t#" + str(dup_i)

file.close()
agent.close()