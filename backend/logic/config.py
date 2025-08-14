# backend/logic/config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class to hold model selection and API keys.
    """

    # --- MODEL SELECTION ---
    # Select which service to use for each task.
    TRANSCRIPTION_MODEL = "groq"
    RESPONSE_MODEL = "ollama"  # Options: 'openai', 'groq', 'gemini', 'ollama'
    TTS_MODEL = "melotts"  # Options: 'openai', 'elevenlabs', 'melotts'

    # --- LLM MODEL NAMES ---
    # Specify the exact model name for each service.
    GROQ_LLM = "llama3-8b-8192"
    OPENAI_LLM = "gpt-4o"
    GEMINI_LLM = "gemini-1.5-flash-latest"
    OLLAMA_LLM = "llama3.2"

    # --- API KEYS ---
    # Keys are loaded from the .env file.
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
