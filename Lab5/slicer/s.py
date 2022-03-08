import os
import socket
import threading
import hashlib

HOST = '127.0.0.1'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

# This is the buffer string
# when input comes in from a client it is added
# into the buffer string to be relayed later
# to different clients that have connected
# Each message in the buffer is separated by a colon :
buffer = ""


# custom say hello command
def sayHello():
    print("----> The hello function was called")


'''
List all songs in the list 
at the top of the program
'''

def listAllSongs():
    global listAllSongs

    for oneSong in listAllSongs:
        print(oneSong)

# sample parser function. The job of this function is to take some input
# data and search to see if a command is present in the text. If it finds a 
# command it will then need to extract the command.
def parseInput(data, con):
    global listOfSongs
    listOfSongs = list()

    print("parsing...")
    print(str(data))

    # Checking for commands 
    if "<hello>" in data:
        print("command in data..")
        # formatted= strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        con.send(str("hello there").encode())

    elif "<hash" in str(data):
        # Declare the hash algorithm
        m = hashlib.sha256()

        parts = str(data).split('-')

        filename = parts[1] # this contains the filename
        cleanedName = filename[0:-3] # chop off the last 3

        # read in the file
        file = open(cleanedName, 'rb')
        content = file.read()

        # get the hash
        m.update(content)
        res = m.digest()

        # send back the result
        con.send(res)

    elif "<findall>" in str(data):
        # list all the files in the directory
        # make sure they are mp3 files
        files = os.listdir(path=".")

        cleaned = list()
        for oneFile in files:
            if ".mp3" in oneFile:
                print(oneFile)
                cleaned.append(oneFile)


        con.send(str(cleaned).encode())

    elif "<addsong" in data:  # <addsong-britney.mp3-localhost>
        print("adding a song")
        parts = data.split("-")
        print(parts[0])
        print(parts[1])  # has the song name

        whoHasIt = parts[2]
        print(whoHasIt[0:-3])

        listOfSongs.append(parts[1])  # store the song name

        # receive the file and make it
        f = open('c0.mp3', 'wb')

        partOfFile = con.recv(1000)

        while partOfFile:
            f.write(partOfFile)
            partOfFile = con.recv(1000)

        f.close()

    elif "<listall>" in str(data):
        listAllSongs()

    elif "<get" in str(data):
        print("getting a file")
        parts = str(data).split('-')
        filename = parts[1] # just get the filename
        print("filename: " + str(filename)) # print the filename
        print("sending the file")

        cleanedName = filename[0:-3] # take the last 3 chars off
        print(cleanedName) #just to see the filename cleaned

        #open the file
        f = open(cleanedName, 'rb')
        content = f.read()
        # send the bytes
        con.sendall(content)
        f.close()

        print("send the file")



# we make a new thread is started from an incoming connection
# the manageConnection funnction is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.

def manageConnection(conn, addr):
    global buffer
    print('Connected by', addr)

    data = conn.recv(1024)

    parseInput(str(data), conn)  # Calling the parser, passing the connection

    print("rec:" + str(data))
    buffer += str(data)

    # conn.send(str(buffer))
    # conn.close()

while 1:
    s.listen(1)
    conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args=(conn, addr))

    t.start()
