# Empathy Engine 🎙️

## 📌 Overview
The Empathy Engine is an AI-based system that converts text into emotionally expressive speech. 
It detects the sentiment of input text and dynamically adjusts voice parameters such as rate and volume.

---

## ⚙️ Features
- Emotion Detection (Happy, Sad, Angry, Excited, Neutral)
- Intensity Scaling
- Dynamic Voice Modulation
- Audio Output (.mp3)

---

## 🧠 How It Works

1. Input text is analyzed using TextBlob.
2. Sentiment polarity determines emotion.
3. Emotion is mapped to voice parameters:
   - Happy → faster + louder
   - Sad → slower + softer
   - Angry → fast + loud
   - Neutral → default
4. Speech is generated using pyttsx3.

---

## 🚀 Setup Instructions

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py