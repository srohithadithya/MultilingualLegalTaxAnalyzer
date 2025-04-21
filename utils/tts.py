import pyttsx3
import os

def text_to_speech(text, language, filename):
    """
    Converts text to speech and saves the output audio file.
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)

    # Generate audio file path
    speech_path = os.path.join("output", f"{filename}_{language}.mp3")
    engine.save_to_file(text, speech_path)
    engine.runAndWait()

    return speech_path