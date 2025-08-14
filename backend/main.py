# backend/main.py
import os
import uuid
import logging
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import logic functions
from logic.config import Config
from logic.api_keys import get_transcription_api_key, get_tts_api_key, get_api_key
from logic.stt import transcribe_audio
from logic.llm import generate_response
from logic.tts import text_to_speech

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static File Serving ---
STATIC_DIR = "generated_audio"
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.post("/api/process")
async def process_input(
    responseModel: str = Form(...),
    text: str = Form(None),
    audio_file: UploadFile = File(None),
):
    # This chat history is reset for every request (stateless)
    chat_history = [
        {
            "role": "system",
            "content": "You are Mirafra AI, a friendly and helpful voice assistant.",
        }
    ]

    user_input = ""
    temp_audio_path = None
    was_voice_input = False

    try:
        if audio_file:
            was_voice_input = True
            temp_audio_path = os.path.join(STATIC_DIR, f"temp_{uuid.uuid4()}.wav")
            with open(temp_audio_path, "wb") as f:
                f.write(await audio_file.read())

            api_key = get_transcription_api_key()
            user_input = transcribe_audio(
                Config.TRANSCRIPTION_MODEL, api_key, temp_audio_path
            )
        elif text:
            user_input = text
        else:
            raise HTTPException(status_code=400, detail="No input provided.")

        chat_history.append({"role": "user", "content": user_input})

        # --- DEBUGGING LOG ---
        logging.info(
            f"--- Attempting to generate response using model: {responseModel} ---"
        )

        # --- DYNAMIC MODEL & KEY SELECTION ---
        api_key = get_api_key("response", responseModel)
        response_text = generate_response(responseModel, api_key, chat_history)

        chat_history.append({"role": "assistant", "content": response_text})

        # --- CONDITIONAL TTS ---
        audio_url = None
        if was_voice_input:
            api_key = get_tts_api_key()
            output_filename = f"response_{uuid.uuid4()}.mp3"
            output_path = os.path.join(STATIC_DIR, output_filename)
            text_to_speech(Config.TTS_MODEL, api_key, response_text, output_path)
            audio_url = f"/static/{output_filename}"

        # --- FINAL RESPONSE ---
        return {
            "responseText": response_text,
            "audioUrl": audio_url,
            "transcribedText": user_input,
            "modelUsed": responseModel,
        }

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary audio file
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)


@app.get("/")
def read_root():
    return {"message": "Voice Assistant Backend is running."}
