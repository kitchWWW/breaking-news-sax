import os
import threading
import time
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from waitress import serve

def current_milli_time():
    return str(round(time.time() * 1000))

def append_to_filelist(file_name):
    with open('filenames.txt', 'a') as file:
        file.write(file_name + '\n')

def read_filelist():
    if not os.path.exists('filenames.txt'):
        return []
    with open('filenames.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

def clear_filelist():
    if os.path.exists('filenames.txt'):
        os.remove('filenames.txt')

app = Flask(__name__)
CORS(app)

@app.route('/breaking-news-sax/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(os.getcwd(), filename)

@app.route('/breaking-news-sax/list_all')
def listAllFiles():
    print("Listing all files.")
    file_list = read_filelist()
    return {"files": file_list}, 200

@app.route('/breaking-news-sax/clear', methods=['POST'])
def clearAllAudio():
    print("Clearing all files.")
    file_list = read_filelist()

    # Delete the files listed in filenames.txt
    for file_name in file_list:
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
        except Exception as e:
            print(f"Failed to delete {file_name}: {e}")

    # Clear the filenames.txt file
    clear_filelist()

    return {"message": "All files cleared."}, 200

@app.route('/breaking-news-sax/upload_audio', methods=['POST'])
def upload_audio():
    print("Uploading audio.")
    if 'audio' not in request.files:
        return 'No audio file provided', 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return 'No selected file', 400

    file_prefix = current_milli_time()
    upload_dir = 'uploads'
    os.makedirs(upload_dir, exist_ok=True)  # Ensure the uploads directory exists
    file_name = os.path.join(upload_dir, f'{file_prefix}_in.ogg')

    audio_file.save(file_name)  # Save the audio file locally

    # Append the filename to the list
    append_to_filelist(file_name)

    return {"file_prefix": file_prefix}, 200

if __name__ == '__main__':
    print("Running!")
    serve(app, host="0.0.0.0", port=3011)
