import socket
import sys
import getpass

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg: 
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();

print 'Socket Created'

host = ''
port = 7986

try: 

    remote_ip = socket.gethostbyname( host ) 

except socket.gaierror: 
    print ' Hostname could not be resolved. Exiting' 
    sys.exit()

print 'IP ADDR of ' + host + ' is ' + remote_ip

s.connect((remote_ip, port))

print ' Socket Connected to ' + host + ' on ip ' + remote_ip

password = 0
close = 0

while (1):
        #Receive Data
	reply = s.recv(4096)
        if ( reply == 'Password'): 
	     password = 1
        elif ( reply == 'Closing'):
	     close = 1
             sys.exit()
        else:
	       print reply

	try: 
          if ( password == 1 ): 
	      message = getpass.getpass(prompt="Please enter your password:\n")
	      password = 0
	  else:
            message = raw_input()
	  
          if close != 1:
    	     s.send(message)
            # print 'Sent:' + message
          else: 
             break
	except socket.error:
    	  print 'Send failed'
    	  sys.exit()

	#print 'Message sent successfully'

s.close()
