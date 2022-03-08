import os

files = os.listdir(path=".")

for oneFile in files:
    if ".mp3" in oneFile:
        print(oneFile)