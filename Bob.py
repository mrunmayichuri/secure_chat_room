#!/usr/bin/env python
#Mrunmayi Churi
#Reference: http://www.binarytides.com/code-chat-application-server-client-sockets-python/
#Reference: https://pypi.python.org/pypi/pycrypto

#Client - Bob

import socket
import select
import string
import sys
from Crypto.Cipher import AES

#Encryption function
def encryption(msg):
    aes_obj = AES.new('TheK3yI$allyourb@se@r3b3longtous', AES.MODE_CBC, 'ThisIsTheIV@666!')    
    mod = len(msg) % 16
    pad = 16 - mod
    #Padding
    if pad == 16:
        ciphertext = aes_obj.encrypt(msg)
        return ciphertext
    else:
        msg += ' ' * pad
	ciphertext = aes_obj.encrypt(msg)
        return ciphertext

#Decryption function
def decryption(ciphertext):
    aes_obj2 = AES.new('TheK3yI$allyourb@se@r3b3longtous', AES.MODE_CBC, 'ThisIsTheIV@666!')
    message = aes_obj2.decrypt(data)
    message = message.strip(' ')
    return message

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
    sys.stdout.write('\nBob: ')
    sys.stdout.flush() 					#Write everything in the buffer to the terminal
     
    while 1:
        socket_list = [sys.stdin, s]
         
        #Monitoring using the select function
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #Incoming data from the Server           
	    if sock == s:
                data = sock.recv(4096)			#Receiving buffer size is 4096
		try:
                    plain_text = decryption(data)	#Decryption of the incoming data
                except ValueError:
                    plain_text = data
                if not data :
                    print '\nDisconnected'
                    sys.exit()
                else :
                    sys.stdout.write('\n' + plain_text)
	            sys.stdout.flush()        
             
            #Text input from the user
            else : 
                msg = 'Bob:' + sys.stdin.readline()
		cipher_text = encryption(msg)
                s.send(cipher_text)
