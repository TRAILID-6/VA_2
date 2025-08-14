import logging
import requests
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from .config import Config

LOCAL_TTS_URL = "http://127.0.0.1:8001/api/tts"


def text_to_speech(model, api_key, text_to_speak, output_file_path):
    """Convert text to speech using the specified model."""
    try:
        if model == "openai":
            client = OpenAI(api_key=api_key)
            response = client.audio.speech.create(
                model="tts-1", voice="nova", input=text_to_speak
            )
            response.stream_to_file(output_file_path)

        elif model == "elevenlabs":
            client = ElevenLabs(api_key=api_key)
            response = client.text_to_speech.convert(
                voice_id="pNInz6obpgDQGcFmaJgB",
                text=text_to_speak,
                model_id="eleven_multilingual_v2",
            )
            with open(output_file_path, "wb") as f:
                for chunk in response:
                    f.write(chunk)

        elif model == "melotts":
            payload = {"text": text_to_speak}
            response = requests.post(LOCAL_TTS_URL, json=payload, stream=True)

            if response.status_code == 200:
                with open(output_file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            else:
                logging.error(f"Local TTS server returned an error: {response.text}")
                raise Exception("Failed to get audio from local TTS server.")

        else:
            raise ValueError("Unsupported TTS model")

    except Exception as e:
        logging.error(f"Failed to convert text to speech: {e}")
        raise
