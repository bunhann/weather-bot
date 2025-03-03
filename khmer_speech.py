from gtts import gTTS
import os
import uuid

def generate_khmer_audio(text):
    """
    Generates a Khmer audio file from the given text and returns the file path.
    """
    # Generate a unique filename for the audio file
    audio_file = f"audio_{uuid.uuid4()}.mp3"

    # Create the Khmer speech audio
    tts = gTTS(text=text, lang='km')
    tts.save(audio_file)

    return audio_file