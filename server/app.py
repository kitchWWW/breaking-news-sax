print("hello?")
from waitress import serve
print("hello? 1")
from flask import Flask, request, send_file, send_from_directory
print("hello? 2")
from flask_cors import CORS
print("hello? 3")
import time
import threading
import os
print("hello? 4")
# import collage  # Import the processing module
# print("hello? 5")

app = Flask(__name__)
CORS(app)

def current_milli_time():
    return str(round(time.time() * 1000))

def testIt(arg):
    print("hello!!!!")

def run_process(filename):
    # Call the process function from processing.py in a separate thread
    thread = threading.Thread(target=collage.doForFile, args=(filename,))
    thread.start()

# @app.route('/breaking-news-sax/test')
# def testFunction():
#     return "hello, world"
#     # return send_from_directory(os.getcwd(), filename)

@app.route('/breaking-news-sax/<path:filename>')
def serve_static_files(filename):
    print("trying?")
    return send_from_directory(os.getcwd(), filename)

@app.route('/breaking-news-sax/listAll')
def listAllFiles():
    print("trying to create the thing!!!!!!")
    return 1

@app.route('/breaking-news-sax/create', methods=['POST'])
def createNewAudio():
    print("trying to create the thing!!!!!!")
    return 1

@app.route('/breaking-news-sax/clear', methods=['POST'])
def createNewAudio():
    print("trying to get rid of everything!!!!!!")
    return 1

@app.route('/breaking-news-sax/upload_audio', methods=['POST'])
def upload_audio():
    print("yeeet")
    if 'audio' not in request.files:
        return 'No audio file provided', 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return 'No selected file', 400

    file_prefix = current_milli_time()
    file_name = 'uploads/'+file_prefix+'_in.ogg'
    audio_file.save(file_name)  # Save the audio file locally

    return file_prefix, 200

if __name__ == '__main__':
    print("running!")
    serve(app, host="0.0.0.0", port=3010)
