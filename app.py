from emotion import detect_emotion
from tts import speak

def main():
    print("=== Empathy Engine ===")

    text = input("Enter text: ")

    emotion, intensity = detect_emotion(text)

    print(f"Detected Emotion: {emotion}")
    print(f"Intensity: {intensity:.2f}")

    speak(text, emotion, intensity)

    print("Audio saved as output.mp3")

if __name__ == "__main__":
    main()