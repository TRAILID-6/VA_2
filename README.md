# Multi-Model AI Voice Assistant

This is a full-stack, modular voice assistant that combines a React frontend with a Python (FastAPI) backend. It allows users to interact with various state-of-the-art AI models for transcription, response generation (LLM), and text-to-speech (TTS) through either voice or text input.

The key feature of this project is its flexibility, allowing you to switch between different cloud-based and local AI models on the fly.

## ✨ Features

* **Multi-Modal Input:** Supports both text and voice input from the browser.
* **Dynamic Model Selection:** Switch between different AI models for different tasks directly from the UI or config.
    * **Speech-to-Text:** Groq, OpenAI
    * **Response Generation (LLM):** Groq (Llama), Gemini, OpenAI (GPT), and local models via Ollama.
    * **Text-to-Speech:** ElevenLabs, OpenAI, and a fully local option with MeloTTS.
* **Real-time Interaction:** Engages in a conversational flow with audio and text responses.
* **Local First Options:** Capable of running entirely offline using Ollama and MeloTTS for maximum privacy and speed.

## 📂 Project Structure
