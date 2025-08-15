```markdown
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

```

web-voice-assistant/
├── backend/
│   ├── logic/
│   │   ├── config.py         \# Main configuration for models
│   │   └── ...               \# Other logic files (llm, stt, tts)
│   ├── .env                  \# API keys and secrets
│   ├── main.py               \# Main FastAPI server
│   ├── local\_tts\_server.py   \# Dedicated server for MeloTTS
│   ├── patch\_melo.py         \# One-time script to fix a dependency
│   └── requirements.txt      \# Python dependencies
│
└── frontend/
├── src/
│   ├── App.js            \# Main React component
│   └── ...
└── package.json          \# Frontend dependencies

````

## 🚀 Getting Started

### Prerequisites

* **Python** (3.9 or higher)
* **Node.js and npm** (for the React frontend)
* **Git** (for installing some dependencies)

### 1. Initial Setup

First, clone the project repository and set up the necessary virtual environments.

```bash
# Clone the repository (if you haven't already)
git clone <your-repo-url>
cd web-voice-assistant
````

### 2\. Backend Setup (Python)

Navigate to the backend folder and set up a Python virtual environment.

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt
```

### 3\. Frontend Setup (React)

Open a **new terminal** for the frontend.

```bash
# Navigate to the frontend directory
cd frontend

# Install the required Node.js packages
npm install
```

## ⚙️ Configuration

### 1\. API Keys

Before running the application, you need to provide API keys for the cloud services you want to use.

1.  In the `backend` folder, rename the `.env.example` file to `.env`.
2.  Open the `.env` file and add your keys.

<!-- end list -->

```env
# Get from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"

# Get from [https://console.groq.com/keys](https://console.groq.com/keys)
GROQ_API_KEY="YOUR_GROQ_API_KEY"

# Get from [https://elevenlabs.io/](https://elevenlabs.io/)
ELEVENLABS_API_KEY="YOUR_ELEVENLABS_API_KEY"

# Get from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
GOOGLE_API_KEY="YOUR_GOOGLE_AI_STUDIO_KEY"
```

### 2\. Switching Models

This project is designed for easy model switching.

  * **Response Model (LLM):** This is controlled directly from the **dropdown menu in the user interface**.
  * **Transcription & TTS Models:** These are set in the backend configuration file.
      * Open `backend/logic/config.py`.
      * Change the values for `TRANSCRIPTION_MODEL` and `TTS_MODEL` to your desired provider (e.g., `'openai'`, `'groq'`, `'elevenlabs'`).

## ▶️ Running the Application

You will need to have **at least two terminals open** to run the full application (three if you use the local MeloTTS).

### Terminal 1: Start the Backend Server

```bash
# Make sure you are in the backend/ directory with your virtual environment active
uvicorn main:app --reload
```

This will start the main server, usually on `http://127.0.0.1:8000`.

### Terminal 2: Start the Frontend Server

```bash
# Make sure you are in the frontend/ directory
npm start
```

This will open the user interface in your browser, usually at `http://localhost:3000`.

## 🏡 Using Local Models (Advanced)

For enhanced privacy and offline capability, you can run the LLM and TTS models locally on your own machine.

### Ollama (for LLM)

1.  **Install Ollama:** Download and install the Ollama application for your operating system from [ollama.com](https://ollama.com/).
2.  **Pull a Model:** Open your terminal and pull the model you want to use. For example:
    ```bash
    ollama run llama3.2
    ```
3.  **Verify Installation:** Check that the model is available:
    ```bash
    ollama list
    ```
4.  **Configure the Project:**
      * Ensure the Ollama application is running.
      * In `backend/logic/config.py`, make sure the `OLLAMA_LLM` variable matches the name of the model you pulled (e.g., `"llama3.2"`).
      * You can now select "Ollama (Local)" from the dropdown in the UI.

### MeloTTS (for TTS)

MeloTTS is a high-quality local text-to-speech engine.

1.  **Activate in Config:** First, open `backend/logic/config.py` and set the TTS model to `"melotts"` to signal your intent to use it.
    ```python
    TTS_MODEL = "melotts"
    ```
2.  **Install the Library:** The standard package has a bug, so we install it directly from GitHub. In your backend terminal (with the virtual environment active), run:
    ```bash
    pip install git+[https://github.com/myshell-ai/MeloTTS.git](https://github.com/myshell-ai/MeloTTS.git)
    ```
3.  **Patch the Installation:** The MeloTTS library has a dependency bug related to Japanese language processing. A patch script is included to fix this.
      * Run the script **once**:
        ```bash
        python patch_melo.py
        ```
      * This will modify a file inside the installed library to prevent it from crashing. Once the script confirms the patch was successful, **you can delete `patch_melo.py`**.
4.  **Download NLTK Data:** MeloTTS requires an additional data package to work correctly. Run this command once:
    ```bash
    python -m nltk.downloader averaged_perceptron_tagger_eng
    ```
5.  **Run the TTS Server (Terminal 3):**
      * Open a **third terminal**.
      * Navigate to the `backend/` directory and activate your virtual environment.
      * Start the dedicated TTS server:
        ```bash
        uvicorn local_tts_server:app --port 8001
        ```
      * The first time you run this, it will download the MeloTTS model files.

<!-- end list -->

```
```
