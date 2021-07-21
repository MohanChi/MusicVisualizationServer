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
        self.pulse_react = 0
        self.motion_react = 0
        self.contrast_strength = 0
        self.musicname = ''
        self.folder = ''


isReceiveParameterData = False
cvData = CreateVideoData()


def Generate(song, style, outfile, pulse, motion, contrast):
    L = lucidsonicdreams.LucidSonicDream(song = song, style = style)
    L.hallucinate(file_name = outfile, pulse_react = pulse, motion_react = motion, contrast_strength= contrast)

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
    cvData.pulse_react = data['pulse_react']
    cvData.motion_react = data['motion_react']
    cvData.contrast_strength = data['contrast_strength']
    global isReceiveParameterData
    isReceiveParameterData = True
    folder = os.getcwd() + '\\Output\\' + cvData.filename
    if not os.path.exists(folder):
        os.mkdir(folder)
    cvData.folder = folder
    print("filename is : " + cvData.filename)
    print("style is : " + cvData.style)
    print("pulse_react is : " + str(cvData.pulse_react))
    print("motion_react is : " + str(cvData.motion_react))
    print("contrast_strength is : " + str(cvData.contrast_strength))
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
                pulse=cvData.pulse_react,
                motion=cvData.motion_react,
                contrast=cvData.contrast_strength)
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
