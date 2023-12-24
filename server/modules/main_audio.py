import os
from youtubesearchpython import VideosSearch
from pytube import YouTube

def extract(name, artist, id):
    # Get the Link of our song
    videosSearch = VideosSearch(name + " by " + artist + " official audio", limit = 1)
    link = videosSearch.result()["result"][0]["link"]
    
    # Download the Mp3
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first() 
    
    # Download to hard drive
    out_file = video.download(r"C:\Users\USER\Desktop\CS Mr. Penney Stuff\Music Visualizer\server\buffer")
    base, ext = os.path.splitext(out_file) 
    new_file = id + '.mp3'
    os.rename(out_file, new_file)
    
    # Get the path of the file
    path = new_file
    return path