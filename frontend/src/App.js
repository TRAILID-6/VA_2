// frontend/src/App.js
import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = 'http://127.0.0.1:8000';

function App() {
  // State for messages, input, and UI status
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [responseModel, setResponseModel] = useState('groq'); // Default model is groq

  // State for testing and audio control
  const [lastAudioUrl, setLastAudioUrl] = useState(null);
  const [lastTranscription, setLastTranscription] = useState('');
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);

  // Refs for DOM elements and media objects
  const messagesEndRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioRef = useRef(null); // For controlling output audio

  // Auto-scroll to the latest message
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([{ role: 'assistant', content: 'Hello! How can I help you today?', model: 'System' }]);
    }
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Main function to communicate with the backend
  const sendToServer = async (formData) => {
    formData.append('responseModel', responseModel);

    try {
      const response = await axios.post(`${API_URL}/api/process`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const { responseText, audioUrl, transcribedText, modelUsed } = response.data;
      setMessages(prev => [...prev, { role: 'assistant', content: responseText, model: modelUsed }]);
      setLastTranscription(transcribedText || '');

      if (audioUrl) {
        if (audioRef.current) {
          audioRef.current.pause();
        }
        const newAudio = new Audio(`${API_URL}${audioUrl}`);
        audioRef.current = newAudio;
        newAudio.onended = () => setIsAudioPlaying(false);
        newAudio.play();
        setIsAudioPlaying(true);
      }
    } catch (error) {
      console.error("Error sending data to server:", error);
    }
  };

  // Handler for sending text input
  const handleSendText = () => {
    if (!inputValue.trim()) return;
    setMessages(prev => [...prev, { role: 'user', content: inputValue }]);
    const formData = new FormData();
    formData.append('text', inputValue);
    sendToServer(formData);
    setInputValue('');
  };

  // FULL Handler for recording audio
  const handleToggleRecording = () => {
    if (isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    } else {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          const mediaRecorder = new MediaRecorder(stream);
          mediaRecorderRef.current = mediaRecorder;
          audioChunksRef.current = [];
          mediaRecorder.ondataavailable = event => audioChunksRef.current.push(event.data);

          mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            setLastAudioUrl(audioUrl); // For the test player

            const audioFile = new File([audioBlob], "recording.wav", { type: "audio/wav" });
            const formData = new FormData();
            formData.append('audio_file', audioFile);
            setMessages(prev => [...prev, { role: 'user', content: '[Voice Input]' }]);
            sendToServer(formData);
            stream.getTracks().forEach(track => track.stop());
          };

          mediaRecorder.start();
          setIsRecording(true);
        })
        .catch(err => console.error("Error accessing microphone:", err));
    }
  };

  // Handler for pausing/resuming output audio
  const handleToggleAudio = () => {
    if (!audioRef.current) return;
    if (isAudioPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsAudioPlaying(!isAudioPlaying);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        My Personal AI
        <div className="model-selector">
          <label htmlFor="model-select">Model: </label>
          <select id="model-select" value={responseModel} onChange={e => setResponseModel(e.target.value)}>
            <option value="groq">Groq (Llama)</option>
            <option value="ollama">Ollama (Local)</option>
            <option value="gemini">Gemini</option>
            <option value="openai">OpenAI (GPT)</option>
          </select>
        </div>
      </div>

      {lastAudioUrl && (
        <div style={{ padding: '10px', textAlign: 'center', backgroundColor: '#fffbe6', borderBottom: '1px solid #eee' }}>
          <strong>Test Playback:</strong>
          <audio controls src={lastAudioUrl} style={{ width: '100%', marginTop: '5px' }} />
          {lastTranscription && (
            <div style={{ marginTop: '10px', fontStyle: 'italic', color: '#555' }}>
              <strong>Transcription Result:</strong> "{lastTranscription}"
            </div>
          )}
        </div>
      )}

      <div className="messages-area">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            {msg.content}
            {msg.role === 'assistant' && msg.model && (
              <div className="model-tag">Powered by {msg.model}</div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input type="text" value={inputValue} onChange={(e) => setInputValue(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && handleSendText()} placeholder="Type your message..." />
        {audioRef.current && (
          <button className="record" onClick={handleToggleAudio}>
            {isAudioPlaying ? 'Pause' : 'Resume'}
          </button>
        )}
        <button className="send" onClick={handleSendText}>Send</button>
        <button className={isRecording ? 'stop' : 'record'} onClick={handleToggleRecording}>{isRecording ? 'Stop' : 'Record'}</button>
      </div>
    </div>
  );
}

export default App;