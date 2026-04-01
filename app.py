from emotion import detect_emotion, split_text
from tts import speak_parts

def main():
    print("=== Empathy Engine (Advanced) ===")

    text = input("Enter text: ")

    parts = split_text(text)

    parts_with_emotion = []

    for part in parts:
        emotion, intensity = detect_emotion(part)
        print(f"{part} → {emotion} ({intensity:.2f})")
        parts_with_emotion.append((part, emotion, intensity))

    speak_parts(parts_with_emotion)

    print("Audio saved as output.mp3")

if __name__ == "__main__":
    main()