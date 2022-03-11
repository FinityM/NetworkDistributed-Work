# import glob
# import os
#
# from pydub import AudioSegment as convert
#
# # find all files that end with m4a
# print("Type in name of file")
# filename = input()
#
# songs = glob.glob(filename)
#
# # print names of files being converted
# print("----------------------------------------\nFiles being converted:\n")
#
# for song in songs:
#     print(song)
#
# print("----------------------------------------\n")
#
# # loop converting files and showing progress of each
# for song in songs:
#     song_name = song[:-4]
#     print("Converting", song_name)
#
#     destination = song_name + ".wav"
#
#     song = convert.from_file(song, format="mp3")
#     song.export(destination, format="wav")
#
#     print("Done\n")
#
# # display completion and where files are located
# working_dir = os.getcwd()
# print("All files have been converted and can be found in", working_dir)
