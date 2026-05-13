from flask import Flask, render_template, request, jsonify
from emotion import detect_emotion, split_text
from tts import speak_parts_sync

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

    for i, part in enumerate(parts):
        emotion, intensity = detect_emotion(part)
        parts_with_emotion.append((part, emotion, intensity))

    output_filename = "static/output.mp3"
    speak_parts_sync(parts_with_emotion, output_filename)

    return jsonify({
        "audio_files": ["/" + output_filename]
    })

if __name__ == "__main__":
    app.run(debug=True)