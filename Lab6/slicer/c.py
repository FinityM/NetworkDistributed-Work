# Echo client program
import socket
import glob
import os

from pydub import AudioSegment
from pydub import AudioSegment as Convert
from pydub.utils import make_chunks

HOST = '127.0.0.1'  # The remote host
PORT = 50007  # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print("enter a username")
username = input()

print("Welcome: " + username)

while True:

    print("type input:")
    text = input()

    # when we send data to the server, we are using a colon
    # at the end of a sentence to mark the end of the current sentence
    # later when the input comes back, we will then be breaking the input
    # into individual parts using the colon : to separate the lines
    s.sendall((text + ":").encode())

    # data = s.recv(80000)

    if "<addsong" in text:
        # read file and send it
        f = open('chunk0.mp3', 'rb')
        content = f.read()
        s.sendall(content)
        f.close()

    elif "<findall>" in text:
        answer = s.recv(1000)
        print(answer)

    elif "<hash" in text:
        answer = s.recv(1000)
        print(answer)

    elif "<get" in text:
        parts = text.split("-")

        print(parts[0]) # command name

        print(parts[1]) # the file name

        f = open('c0part.mp3', 'wb')

        partOfFile = s.recv(1000)

        while partOfFile:
            f.write(partOfFile)
            partOfFile = s.recv(1000)
            print(partOfFile)

    elif "<segment>" in text:
        print("please enter a file name")

        file_name = input()

        myaudio = AudioSegment.from_file(file_name, "mp3")
        chunk_length_ms = 1000 * 30  # pydub calculates in millisec
        chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks of 30 seconds

        # Export all of the individual chunks as mp3 files

        for i, chunk in enumerate(chunks):
            chunk_name = "chunk{0}.mp3".format(i)
            chunk.export(chunk_name, format="mp3")

    elif "<convert>" in text:
        print("Enter a the filename to convert to a wav file")

        filename = input()

        songs = glob.glob(filename)

        # print names of files being converted
        print("----------------------------------------\nFiles being converted:\n")

        for song in songs:
            print(song)

        print("----------------------------------------\n")

        # loop converting files and showing progress of each
        for song in songs:
            song_name = song[:-4]
            print("Converting", song_name)

            destination = song_name + ".wav"

            song = Convert.from_file(song, format="mp3")
            song.export(destination, format="wav")

            print("Done\n")

        # display completion and where files are located
        working_dir = os.getcwd()
        print("All files have been converted and can be found in", working_dir)

    elif "<deletefile>" in text:
        print("Enter a file in the directory to delete")

        fileToDelete = input()

        if os.path.exists(fileToDelete):
            os.remove(fileToDelete)
        else:
            print("File does not exist")

    elif "<checkport>" in text:
        answer = s.recv(1000)
        print(answer)

    # print("Response:" + str(data))

s.close()
