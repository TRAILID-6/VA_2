# backend/logic/api_keys.py
from .config import Config

API_KEY_MAPPING = {
    "transcription": {
        "openai": Config.OPENAI_API_KEY,
        "groq": Config.GROQ_API_KEY,
    },
    "response": {
        "openai": Config.OPENAI_API_KEY,
        "groq": Config.GROQ_API_KEY,
        "gemini": Config.GOOGLE_API_KEY,
        "ollama": None,
    },
    "tts": {
        "openai": Config.OPENAI_API_KEY,
        "elevenlabs": Config.ELEVENLABS_API_KEY,
        "melotts": None,
    },
}


def get_api_key(service, model):
    """Select the API key for the specified service and model."""
    return API_KEY_MAPPING.get(service, {}).get(model)


def get_transcription_api_key():
    """Get the API key for the configured transcription service."""
    return get_api_key("transcription", Config.TRANSCRIPTION_MODEL)


def get_response_api_key():
    """Get the API key for the configured response generation service."""
    return get_api_key("response", Config.RESPONSE_MODEL)


def get_tts_api_key():
    """Get the API key for the configured TTS service."""
    return get_api_key("tts", Config.TTS_MODEL)
