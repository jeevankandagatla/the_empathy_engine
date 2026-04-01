import re
from textblob import TextBlob

def split_text(text):
    # Split but KEEP delimiters like "but"
    parts = re.split(r'(\bbut\b|\bhowever\b|\balthough\b|[,.!?])', text, flags=re.IGNORECASE)

    result = []
    current = ""

    for part in parts:
        if part.lower() in ["but", "however", "although"] or re.match(r'[,.!?]', part):
            current += " " + part
            result.append(current.strip())
            current = ""
        else:
            current += " " + part

    if current.strip():
        result.append(current.strip())

    return result

def detect_emotion(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    text_lower = text.lower()

    intensity = abs(polarity)

    angry_words = ["angry", "furious", "hate", "worst", "terrible", "frustrated", "annoyed"]

    if any(word in text_lower for word in angry_words):
        return "angry", intensity

    if polarity > 0.5:
        return "excited", intensity
    elif polarity > 0:
        return "happy", intensity
    elif polarity < 0:
        return "sad", intensity
    else:
        return "neutral", intensity