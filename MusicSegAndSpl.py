from pydub import AudioSegment
from moviepy.editor import VideoFileClip, concatenate_videoclips
from concurrent.futures import ThreadPoolExecutor
import lucidsonicdreams
import multiprocessing

def MusicSegmentBySecond(filename, seconds=15):
    # audio_segment = AudioSegment.from_file("F:/MIProject/Never.mp3")
    audio_segment = AudioSegment.from_mp3(filename)
    total = int(audio_segment.duration_seconds / seconds)
    for i in range(total):
        filestr = "chunk" + str(i) + ".mp3"
        audio_segment[i * seconds * 1000: (i + 1) * seconds * 1000].export(filestr)
    filestr = "chunk" + str(total) + ".mp3"
    audio_segment[total * seconds * 1000:].export(filestr)

def MusicSegmentByProcess(filename, folder, cpu_count=3):
    audio_segment = AudioSegment.from_mp3(filename)
    ms_seconds = int(audio_segment.duration_seconds / cpu_count) * 1000
    filestr0 = folder + "\\chunk0.mp3"
    filestr1 = folder + "\\chunk1.mp3"
    filestr2 = folder + "\\chunk2.mp3"
    audio_segment[: ms_seconds].export(filestr0)
    audio_segment[ms_seconds: ms_seconds * 2].export(filestr1)
    audio_segment[ms_seconds * 2:].export(filestr2)

def threadProcess(i):
    print(i)
    l = lucidsonicdreams.LucidSonicDream(song="chunk" + str(i) + ".mp3", style="cat.pkl")
    print(str(i) + " is here")
    l.hallucinate(file_name=str(i) + ".mp4")
    print(str(i) + " is finished")

def MultiThreadProcess_0():
    with ThreadPoolExecutor(max_workers=8) as executor:
        [executor.submit(threadProcess, param) for param in range(3)]


def MultiThreadProcess_1(index):
    print(multiprocessing.cpu_count())
    pool = multiprocessing.Pool(index) #multiprocessing.cpu_count()
    for i in range(index):
        pool.apply_async(threadProcess, (i, ))
    pool.close()
    pool.join()
    print("close!")

def ConcatenateVideos(filename0, filename1, filename2, outputfile):
    vid0 = VideoFileClip(filename0)
    vid1 = VideoFileClip(filename1)
    vid2 = VideoFileClip(filename2)
    final = concatenate_videoclips([vid0, vid1, vid2])
    final.write_videofile(outputfile)
