from flask import Flask
from flask import request
from flask import send_from_directory
from flask import make_response
import json
import os
import lucidsonicdreams

app = Flask(__name__)
isReceiveParameterData = False

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/ParameterData', methods = ['POST'])
def VideoDataReceive():
    data = request.get_data()
    data = json.loads(data)
    filename = data['filename']
    style = data['style']
    pulse_react = data['pulse_react']
    motion_react = data['motion_react']
    contrast_strength = data['contrast_strength']
    isReceiveParameterData = True
    print("filename is : " + filename)
    print("style is : " + style)
    print("pulse_react is : " + str(pulse_react))
    print("motion_react is : " + str(motion_react))
    print("contrast_strength is : " + str(contrast_strength))
    return 'Parameter is Here !!!'

@app.route('/MusicData', methods = ['POST'])
def MusicDataReceive():

    if 'file' not in request.files:
        return('No file part')

    file = request.files['file']
    if file is None:
        return('No such file')
    else:
        file_name = file.filename
        suffix = os.path.splitext(file_name)[-1]  # 获取文件后缀（扩展名）
        basePath = os.path.dirname(__file__)
        file.save(basePath + '/'+ file_name)  # 保存文件
        if isReceiveParameterData:
            lucidsonicdreams.run()
        return file.filename

@app.route('/VideoReturn/<file_name>', methods = ['GET'])
def videoSend(file_name):
    if request.method == 'GET':
        #return send_from_directory(os.path.dirname(__file__), "Always.mp3", as_attachment=True)
        return send_from_directory(os.path.dirname(__file__), file_name, as_attachment=True)

def WriteInFile(string):
    f = open('StringMp3.mp3', 'w')
    f.write(string)
    f.close()
    return 'Write is Here!!!'

if __name__ == '__main__':
    #WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run()