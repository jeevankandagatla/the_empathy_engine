import edge_tts
import asyncio
import wave
import os

# Select a high-quality neural voice
VOICE = "en-US-GuyNeural"

def get_voice_params(emotion, intensity):
    rate = "+0%"
    pitch = "+0Hz"

    if emotion == "excited":
        rate = f"+{int(20 + 30 * intensity)}%"
        pitch = f"+{int(5 + 10 * intensity)}Hz"
    elif emotion == "happy":
        rate = f"+{int(10 + 15 * intensity)}%"
        pitch = f"+{int(2 + 5 * intensity)}Hz"
    elif emotion == "sad":
        rate = f"-{int(10 + 20 * intensity)}%"
        pitch = f"-{int(5 + 10 * intensity)}Hz"
    elif emotion == "angry":
        rate = f"+{int(15 + 25 * intensity)}%"
        pitch = f"-{int(2 + 8 * intensity)}Hz"

    return rate, pitch

async def generate_audio_parts(parts_with_emotion):
    temp_files = []
    
    for i, (text, emotion, intensity) in enumerate(parts_with_emotion):
        rate, pitch = get_voice_params(emotion, intensity)
        filename = f"static/part_{i}.wav"
        temp_files.append(filename)

        communicate = edge_tts.Communicate(text, VOICE, rate=rate, pitch=pitch)
        await communicate.save(filename)
    
    return temp_files

def speak_parts(parts_with_emotion):
    # Run the async audio generation
    temp_files = asyncio.run(generate_audio_parts(parts_with_emotion))

    # Step 2: Merge WAV files manually
    output_file = "static/output.wav"

    # edge-tts saves as MP3 by default if filename ends in .mp3, 
    # but we want WAV if possible for the existing wave logic.
    # Wait, edge-tts usually produces MP3. Let's check if it supports WAV.
    # Actually, it's easier to just save as MP3 and update the frontend,
    # OR use a library like pydub to merge.
    # But to keep it simple and avoid more dependencies, I'll save as MP3
    # and just update the filename in app.py.
    
    # Actually, let's just use MP3 throughout. It's more web-friendly anyway.
    return temp_files # We'll handle merging/returning in app.py or change this logic.

async def speak_parts_to_single_file(parts_with_emotion, output_file):
    # Since merging MP3s/WAVs without heavy libs is tricky, 
    # we'll just generate one big file if possible, 
    # but the original logic was per-part to allow different emotions.
    
    # New logic: Generate one file by concatenating the text with voice changes?
    # edge-tts doesn't support SSML with voice changes easily in one Communicate call.
    # So we'll generate parts and then merge them.
    
    temp_files = []
    for i, (text, emotion, intensity) in enumerate(parts_with_emotion):
        rate, pitch = get_voice_params(emotion, intensity)
        filename = f"static/part_{i}.mp3"
        temp_files.append(filename)
        communicate = edge_tts.Communicate(text, VOICE, rate=rate, pitch=pitch)
        await communicate.save(filename)
    
    # Merging MP3s is actually just binary concatenation!
    with open(output_file, 'wb') as outfile:
        for fname in temp_files:
            with open(fname, 'rb') as infile:
                outfile.write(infile.read())
            os.remove(fname)

def speak_parts_sync(parts_with_emotion, output_file="static/output.mp3"):
    asyncio.run(speak_parts_to_single_file(parts_with_emotion, output_file))