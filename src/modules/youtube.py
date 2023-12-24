import soundfile as sf
from utils.mp3 import to_mp3
from utils.wav import to_wav
from pydub import AudioSegment

def youtubeThread(name, artist):
    # YouTube Thread
    mp3 = to_mp3(name, artist)
    wav = to_wav(mp3)

    # Retrieve the data from the wav file
    data, samplerate = sf.read(wav)
    
    Fs = samplerate  # the sample rate
    print((1 / Fs)*1000)
    
    # Play Song
    song = AudioSegment.from_wav(wav)
    return [song, wav]