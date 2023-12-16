import os
import subprocess
import paho.mqtt.client as mqtt
from youtubesearchpython import VideosSearch
from pytube import YouTube
from taylorAudVis import data_main
    
def to_mp3(name, artist):
    # Get the Link of our song
    videosSearch = VideosSearch(name + " by " + artist + " official audio", limit = 1)
    link = videosSearch.result()["result"][0]["link"]
    
    # Download the Mp3
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first() 
    out_file = video.download()
    base, ext = os.path.splitext(out_file) 
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    
    # Get the path of the file
    path = new_file
    return [path, base]

def to_wav(mp3):
    subprocess.call(['ffmpeg','-i',mp3[0],mp3[1]+".wav"])
    return mp3[1]+".wav"

n = input("Enter the name of the Song: ")
artist = input("Enter the name of the Artist : ")
mp3 = to_mp3(n, artist)
wav = to_wav(mp3)

# MQTT STUFF
client = mqtt.Client()
client.username_pw_set("gkvpckep", "yGbZQKc8MAma")
client.connect("awesome-fisher.cloudmqtt.com", 1883, 60)

# Now, we Pass it to the audVis module
data_main(wav, client)