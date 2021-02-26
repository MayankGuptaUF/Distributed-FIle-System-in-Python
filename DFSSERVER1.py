import multiprocessing
import socket
import time
import pickle
def server_program(dict,count1,count2,q1,q2,r1,r2,rq1,rq2,req,di,dli,port=6000):
	
	# get the hostname
	host = socket.gethostname()
	host_str=str(host)+str(port)
	
	if(port==6000):
		port2=7000
	if(port==7000):
		port2=8000
	if(port==8000):
		port2=6000
	host_str2=str(host)+str(port2)
	server_socket = socket.socket()  # get instance
	
	server_socket.bind((host, port))  # bind host address and port together
	
	# configure how many client the server can listen simultaneously
	server_socket.listen(10)
	
	while True:
		
		conn, address = server_socket.accept()  # accept new connection
		print("Connection from: " + str(address))
		while True:
			data = conn.recv(16384).decode()
			if not data:
			# if data is not received break
				break
			
			temp=data
			
			data=data.split()
			if(data[0]=='connect'):
				print("Hello")
			if(data[0]=='write'):
				write(data[1],data[2])
				dict[data[1]]=[host_str,host_str2]
				
				q1.put(temp)
				q2.put(temp)
				count1.value=1
				count2.value=1
				rr=str(dict)
				conn.send(rr.encode())
				conn.send(data[2].encode())
			if(data[0]=='read'):
				l1=dict[data[1]]
				if(l1.count(host_str)>0):
					k=read(data[1])
					conn.send(bytes(read(data[1]), 'utf-8'))

				else:
					rq1.put(temp)		
					rq2.put(temp)
					r1.value=1
					r2.value=1
					while(1):
						read1=req.get()
						if read:	
							break
					
					print(read1)
					
					
					#r1.value=1
					conn.send(bytes(read1, 'utf-8'))
			if(data[0]=='create'):
				create(data[1])	
				dict[data[1]]=[host_str]
				q1.put(temp)
				q2.put(temp)
				count1.value=1
				count2.value=1
			if(data[0]=='delete'):
				delete(data[1])
				dict.pop(data[1])
				rr=str(dict)
				conn.send(rr.encode())
				dli.put(temp)
				di.value=1
			data = 'DONE'
			try:
				conn.send(data.encode())  # send data to the client
			except:
				pass
	#conn.close()  # close the connection


def write(filename,content):
	f = open(filename, "a")
	f.write(content)
	f.close()


def create(filename):
	f= open(filename,"w+")
	f.close()

def read(filename):
	f = open(filename, "r")
	return(f.read())

def delete(filename):
	try:

		os.remove(filename)
	except:
		return False
def intraserver(port,q,shared_dict,count,f,r1,rq1,di,dli,req):
	host = socket.gethostname()
	server_socket = socket.socket() 
	server_socket.bind((host, port))
	server_socket.listen(2)
	
	while 1:
		conn, address = server_socket.accept()
		print("Connection from:server " + str(address))
		print(count.value)
		serialized_dict = pickle.dumps(shared_dict.copy())
		#data=serialized_dict.encode()
		#count.value=0
		conn.send(serialized_dict)
		
		while 1:
			
			if(count.value==1 and f==0):
				
				print(shared_dict)
				serialized_dict = pickle.dumps(shared_dict.copy())
				#data=serialized_dict.encode()
				conn.send(serialized_dict)
				("here")
				
				count.value=0
			
			if(count.value==1 and f==1):
				#serialized_dict = pickle.dumps(shared_dict.copy())
				#data=serialized_dict.encode()
				#conn.send(serialized_dict )
				#("here")
				while(q.empty() is False):
					out=q.get()
				#print(out)
				out=pickle.dumps(out)
				#out=out.encode()
				conn.send(out)
				
				count.value=0

			if(r1.value==1 and f==0):
				#serialized_dict = pickle.dumps(shared_dict.copy())
				#data=serialized_dict.encode()
				#conn.send(serialized_dict)
				while(rq1.empty() is False):
					out1=rq1.get()
				#print("out1")
				out1=pickle.dumps(out1)
				#out1=out1.encode()
				
				conn.send(out1)
				while 1:
					read=conn.recv(16384)
					
					if read:
						break
				read=pickle.loads(read)
				req.put(read)
				#print("hello")
				print(read)
				r1.value=0
				
			if(di.value==1 and f1==0):
				serialized_dict = pickle.dumps(shared_dict.copy())
				conn.send(serialized_dict)
				di.value=0
			if(di.value==1 and f1==1):
				serialized_dict = pickle.dumps(shared_dict.copy())
				conn.send(serialized_dict)
				print("sending")
				try:
					while(dli.empty() is False):
						out2=dli.get()
					print(out2)
					out2=pickle.dumps(out2)
					conn.send(out2)
				except:
					pass
				di.value=0
			if(hasher.value==1):
				serialized_dict = pickle.dumps(shared_dict.copy())
				conn.send(serialized_dict)
				hasher.value=0

def intraclient(port,q,shared_dict):
	
	host = socket.gethostname()
	host_str=str(host)+str(port)
	
	port1=6000
	if(port==7002):
		port2=7000
	if(port==8001):
		port2=8000
	host_str1=str(host)+str(port1)
	host_str2=str(host)+str(port2)
	client_socket = socket.socket()
	while 1:
		try:
			client_socket.connect((host, port))
			break
	
		except:
			m=1	
	
	try:
		data = client_socket.recv(16384)
		dta=pickle.loads(data)
		dit.update(dta)
		#print(dict)
		#print(dta)
	except:
		pass
	while 1:
		data = client_socket.recv(16384)
		if data:
			dta=pickle.loads(data)
			#print(dta)
			#print(type(dta))
			
			if isinstance(dta, str)==True:
				print(dta)
				dta=dta.split()
				if(dta[0]=='read'):
					k=read(dta[1])
					print("here")
					sreial=pickle.dumps(k)
					client_socket.send(sreial)
				if(dta[0]=='create'):
					create(dta[1]) 
				if(dta[0]=='write'):
					write(dta[1],dta[2])
					shared_dict[dta[1]]=[host_str2,host_str1]
					print(shared_dict)
				if(dta[0]=='delete'):
					delete(dta[1])
					shared_dict.pop(dta[1])
			if isinstance(dta, dict)==True:
				shared_dict.update(dta)
				print(shared_dict)
		#data = client_socket.recv(16384).decode()
		#print(data)
		#dta=json.loads(data)
	
	
	#client_socket.close()

if __name__ == '__main__':
	manager = multiprocessing.Manager()
	count1 = multiprocessing.Value('i', 0)
	count2 = multiprocessing.Value('i', 0)
	f1=1
	f2=0
	req=multiprocessing.Queue()
	hasher= multiprocessing.Value('i', 0)
	r1=multiprocessing.Value('i', 0)
	r2=multiprocessing.Value('i', 0)
	rq1=multiprocessing.Queue()
	rq2=multiprocessing.Queue()
	di=multiprocessing.Value('i',0)
	dli=multiprocessing.Queue()
	shared_dict = manager.dict()
	q1=multiprocessing.Queue()
	q2=multiprocessing.Queue()
	p1 = multiprocessing.Process(target=server_program, args=(shared_dict,count1,count2,q1,q2,r1,r2,rq1,rq2,req,di,dli,6000))
	p2 = multiprocessing.Process(target=intraserver, args=(6001,q1,shared_dict,count1,f1,r1,rq1,di,dli,req))
	p3 = multiprocessing.Process(target=intraserver, args=(6002,q2,shared_dict,count2,f2,r2,rq2,di,dli,req))
	p4 = multiprocessing.Process(target=intraclient, args=(8001,q1,shared_dict))
	p5 = multiprocessing.Process(target=intraclient, args=(7002,q2,shared_dict))
	#p4 = multiprocessing.Process(target=editq, args=(q,))
	p1.start()
	p2.start()
	p3.start()
	p4.start()
	p5.start()
	p1.join()
	p2.join()
	p3.join()
	p4.join()
	p5.join()
