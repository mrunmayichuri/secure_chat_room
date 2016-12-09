#!/usr/bin/env python
#Mrunmayi Churi
#Reference: http://www.binarytides.com/code-chat-application-server-client-sockets-python/

#Client(Attacker) - Trudy

import socket
import select
import string
import sys
 
#Main function
if __name__ == "__main__":
     
    if(len(sys.argv) < 3) :
        print 'Enter the correct port number'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
     
    #Connection to the Server
    try :
        s.connect((host, port))
    except :
        print 'Connection error: Unable to connect'
        sys.exit()

    #Initialization of the chat room server     
    print '\nWelcome to the Chat Room Server. Start sending messages'
    sys.stdout.write('\nTrudy: ')
    sys.stdout.flush() 					#Write everything in the buffer to the terminal
     
    while 1:
        socket_list = [sys.stdin, s]
         
        #Monitoring using the select function
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #Incoming data from the Server
            if sock == s:
                data = sock.recv(4096)			#Receiving buffer size is 4096
                if not data :
                    print '\nDisconnected'
                    sys.exit()
                else :
                    sys.stdout.write('\n' + data)
	            sys.stdout.flush() 
             
            #Text input from the user
            else :
                msg = '[Untrusted]: ' + sys.stdin.readline()
                s.send(msg)
