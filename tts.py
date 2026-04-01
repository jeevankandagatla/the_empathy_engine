import pyttsx3
import wave
import os

import pythoncom

def apply_voice(engine, emotion, intensity, text):
    rate = 150
    volume = 0.8
    pitch = "0"

    if emotion == "excited":
        rate = 180 + int(40 * intensity)
        volume = 1.0
        pitch = "+10"
    elif emotion == "happy":
        rate = 160 + int(20 * intensity)
        volume = 0.9
        pitch = "+5"
    elif emotion == "sad":
        rate = 120 - int(20 * intensity)
        volume = 0.6
        pitch = "-10"
    elif emotion == "angry":
        rate = 170 + int(30 * intensity)
        volume = 1.0
        pitch = "-5"

    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    
    # Wrap in SAPI5 pitch modifier XML for realistic tone shift
    return f"<pitch absmiddle='{pitch}'>{text}</pitch>"


def speak_parts(parts_with_emotion):
    # Initialize COM in the current thread (required for Flask routes on Windows)
    pythoncom.CoInitialize()
    engine = pyttsx3.init()

    temp_files = []

    # Step 1: Generate individual WAV files
    for i, (text, emotion, intensity) in enumerate(parts_with_emotion):
        modulated_text = apply_voice(engine, emotion, intensity, text)

        filename = f"static/part_{i}.wav"
        temp_files.append(filename)

        engine.save_to_file(modulated_text, filename)
        
    engine.runAndWait()

    # Step 2: Merge WAV files manually
    output_file = "static/output.wav"

    with wave.open(output_file, 'wb') as out:
        for i, file in enumerate(temp_files):
            with wave.open(file, 'rb') as w:
                if i == 0:
                    out.setparams(w.getparams())
                out.writeframes(w.readframes(w.getnframes()))

    # Step 3: Cleanup temp files
    for file in temp_files:
        os.remove(file)