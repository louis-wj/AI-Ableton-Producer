import pyttsx3
import threading
import queue
from ai_engine import AIEngine
from ableton_controller import AbletonController
import time
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import os

class Speaker(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.queue = queue.Queue()
        self.engine = pyttsx3.init()
        
        # Select Male Voice (David)
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "DAVID" in voice.name.upper() or "DAVID" in voice.id.upper():
                self.engine.setProperty('voice', voice.id)
                break
        
        self.engine.setProperty('rate', 160)

    def run(self):
        while True:
            text = self.queue.get()
            if text is None: break
            self.engine.say(text)
            self.engine.runAndWait()
            self.queue.task_done()

    def say(self, text):
        self.queue.put(text)

# Backend App State
class GlobalState:
    def __init__(self):
        self.ableton = AbletonController()
        self.ai = AIEngine()
        self.speaker = Speaker()
        self.speaker.start()
        
state = GlobalState()
app = FastAPI()

# Serve UI
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("frontend/index.html", "r") as f:
        return f.read()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_text = data.get("text")
    
    # 1. AI Reasoning
    command = state.ai.get_command(user_text)
    
    # 2. Execution
    state.ableton.execute(command)
    
    # 3. Descriptive Feedback
    response_text = f"I have processed your request for '{user_text}'. "
    if "log" in str(command):
        # Use AI's own descriptive log if available
        try:
            response_text = command.get("args", {}).get("message", response_text)
        except: pass
    
    state.speaker.say(response_text)
    
    return {"response": response_text, "idle": True}

if __name__ == "__main__":
    print("--- AI ABLETON PRODUCER PREMIUM UI STARTING ---")
    print("Open http://localhost:8000 in your browser")
    state.speaker.say("AI Producer Premium Interface is now active.")
    uvicorn.run(app, host="0.0.0.0", port=8000)
