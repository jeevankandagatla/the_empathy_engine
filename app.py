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
    for part in parts:
        emotion, intensity = detect_emotion(part)
        parts_with_emotion.append((part, emotion, intensity))

    speak_parts(parts_with_emotion)

    return jsonify({
        "status": "success",
        "audio": "/static/output.mp3"
    })

if __name__ == "__main__":
    app.run(debug=True)