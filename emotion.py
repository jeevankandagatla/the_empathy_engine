import re
from textblob import TextBlob

def split_text(text):
    # Step 1: Split by punctuation (keep punctuation) 
    # BUT DO NOT split if the punctuation is immediately followed by a connector!
    # This prevents e.g. "I am happy," and "but" from being broken apart prematurely.
    sentences = re.split(r'(?<=[.!?,])\s+(?!(?i:but|however|although)\b)', text)

    final_parts = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # Step 2: Recursively find all connectors and split AFTER them (keeping trailing punctuation)
        while True:
            # Find the FIRST connector in the current sentence chunk
            match = re.search(r'\b(but|however|although)\b[.!?,]*', sentence, flags=re.IGNORECASE)
            
            if match:
                idx = match.end()
                
                # Split into two parts, breaking word on the left
                first = sentence[:idx].strip()
                sentence = sentence[idx:].strip() # Keep remaining part for the next iteration
                
                if first:
                    final_parts.append(first)
                
                if not sentence:
                    break
            else:
                final_parts.append(sentence)
                break

    return final_parts

def detect_emotion(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    text_lower = text.lower()

    intensity = abs(polarity)

    angry_words = ["angry", "furious", "hate", "worst", "terrible", "frustrated", "annoyed", "mad", "upset"]
    sad_words = ["sad", "depressed", "cry", "miserable", "alone", "lonely", "sorrow", "hurt"]
    excited_words = ["excited", "thrilled", "amazing", "awesome", "fantastic", "incredible", "wow", "great"]
    happy_words = ["happy", "glad", "joy", "good", "nice", "fun", "lovely"]

    # Direct keyword matches trump polarity
    if any(word in text_lower for word in angry_words):
        return "angry", max(0.5, intensity)
    if any(word in text_lower for word in sad_words):
        return "sad", max(0.4, intensity)
    if any(word in text_lower for word in excited_words):
        return "excited", max(0.6, intensity)
    if any(word in text_lower for word in happy_words):
        return "happy", max(0.4, intensity)

    # Fallback to TextBlob polarity rules
    if polarity > 0.4:
        return "excited", intensity
    elif polarity > 0.05:
        return "happy", intensity
    elif polarity < -0.3:
        return "sad", intensity
    elif polarity < 0:
        return "angry", intensity * 1.5  # Slightly boost intensity for frustration
    else:
        return "neutral", intensity