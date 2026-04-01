# Empathy Engine 🎙️

## 📌 Overview
The **Empathy Engine** is an advanced AI-driven conversational web application that converts typed or spoken text into emotionally expressive speech. It features a stunning, modern glassmorphism web interface that allows users to chat via text or microphone. 

Under the hood, the engine intelligently chunks your sentences, detects the underlying sentiment of each chunk, and dynamically modulates Text-to-Speech (TTS) voice parameters—adjusting speed, volume, and pitch—to truly express the feeling behind the words.

---

## 🚀 Setup & Execution Instructions

Follow these step-by-step instructions to get the application running on your Windows machine:

1. **Ensure Python is Installed**: Ensure you have Python 3.8+ installed on your system.
2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```
3. **Activate the Environment**:
   ```bash
   venv\Scripts\activate
   ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the Server**:
   ```bash
   python app.py
   ```
6. **Access the UI**: Open your web browser and navigate to `http://127.0.0.1:5000`. Be sure to grant microphone permissions if you intend to use the voice-to-text feature!

---

## 🧠 Design & Architectural Choices

### 1. Robust Sentence Chunking (`emotion.py`)
Standard TTS engines sound robotic when reading long, multi-emotional paragraphs. We engineered a custom chunking algorithm that splits the user's input safely:
- It splits strings on punctuation (`.`, `!`, `?`, `,`) **only** if the punctuation is not immediately followed by a logical connector.
- It recursively hunts for connectors (`but`, `however`, `although`) and splits the sentence right after them. This ensures that the breaking connector word remains safely attached to the left part of the context, allowing the TTS engine to shift its tone exactly when the semantic pivot happens.

### 2. Emotion Classification Override
We utilize `TextBlob` for baseline sentiment polarity. However, because standard algorithmic polarity can occasionally misclassify emotions (e.g., scoring the word "happy" higher than "excited"), the engine employs a **hierarchical keyword override**:
- It searches the chunk for distinct clusters of emotional trigger words (`angry_words`, `sad_words`, `excited_words`, `happy_words`). 
- Direct keyword matches immediately force the classification (and scale the intensity), safely bypassing generic polarity errors.

### 3. Voice Parameter Mapping (`tts.py`)
Once an emotion and its intensity (0.0 to 1.0) are calculated, it applies a multidimensional shift to the `pyttsx3` engine. We map emotions to voice parameters using the following logic:

| Emotion | Rate (Speed in WPM) | Volume | Pitch (Tone) | Explanation |
| :--- | :--- | :--- | :--- | :--- |
| **Excited** | `180 + (40 * intensity)` | 100% | `+10` | Vastly accelerates speaking speed, maxes volume, and shifts the physical pitch higher to emulate adrenaline and energy. |
| **Happy** | `160 + (20 * intensity)` | 90% | `+5` | Slightly faster than baseline, buoyant pitch, comfortable high volume. |
| **Sad** | `120 - (20 * intensity)` | 60% | `-10` | Noticeably slows down the speech rate, drastically lowers the volume to a soft tone, and drops the physical pitch to convey sorrow. |
| **Angry** | `170 + (30 * intensity)` | 100% | `-5` | Fast and incredibly loud, but with a deeply lowered pitch to represent frustration and growling aggression. |
| **Neutral** | Base (`150`) | 80% | `0` | Standard, calm conversational voice. |

*Note on Pitch Modulation: Because `pyttsx3` does not natively support an `engine.setProperty('pitch')` interface, our engine physically wraps your text chunks in Microsoft SAPI5 XML modifier tags (e.g., `<pitch absmiddle='-10'>...text...</pitch>`). This instructs the Windows OS voice driver to physically modulate the synthesis frequency on the fly, producing a vastly more realistic conversational tone.*

### 4. UI/UX 
To ensure the product feels premium, the frontend (`index.html`) moves away from generic `<audio>` tags. We built a custom **Glassmorphism Chat Dashboard** equipped with:
- An animated mesh gradient backdrop.
- A glowing STT (Speech-to-Text) microphone button natively hooking into the browser's `SpeechRecognition` API.
- A custom audio playback UI that seamlessly autoplays the dynamically generated `.wav` files perfectly in sync with the bot's typing indicator animations.