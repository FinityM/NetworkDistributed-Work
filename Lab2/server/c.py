
# Echo client program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50007          # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:

    print("type input:")
    text = input()

    # when we send data to the server, we are using a colon
    # at the end of a sentence to mark the end of the current sentence
    # later when the input comes back, we will then be breaking the input
    # into individual parts using the colon : to separate the lines
    s.sendall((text + ":").encode())

    data = s.recv(80000)

    print("Response:" + str(data))
    
s.close()
