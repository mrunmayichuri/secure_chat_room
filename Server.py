#!/usr/bin/env python
#Mrunmayi Churi
#Reference: http://www.binarytides.com/code-chat-application-server-client-sockets-python/

#Chat room Server
 
import socket
import select

#Broadcast messages to all the users in the chat room
def broadcast (sock, message):
    #Broadcasting messages to everyone except the Server socket and the user who sent the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                #Error handling of broken socket connections, for e.g. Keyboard interrupt
                socket.close()
                CONNECTION_LIST.remove(socket)

#Main function 
if __name__ == "__main__":
     
    #List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 4444
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    #Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Welcome to the chat server on port " + str(PORT)
 
    while 1:
        #Monitoring client sockets through the select function
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #Code for a new connection
            if sock == server_socket:
                # Handle the case in which there is a new connection received through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "(%s, %s) connected" % addr
                 
            #Incoming data from a client 
            else:
                try:
                    #Sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast(sock, data)                                
                except:
                    broadcast(sock, "(%s, %s) is offline" % addr)
                    print "(%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
