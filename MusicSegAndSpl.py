from pydub import AudioSegment
import pydub
from pydub.silence import split_on_silence
import sys
import os

def MusicSegment(filename, seconds = 30):
    #audio_segment = AudioSegment.from_file("F:/MIProject/Never.mp3")
    audio_segment = AudioSegment.from_file(filename)

    total = int(audio_segment.duration_seconds / seconds)
    for i in range(total):
        filestr = "chunk" + str(i) + ".mp3"
        audio_segment[i * seconds * 1000 : (i + 1) * seconds * 1000].export(filestr)
    filestr = "chunk" + str(total) + ".mp3"
    audio_segment[total * seconds * 1000:].export(filestr)