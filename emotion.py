from textblob import TextBlob

def detect_emotion(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    # intensity = strength of emotion
    intensity = abs(polarity)

    if polarity > 0.5:
        return "excited", intensity
    elif polarity > 0:
        return "happy", intensity
    elif polarity < -0.5:
        return "angry", intensity
    elif polarity < 0:
        return "sad", intensity
    else:
        return "neutral", intensity