from utils.mp3 import to_mp3
from utils.wav import to_wav
from pydub import AudioSegment

"""
The youTube Thread simply calls the other two helper functions
"""
def youtubeThread(name, artist):
    # YouTube Thread
    mp3 = to_mp3(name, artist)
    wav = to_wav(mp3)
    
    # Create segment
    song = AudioSegment.from_wav(wav)
    return [song, wav]