from flask import Flask, render_template, request, jsonify
from emotion import detect_emotion, split_text
from tts import speak_parts

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    text = data["text"]

    parts = split_text(text)

    parts_with_emotion = []
    audio_files = []

    for i, part in enumerate(parts):
        emotion, intensity = detect_emotion(part)
        parts_with_emotion.append((part, emotion, intensity))

        filename = f"/static/part_{i}.wav"
        audio_files.append(filename)

    speak_parts(parts_with_emotion)

    return jsonify({
        "audio_files": audio_files
    })

if __name__ == "__main__":
    app.run(debug=True)