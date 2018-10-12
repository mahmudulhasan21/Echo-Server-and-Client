import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address
	
	data = connection.recv(50)
        print >>sys.stderr, 'received "%s"' % data
	connection.sendall(data)
	check_start = 0

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(50)
            print >>sys.stderr, 'received "%s"' % data
	    start = 'begin'
	    end = 'end'
	    close = 'close'

	    if data == close:
		break

	    if data == start:
		check_start = 1
            if data != end:
		if check_start == 1:
                    print >>sys.stderr, 'sending data back to the client'
                    connection.sendall(data)
		if check_start == 0:
                    print >>sys.stderr, 'sending feedback to the client'
                    connection.sendall("_")
            else:
		if check_start == 1:
                    print >>sys.stderr, 'no more data from', client_address
                    check_start = 0
		if check_start == 0:
                    print >>sys.stderr, 'sending feedback to the client'
                    connection.sendall("_")
            
    finally:
        # Clean up the connection
        connection.close()
