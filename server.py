import socket
import sys

from thread import *

HOST = '' # means all available interfaces
PORT = 7986
connList = []
addrList = []
accList = [
   ('PizzaMan', 'Pineapple'),
   ('Hello', '1234'),
   ('Easy', 'Name')
]
offline_list = [
   ('PizzaMan', 'Pineapple'), 
   ('Hello', '1234'),
   ('Easy','Name')
]
conn_index_list = []
friends_list = []

currFriends_P = []
currFriends_H = []
currFriends_E = []

friendList_P = []
friendList_H = []
friendList_E = []

mailList_P = []
mailList_H = []
mailList_E = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Errors: ' + str(msg[0]) + ' Message ' + str(msg[1]) 
    sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'


def changePassword(account):
    old_passwdFlag = 0
    new_passwdFlag = 0
   # conn.send("Changing Account Password!: \n")
    for i in range(0, len(accList)):

	    if ( account == accList[i]):
                
	        while ( old_passwdFlag != 1 ):
		      conn.send("Type in your old Password:\n") 
		      oldpswd = conn.recv(1024)
		      if ( oldpswd != account[1] ):
			  conn.send("Wrong old password!\n")
		      else: 
		          old_passwdFlag = 1
                while ( new_passwdFlag != 1 ):
		       conn.send("Type in your new Password:\n")
		       newpswd = conn.recv(1024)
		       if ( newpswd > 1 ): 
		           new_passwdFlag = 1
                newaccount = (account[0], newpswd)
                accList[i] = newaccount
                conn.send("New Password created: " + str(accList[i]))
		break
        
        
        
def check_acc(account):
    none = 0;
    for k in range(0,len(offline_list)):
	if ( account == offline_list[k]):
	     offline_list.remove(offline_list[k])
	     break

    for i in range(0, len(accList)):
	if ( account != accList[i] ):
	   none = none + 1
           continue
	else:
	  if ( account == accList[i] ): 
             conn.send(account[0] + " has connected!")
          return 1

    if ( none == 3 ): 
	    conn.send("Sorry, username or password is incorrect\n")
	    return 0
	   
def accept_friendRequests(mailbox, uname):
	for i in range(0, len(mailbox)):
	   conn.send(mailbox[i] + " wants to be your friend\n Yes(Y) or No(N)?\n")
	declined = []
	conn.send("Do you want to answer your friend requests?\n")
	answer = conn.recv(1024)
        if ( answer == 'yes'):
                for i in range(0,len(mailbox)):
		   conn.send("Y/N: " + mailbox[i] + "\n")
		   rep = conn.recv(1024)
		   if ( rep == 'Y' ):
			if ( uname == 'PizzaMan'):
			    currFriends_P.append( mailbox[i] )
			    if ( mailbox[i] == 'Hello'):
				currFriends_H.append(uname)
			    elif (mailbox[i] == 'Easy'):
				currFriends_E.append(uname)
			elif ( uname == 'Hello' ):
			    currFriends_H.append( mailbox[i] )
		    	    if ( mailbox[i] == 'PizzaMan'):
                                currFriends_P.append(uname)
                            elif (mailbox[i] == 'Easy'):
                                currFriends_E.append(uname)
		        elif ( uname == 'Easy' ):
			    currFriends_E.append( mailbox[i] )
			    if ( mailbox[i] == 'PizzaMan'):
                                currFriends_P.append(uname)
                            elif (mailbox[i] == 'Hello'):
                                currFriends_H.append(uname)
		   elif ( rep == 'N'):
		   	continue
		   else:
			declined.append(mailbox[i])
			conn.send("We take that as a no answer!")
			continue

	        return declined
        elif ( answer == 'no'):
	    return 0 
        return declined
#function for handling connections and create threads
def clientthread(conn, addr): 
    #Sending msg to client
    uname_flag = 0
    passwd_flag = 0
    mailBox = 0
    mail = 0
    userIndex = 0
    p_sending = ''
    conn.send('Welcome to the server.\n') #only takes strings
    while 1:

    	while ( uname_flag != 1 ):
    	   conn.send('Please enter your username:') 
    	   uname = conn.recv(1024)
           if ( uname > 1 ): 
	            uname_flag = 1
    
        while ( passwd_flag != 1 ):	
    	   conn.send('Password')
    	   passwd = conn.recv(1024)
           if ( passwd > 1 ):
	          passwd_flag = 1

        account = (uname, passwd)
        print "ACCOUNT ENTERED:" + uname + " " + passwd
        if ( check_acc(account) == 1 ):
	   #find MailBox, add index
           userIndex = len(connList) - 1
           new_tuple = (uname, str(userIndex))
           conn_index_list.append(new_tuple);
	   if ( uname == 'PizzaMan'): 
	       mailBox = 0
           elif ( uname == 'Hello'):
               mailBox = 1
           else:
               mailBox = 2
	   break
        else:
	   uname_flag = 0
           passwd_flag = 0
	   continue
  
    while True:

     conn.send('\nChoose an option: \n\t 1. Group Messaging\n \t 2. Change Password\n \t 3. Logout\n \t 4. Mailbox \n \t 5. Private Messaging \n \t 6. Friend Mailbox \n \t 7. Friend Requests \n \t 8. Friend List \n')
     ureply = conn.recv(1024)
     if ( ureply == '1' ): 
         #Group Messaging
	  conn.send("Broadcast Messaging On! Type !q to stop messaging.")
          while(1):
	    #print(len(connList))
            msg_all = conn.recv(1024)
	    if ( msg_all != "!q"):
               for i in range(0, len(connList)):
                    connList[i].sendall(account[0] + ": " + msg_all + "\n")
		    for j in offline_list:
			if ( j[0] == 'PizzaMan'):
			   mailList_P.append(account[0] + ": " + msg_all)
			if ( j[0] == 'Hello'):
			   mailList_H.append(account[0] + ": " + msg_all)
			if ( j[0] == 'Easy'):
			   mailList_E.append(account[0] + ": " + msg_all)
			continue
			
               #   if ( conn != connList[i] ):  
	#	     conn.sendto(account[0] + ": " + msg_all + "\n", addrList[i])
	    else:
		conn.send("You have left Messaging!")
		break
     elif ( ureply == '2'):
             #change Password
             changePassword(account) 
	     continue
     elif ( ureply == '3'):
             print uname + " logging out\n" 
             offline_list.append(uname)
             conn.send('Closing')
             conn.close()
             connList.remove(conn) 
             break
	     #Logout
     elif ( ureply == '4'):
           #Check Unread Messages
	    if ( mailBox == 0 ):
		unread_msgs = len(mailList_P)
		mail = 0
            elif (mailBox == 1):
		unread_msgs = len(mailList_H)
		mail = 1
	    else:
		unread_msgs = len(mailList_E)
		mail = 2

	    conn.send("You have " + str(unread_msgs) + " pending messages.\n")
            conn.send("Would you like to view them?(y/n)\n")
	    ask = conn.recv(1024)
	    if ( ask == "y" ):
		if ( mail == 0 ):
 		   for k in mailList_P:
		      conn.send(k + "\n")
                   del mailList_P[:]
		elif ( mail == 1 ): 
		   for k in mailList_H:
		      conn.send(k + "\n")
		   del mailList_H[:]
		else:
		   for k in mailList_E:
		      conn.send(k + "\n")
		   del mailList_E[:]
            continue
     elif ( ureply == '5' ):
	  conn.send("Enter user to send private message to: \n" )
	  user_sendto = conn.recv(1024)
	  conn.send("Type your message: \n") 
	  if ( user_sendto == "PizzaMan" ):
	      p_sending = conn.recv(1024)
              for i in conn_index_list:
                 if(i[0] == "PizzaMan"):
		    connList[int(i[1])].sendall(uname + ": " + p_sending)
	      for j in offline_list:
                 if ( j[0] == 'PizzaMan'):
                     mailList_P.append(uname + ": " + p_sending)
	      continue 
          elif ( user_sendto == "Hello"):
	      p_sending = conn.recv(1024)
              for i in conn_index_list:
                 if(i[0] == "Hello"):
                    connList[int(i[1])].sendall(uname + ": " + p_sending)
              for j in offline_list:
                 if ( j[0] == 'Hello'):
                     mailList_H.append(uname + ": " + p_sending)
	      continue
	  elif ( user_sendto == "Easy"):
              p_sending = conn.recv(1024)
              for i in conn_index_list:
                 if(i[0] == "Easy"):
                    connList[int(i[1])].sendall(uname + ": " + p_sending)
              for j in offline_list:
                 if ( j[0] == 'Easy'):
                     mailList_E.append(uname + ": " + p_sending)
	      continue
	  else:
	     conn.send("User does not exist")
             continue  
     elif ( ureply == '6' ):
	  if ( mailBox == 0 ):
	     conn.send("You have " + str(len(friendList_P)) + " friend requests.\n")
	     if ( len(friendList_P) != 0 ):
	         num_declined = accept_friendRequests(friendList_P, uname)
		 conn.send("Your friends: \n")
		 for i in currFriends_P: 
		    conn.send(i + "\n")
		 if ( num_declined != 0 ):
		     del friendList_P[:]
		     for j in num_declined:
		        friendList_P.append(j)
		    
		    

          elif ( mailBox == 1 ):
	     conn.send("You have " + str(len(friendList_H)) + " friend requests.\n")
             if ( len(friendList_H) != 0 ):
                 num_accepted = accept_friendRequests(friendList_H, uname)
                 conn.send("Your friends: \n")
                 for i in currFriends_H:
                    conn.send(i + "\n")
	  else: 
	     conn.send("You have " + str(len(friendList_E)) + " friend requests.\n")
	     if ( len(friendList_E) != 0 ):
                 num_accepted = accept_friendRequests(friendList_E, uname)
                 conn.send("Your friends: \n")
                 for i in currFriends_E:
                    conn.send(i + "\n")
	
	  #check friend mailbox
     elif ( ureply == '7' ):
	  conn.send("Type in a username to send a friend request to: \n")
	  fname = conn.recv(1024)
	  if ( fname == "PizzaMan"):
	  	friendList_P.append(uname)
	  elif (fname == "Hello"):
		friendList_H.append(uname)
	  elif (fname == "Easy"):
	        friendList_E.append(uname)
          else:
	  	continue
	  continue
	  #send friend request
     elif ( ureply == '8'):
	  conn.send("Your friends: \n")
 	  if ( mailBox == 0 ): 
		for i in currFriends_P:
                    conn.send(i+ "\n")
	  elif ( mailBox == 1): 
		for i in currFriends_H:
                    conn.send(i + "\n")
	  else: 
	     for i in currFriends_E:
                    conn.send(i + "\n")
     else:
            continue 

while 1:
    #wait to accept a connection
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    start_new_thread(clientthread ,(conn, addr))
    connList.append(conn)
    addrList.append(addr)
s.close()
