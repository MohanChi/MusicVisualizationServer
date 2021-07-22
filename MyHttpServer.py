from flask import Flask
from flask import request
from flask import send_from_directory
import json
import os
import lucidsonicdreams

app = Flask(__name__)

class CreateVideoData:
    def __init__(self):
        self.filename = ''
        self.style = ''
        self.speed_fpm = 0
        self.pulse_react = 0
        self.motion_react = 0
        self.motion_randomness = 0
        self.contrast_strength = 0
        self.class_pitch_react = 0
        self.flash_strength = 0
        self.pulse_percussive = True
        self.pulse_harmonic= True
        self.motion_percussive= True
        self.motion_harmonic= True
        self.flash_percussive= True
        self.contrast_percussive= True
        self.resolution = 0
        self.start = 0
        self.fps = 0
        self.musicname = ''
        self.folder = ''


isReceiveParameterData = False
cvData = CreateVideoData()


def Generate(song, style, outfile, speed_fpm,
             pulse_react, motion_react,
             motion_randomness, contrast_strength,
             class_pitch_react, flash_strength,
             pulse_percussive, pulse_harmonic,
             motion_percussive, motion_harmonic,
             flash_percussive, contrast_percussive,
             resolution, start, fps):
    L = lucidsonicdreams.LucidSonicDream(song=song, style=style)
    L.hallucinate(file_name=outfile, speed_fpm=speed_fpm,
                  pulse_react=pulse_react, motion_react=motion_react,
                  motion_randomness=motion_randomness, contrast_strength=contrast_strength,
                  class_pitch_react=class_pitch_react, flash_strength=flash_strength,
                  pulse_percussive=pulse_percussive, pulse_harmonic=pulse_harmonic,
                  motion_percussive=motion_percussive, motion_harmonic=motion_harmonic,
                  flash_percussive=flash_percussive,contrast_percussive=contrast_percussive,
                  resolution=resolution, start=start, fps=fps)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/ParameterData', methods = ['POST'])
def VideoDataReceive():
    data = request.get_data()
    data = json.loads(data)
    cvData.__init__()
    cvData.filename = data['filename']
    cvData.style = data['style']
    cvData.speed_fpm = data['speed_fpm']
    cvData.pulse_react = data['pulse_react']
    cvData.motion_react = data['motion_react']
    cvData.motion_randomness = data['motion_randomness']
    cvData.contrast_strength = data['contrast_strength']
    cvData.class_pitch_react = data['class_pitch_react']
    cvData.flash_strength = data['flash_strength']
    cvData.pulse_percussive = data['pulse_percussive']
    cvData.pulse_harmonic = data['pulse_harmonic']
    cvData.motion_percussive = data['motion_percussive']
    cvData.motion_harmonic = data['motion_harmonic']
    cvData.flash_percussive = data['flash_percussive']
    cvData.contrast_percussive = data['contrast_percussive']
    cvData.resolution = data['resolution']
    cvData.start = data['start']
    cvData.fps = data['fps']
    global isReceiveParameterData
    isReceiveParameterData = True
    folder = os.getcwd() + '\\Output\\' + cvData.filename
    if not os.path.exists(folder):
        os.mkdir(folder)
    cvData.folder = folder
    print("filename is : " + cvData.filename)
    print("style is : " + cvData.style)
    print("speed_fpm is : " + str(cvData.speed_fpm))
    print("pulse_react is : " + str(cvData.pulse_react))
    print("motion_react is : " + str(cvData.motion_react))
    print("motion_randomness is : " + str(cvData.motion_randomness))
    print("contrast_strength is : " + str(cvData.contrast_strength))
    print("class_pitch_react is : " + str(cvData.class_pitch_react))
    print("flash_strength is : " + str(cvData.flash_strength))
    print("pulse_percussive is : " + str(cvData.pulse_percussive))
    print("pulse_harmonic is : " + str(cvData.pulse_harmonic))
    print("motion_percussive is : " + str(cvData.motion_percussive))
    print("motion_harmonic is : " + str(cvData.motion_harmonic))
    print("flash_percussive is : " + str(cvData.flash_percussive))
    print("contrast_percussive is : " + str(cvData.contrast_percussive))
    print("resolution is : " + str(cvData.resolution))
    print("start is : " + str(cvData.start))
    print("fps is : " + str(cvData.fps))
    return 'Parameter is Here !!!'

@app.route('/MusicData', methods = ['POST'])
def MusicDataReceive():
    if 'file' not in request.files:
        return('No file part')

    file = request.files['file']

    if file is None:
        return('No such file')
    else:
        cvData.musicname = file.filename
        if not os.path.exists(cvData.folder):
            return 'No such folder and music parameter'
        file.save(cvData.folder + '\\' + cvData.musicname)  # 保存文件
        global isReceiveParameterData
        if isReceiveParameterData:
            Generate(
                song=cvData.folder + '\\' + cvData.musicname,
                style=cvData.style + '.pkl',
                outfile=cvData.folder + '\\' + cvData.filename + '.mp4',
                speed_fpm=cvData.speed_fpm, pulse_react=cvData.pulse_react, motion_react=cvData.motion_react,
                motion_randomness=cvData.motion_randomness, contrast_strength=cvData.contrast_strength,
                class_pitch_react=cvData.class_pitch_react, flash_strength=cvData.flash_strength,
                pulse_percussive=cvData.pulse_percussive, pulse_harmonic=cvData.pulse_harmonic,
                motion_percussive=cvData.motion_percussive, motion_harmonic=cvData.motion_harmonic,
                flash_percussive=cvData.flash_percussive, contrast_percussive=cvData.contrast_percussive,
                resolution=cvData.resolution, start=cvData.start, fps=cvData.fps)
        isReceiveParameterData = False
        return file.filename + ' is here!!!'

@app.route('/VideoReturn/<file_name>', methods = ['GET'])
def videoSend(file_name):
    if request.method == 'GET':
        #return send_from_directory(os.path.dirname(__file__), "Always.mp3", as_attachment=True)
        return send_from_directory(cvData.folder, file_name + '.mp4', as_attachment=True)

def WriteInFile(string):
    f = open('StringMp3.mp3', 'w')
    f.write(string)
    f.close()
    return 'Write is Here!!!'
