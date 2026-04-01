import re
from textblob import TextBlob

def split_text(text):
    # Step 1: Split by punctuation (keep punctuation)
    sentences = re.split(r'(?<=[.!?,])\s+', text)

    final_parts = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # Step 2: Check for connectors inside sentence
        match = re.search(r'\b(but|however|although)\b', sentence, flags=re.IGNORECASE)

        if match:
            idx = match.start()

            # Split into two parts
            first = sentence[:idx].strip()
            second = sentence[idx:].strip()

            # Add only if meaningful
            if first:
                final_parts.append(first)
            if second:
                final_parts.append(second)
        else:
            final_parts.append(sentence)

    return final_parts

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