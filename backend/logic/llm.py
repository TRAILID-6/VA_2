# backend/logic/llm.py
import logging
from openai import OpenAI
from groq import Groq
import google.generativeai as genai
import ollama
from .config import Config


def _format_history_for_gemini(chat_history):
    """
    Converts OpenAI-style history to Gemini-style history.
    """
    gemini_history = []
    for msg in chat_history:
        if msg["role"] == "assistant":
            gemini_history.append({"role": "model", "parts": [msg["content"]]})
        elif msg["role"] == "user":
            gemini_history.append({"role": "user", "parts": [msg["content"]]})
    return gemini_history


def generate_response(model, api_key, chat_history):
    """Generate a response using the specified LLM."""
    try:
        if model == "openai":
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=Config.OPENAI_LLM, messages=chat_history
            )
            return response.choices[0].message.content

        elif model == "groq":
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model=Config.GROQ_LLM, messages=chat_history, temperature=0.7
            )
            return response.choices[0].message.content

        elif model == "gemini":
            genai.configure(api_key=api_key)

            system_prompt = ""
            if chat_history and chat_history[0]["role"] == "system":
                system_prompt = chat_history[0]["content"]

            gemini_history = _format_history_for_gemini(chat_history[1:])

            model_instance = genai.GenerativeModel(
                model_name=Config.GEMINI_LLM, system_instruction=system_prompt
            )

            latest_user_message = chat_history[-1]["content"]

            chat = model_instance.start_chat(history=gemini_history[:-1])
            response = chat.send_message(latest_user_message)

            return response.text

        elif model == "ollama":
            response = ollama.chat(model=Config.OLLAMA_LLM, messages=chat_history)
            return response["message"]["content"]

        else:
            raise ValueError("Unsupported response model")

    except Exception as e:
        logging.error(f"Failed to generate response: {e}")
        raise
