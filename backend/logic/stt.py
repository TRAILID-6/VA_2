# backend/logic/stt.py
import logging
from openai import OpenAI
from groq import Groq


def transcribe_audio(model, api_key, audio_file_path):
    """Transcribe an audio file using the specified model."""
    try:
        if model == "openai":
            client = OpenAI(api_key=api_key)
            with open(audio_file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file
                )
            return transcription.text

        elif model == "groq":
            client = Groq(api_key=api_key)
            with open(audio_file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-large-v3", file=audio_file
                )
            return transcription.text

        else:
            raise ValueError("Unsupported transcription model")
    except Exception as e:
        logging.error(f"Failed to transcribe audio: {e}")
        raise
