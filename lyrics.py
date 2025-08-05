import os
import speech_recognition as sr
from pydub import AudioSegment

# Folder containing .wav files
SONG_FOLDER_PATH = r"C:\Users\Harshith\OneDrive\Desktop\songs"
# File to save extracted lyrics
LYRICS_FILE_PATH = r"C:\Users\Harshith\OneDrive\Desktop\songs\song.txt"

# Initialize the recognizer
r = sr.Recognizer()

def extract_and_store_lyrics(input_folder, lyrics_file):
    """
    Extract lyrics from .wav files in the input folder and save them to the lyrics file.
    """
    processed_titles = set()

    # Read already processed song titles to avoid duplication
    if os.path.exists(lyrics_file):
        with open(lyrics_file, "r") as file:
            for line in file:
                if line.startswith("Song:"):
                    processed_titles.add(line.strip().replace("Song: ", ""))

    # Open lyrics file in append mode
    with open(lyrics_file, "a") as output:
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".wav"):
                song_title = os.path.splitext(file_name)[0]

                # Skip if the song has already been processed
                if song_title in processed_titles:
                    print(f"Skipping {song_title} as it has already been processed.")
                    continue

                wav_file = os.path.join(input_folder, file_name)

                try:
                    # Convert the audio file to a standard format
                    audio = AudioSegment.from_wav(wav_file)
                    audio = audio.set_channels(1).set_sample_width(2).set_frame_rate(16000)
                    audio.export(wav_file, format="wav")

                    # Process the audio file
                    with sr.AudioFile(wav_file) as source:
                        print(f"Processing audio: {file_name}...")
                        audio_text = r.record(source)

                    # Recognize speech using Google Web Speech API
                    try:
                        recognized_text = r.recognize_google(audio_text)
                        # Write the song title and recognized lyrics to the text file
                        output.write(f"Song: {song_title}\n")
                        output.write(f"Recognized Text: {recognized_text}\n\n")
                        print(f"Recognized text for {song_title}: {recognized_text}")
                    except sr.UnknownValueError:
                        output.write(f"Song: {song_title}\n")
                        output.write("Error: Could not understand the audio.\n\n")
                        print(f"Could not understand the audio in {song_title}.")
                    except sr.RequestError as e:
                        output.write(f"Song: {song_title}\n")
                        output.write(f"Error: Could not request results from Google Speech Recognition service; {e}\n\n")
                        print(f"Error with Google Speech Recognition for {song_title}: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred while processing {wav_file}: {e}")

# Run the function
extract_and_store_lyrics(SONG_FOLDER_PATH, LYRICS_FILE_PATH)
