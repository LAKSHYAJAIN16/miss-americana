import subprocess
import os

"""
to_wav takes in the path and name of the mp3 file.
It then uses ffmpeg to convert it to a .wav file which will be used to play the audio
"""
def to_wav(mp3):
    subprocess.call(['ffmpeg','-i',mp3[0],mp3[1]+".wav"])
    
    # Remove the mp3 file
    os.remove(mp3[0])
    return mp3[1]+".wav"