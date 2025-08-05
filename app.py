import subprocess
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import pyttsx3
import speech_recognition as sr
from pygame import mixer
from fuzzywuzzy import fuzz

app = Flask(__name__)

# Folder paths and global variables
SONG_FOLDER_PATH = r"C:\Users\Harshith\OneDrive\Desktop\songs"
LYRICS_FILE_PATH = r"C:\Users\Harshith\OneDrive\Desktop\songs\song.txt"
current_song_path = None
r = sr.Recognizer()
mixer.init()

# Helper functions
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def get_audio():
    mixer.music.pause()
    try:
        with sr.Microphone() as source:
            speak("Listening for lyrics...")
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
        return r.recognize_google(audio).lower()
    except Exception as e:
        print(f"Error capturing audio: {e}")
        return ""

def load_songs_and_lyrics(file_path):
    songs_db = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        current_song = None
        current_lyrics = ""
        for line in lines:
            line = line.strip()
            if line.startswith("Song:"):
                if current_song:
                    songs_db.append({"song": current_song, "lyrics": current_lyrics.strip()})
                current_song = line.replace("Song:", "").strip()
                current_lyrics = ""
            elif current_song:
                current_lyrics += " " + line

        if current_song:
            songs_db.append({"song": current_song, "lyrics": current_lyrics.strip()})
    except Exception as e:
        print(f"Error reading lyrics file: {e}")
    return songs_db

def search_and_play_song(lyric_input):
    try:
        if lyric_input:
            songs_db = load_songs_and_lyrics(LYRICS_FILE_PATH)
            for song_entry in songs_db:
                lyrics = song_entry['lyrics']
                song_title = song_entry['song']
                similarity = fuzz.token_set_ratio(lyric_input, lyrics)
                if similarity >= 75:
                    global current_song_path
                    current_song_path = os.path.join(SONG_FOLDER_PATH, song_title + ".wav")
                    mixer.music.load(current_song_path)
                    mixer.music.play()
                    return song_title
        return None
    except Exception as e:
        print(f"Error in search_and_play_song: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next', methods=['GET', 'POST'])
def index2():
    return render_template('index2.html')

@app.route('/index3')
def index3():
    song_title = request.args.get('songTitle', 'Unknown Song')
    return render_template('index3.html', song_title=song_title)

@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        lyric_input = get_audio()
        if lyric_input:
            song_title = search_and_play_song(lyric_input)
            if song_title:
                return jsonify({'message': f"Playing {song_title}", 'song_title': song_title})
            else:
                return jsonify({'message': "No matching song found", 'song_title': None})
        else:
            return jsonify({'message': "No audio input detected", 'song_title': None})
    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({'message': "Error occurred while processing audio.", 'song_title': None})

@app.route('/extract-lyrics', methods=['POST'])
def extract_lyrics():
    try:
        lyrics_output = subprocess.check_output(['python', 'lyrics.py'], text=True)
        return jsonify({'lyrics_output': lyrics_output})
    except Exception as e:
        print(f"Error extracting lyrics: {e}")
        return jsonify({'lyrics_output': "Error occurred while extracting lyrics."})

@app.route('/toggle-play', methods=['POST'])
def toggle_play():
    try:
        if mixer.music.get_busy():
            mixer.music.pause()
            return jsonify({'message': "Music paused"})
        else:
            mixer.music.unpause()
            return jsonify({'message': "Music resumed"})
    except Exception as e:
        print(f"Error toggling playback: {e}")
        return jsonify({'message': "Error occurred while toggling playback."})

@app.route('/restart')
def restart():
    mixer.music.pause()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
