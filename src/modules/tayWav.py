import subprocess

"""
to_wav takes in the path and name of the mp3 file.
It then uses ffmpeg to convert it to a .wav file which will be used to play ot
"""
def to_wav(mp3):
    subprocess.call(['ffmpeg','-i',mp3[0],mp3[1]+".wav"])
    return mp3[1]+".wav"