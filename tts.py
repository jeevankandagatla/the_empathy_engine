import pyttsx3
import wave
import os

engine = pyttsx3.init()

def apply_voice(emotion, intensity):
    rate = 150
    volume = 0.8

    if emotion == "excited":
        rate = 180 + int(40 * intensity)
        volume = 1.0
    elif emotion == "happy":
        rate = 160 + int(20 * intensity)
        volume = 0.9
    elif emotion == "sad":
        rate = 120 - int(20 * intensity)
        volume = 0.6
    elif emotion == "angry":
        rate = 170 + int(30 * intensity)
        volume = 1.0

    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)


def speak_parts(parts_with_emotion):
    temp_files = []

    # Step 1: Generate individual WAV files
    for i, (text, emotion, intensity) in enumerate(parts_with_emotion):
        apply_voice(emotion, intensity)

        filename = f"static/part_{i}.wav"
        temp_files.append(filename)

        engine.save_to_file(text, filename)
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