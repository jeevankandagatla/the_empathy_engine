import pyttsx3

engine = pyttsx3.init()

def speak(text, emotion, intensity):
    
    # Default values
    rate = 150
    volume = 0.8

    # Emotion-based mapping
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
    else:  # neutral
        rate = 150
        volume = 0.8

    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    # Optional: change voice (try index 0 or 1)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    # Save output
    engine.save_to_file(text, "output.mp3")
    engine.runAndWait()