import socket
import time

file = open("config", "r") 
line = file.readline()
channel = line.split("'")[1]

botnick = "ShengTanBOT"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect(("irc.freenode.net" , 6667))
irc.send("NICK "+ botnick +"\r\n")
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\r\n")
irc.send("JOIN "+ channel +"\r\n")
irc.send("PRIVMSG " + botnick + " :iNOOPE\r\n") 
irc.send("PRIVMSG "+ channel +" :Hello! I am robot.\r\n")

while 1:
	query = irc.recv(2048);

	if query.find(":@hi") != -1:
		irc.send("PRIVMSG "+ channel +" :Hello! \r\n")
	if query.find("PING") != -1:
		irc.send("PONG " + query.split() [1] + "\r\n") 
	if query.find(":@exit") != -1:
		break
	if query.find(":@repeat") != -1:
		s = query.split(":@repeat ",1)[1]
		ss = " :" + s.split("\r\n")[0]
		irc.send("PRIVMSG "+ channel +" "+ ss + "\r\n")
	if query.find(":@convert") != -1:
		s = query.split(":@convert ",1)[1]
		ss = s.split("\r\n")[0]
		if ss.find("0x") != -1:
			irc.send("PRIVMSG "+ channel +" "+ str(int(ss,16)) + "\r\n")
		else:
			irc.send("PRIVMSG "+ channel +" "+ str(hex(int(ss))) + "\r\n")
	if query.find(":@help") != -1:
		irc.send("PRIVMSG "+ channel +" :@repeat <Message>.\r\n")
		irc.send("PRIVMSG "+ channel +" :@convert <Number>.\r\n")
		irc.send("PRIVMSG "+ channel +" :@ip <String>.\r\n")
	if query.find(":@ip") != -1:
		s = query.split(":@ip ",1)[1]
		ss = s.split("\r\n")[0]
		l = int(len(ss))
		if l<4 or l>12:
			irc.send("PRIVMSG "+ channel +" :Invalid Input!\r\n")
			continue
		ans_list = []
		for i in range(1,l-2):
			for j in range(i+1,l-1):
				for k in range(j+1,l):
					a = ss[0:i]
					b = ss[i:j]
					c = ss[j:k]
					d = ss[k:l]
					if int(a)>255 or int(b)>255 or int(c)>255 or int(d)>255:
						continue
					if (a[0]=="0" and len(a)!=1) or (b[0]=="0" and len(b)!=1) or (c[0]=="0" and len(c)!=1) or (d[0]=="0" and len(d)!=1):
						continue
					ans_list.append(a+"."+b+"."+c+"."+d)
		ans = len(ans_list)
		irc.send("PRIVMSG "+ channel + " " + str(ans) +"\r\n")
		for i in range(0,ans):
			irc.send("PRIVMSG "+ channel + " " + ans_list[i] +"\r\n")
			time.sleep(1)
			
irc.close()