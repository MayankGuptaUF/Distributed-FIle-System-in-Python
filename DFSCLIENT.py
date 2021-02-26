import socket
import random
import string
import sys
def client_program():
	IP1=sys.argv[1]
	IP2=sys.argv[2]
	IP3=sys.argv[3]
	cell=[IP1,IP2,IP3]
	final=random.choice(cell)
	IP=final.split(':')
	host = IP[0]  # as both code is running on same pc
	port = int(IP[1])  # socket server port number

	client_socket = socket.socket()  # instantiate
	client_socket.connect((host, port))  # connect to the server
	message='connect'
	while message.lower().strip() != 'exit':
		client_socket.send(message.encode())  # send message
		data = client_socket.recv(1024).decode()  # receive response
		
		print('Received from server: ' + data)  # show in terminal
		data=None
		while data==None:
			data1=input("->")
			message=data1
			if(message[:5]=='write'):
				k=randomString(int(message.split()[2]))
				message = message.split()[0] + ' ' +message.split()[1] + ' ' + k
			break
		#message = input(" -> ")  # again take input
		#message='bye'
	client_socket.close()  # close the connection



def randomString(stringLength=8):
	letters = string.ascii_lowercase
	return ( ''.join(random.choice(letters) for i in range(stringLength)) )


if __name__ == '__main__':
	client_program()
