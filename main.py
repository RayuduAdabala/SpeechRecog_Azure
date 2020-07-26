import pyaudio
import wave
import azure.cognitiveservices.speech as speechsdk
from ASR import SpeechRecog
import time
from flask import Flask, request, jsonify, render_template, send_file

app = Flask(__name__) #Initialize the flask App
@app.route('/')
def home():
    return render_template('index.html')
#
# the file name output you want to record into
@app.route('/record',methods=['POST'])

def recorder():
    filename = "recorded.wav"
# set the chunk size of 1024 samples
    chunk = 1024
# sample format
    FORMAT = pyaudio.paInt16
# mono, change to 2 if you want stereo
    channels = 1
# 44100 samples per second
    sample_rate = 44100
    record_seconds = 15
# initialize PyAudio object
    p = pyaudio.PyAudio()
# open stream object as input & output
    stream = p.open(format=FORMAT,
                channels=channels,
                rate=sample_rate,
                input=True,
                output=True,
                frames_per_buffer=chunk)
    frames = []
    print("Recording...")
    # render_template('index.html', Recording_text='Speak : Recording..')
    try:
        for i in range(int(44100 / chunk * record_seconds)):
            data = stream.read(chunk)
    # if you want to hear your voice while recording
    # stream.write(data)
            frames.append(data)
    except KeyboardInterrupt:
        print("Stopped")
    print("Finished recording.")
# stop and close stream
    stream.stop_stream()
    stream.close()
# terminate pyaudio object
    p.terminate()
# save audio file
# open the file in 'write bytes' mode
    wf = wave.open(filename, "wb")
# set the channels
    wf.setnchannels(channels)
# set the sample formathttps://github.com/addpipe/simple-web-audio-recorder-demo
    wf.setsampwidth(p.get_sample_size(FORMAT))
# set the sample rate
    wf.setframerate(sample_rate)
# write the frames as bytes
    wf.writeframes(b"".join(frames))
# close the file
    wf.close()
    # render_template('index.html', Processing_text='Speak : Processing..')
    SpeechRecog()
    return render_template('Download.html', Voice_Notes='Your voice notes')
def stop():
    a=True
    return a
@app.route('/download')
def download_file():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	# path = "simple.docx"
	path = "your_file.txt"
	return send_file(path, mimetype="text/plain", as_attachment=True)

if __name__ == "__main__":
    app.run()