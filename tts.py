import pyttsx3
import time

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


def get_pause_duration(text):
    if text.endswith(","):
        return 0.3
    elif text.endswith("."):
        return 0.6
    elif text.endswith("!") or text.endswith("?"):
        return 0.8
    else:
        return 0.2


def speak_parts(parts_with_emotion):
    full_text = ""

    for text, emotion, intensity in parts_with_emotion:
        apply_voice(emotion, intensity)

        engine.say(text)
        engine.runAndWait()  # speak immediately

        pause = get_pause_duration(text)
        time.sleep(pause)

        full_text += text + " "

    # Save full audio (optional)
    engine.save_to_file(full_text.strip(), "output.mp3")
    engine.runAndWait()