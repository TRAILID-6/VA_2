import uvicorn
import torch
from melo.api import TTS
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

# Configuration
PORT = 8001
TEMP_AUDIO_FILE = "temp_tts_output.wav"

# Initialize Model
speed = 1.0
device = "cuda" if torch.cuda.is_available() else "cpu"

print("Loading MeloTTS model... (This may take a moment)")
model = TTS(language="EN", device=device)
speaker_ids = model.hps.data.spk2id
print("MeloTTS model loaded.")

# FastAPI App
app = FastAPI()


class TTSRequest(BaseModel):
    text: str
    speaker_id: str = "EN-US"


@app.post("/api/tts")
async def generate_speech(request: TTSRequest):
    if request.speaker_id not in speaker_ids:
        raise HTTPException(status_code=400, detail="Invalid speaker_id")
    try:
        model.tts_to_file(
            request.text, speaker_ids[request.speaker_id], TEMP_AUDIO_FILE, speed=speed
        )
        return FileResponse(TEMP_AUDIO_FILE, media_type="audio/wav")
    except Exception as e:
        print(f"Error during TTS generation: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate audio")
