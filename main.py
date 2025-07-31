import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any
import google.generativeai as genai
from google.generativeai.types import content_types

# 1. Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chat.log"),
        logging.StreamHandler()
    ]
)

# 2. Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    logging.error("API_KEY not found in .env file.")
    raise ValueError("API_KEY not found. Please create a .env file with your Gemini API key.")

# Configure the Gemini SDK
genai.configure(api_key=API_KEY)

# 3. Initialize FastAPI app
app = FastAPI()

# 4. Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# 5. Define Pydantic models
class ChatRequest(BaseModel):
    history: List[Dict[str, Any]]

# 6. Define API endpoints
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.post("/api/chat")
async def chat_handler(request: ChatRequest):
    logging.info(f"Incoming request history: {request.history}")

    if not request.history:
        raise HTTPException(status_code=400, detail="Chat history cannot be empty.")

    try:
        # Extract the last user message and the preceding history
        last_user_message_text = request.history[-1]["parts"][0]["text"]
        previous_history = request.history[:-1]

        # Initialize the generative model
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Format the previous history for the SDK
        formatted_history = []
        for message in previous_history:
            role = message['role']
            text = message['parts'][0]['text']
            formatted_history.append(content_types.to_content({'role': role, 'parts': [text]}))

        # Start a chat session with the context
        chat_session = model.start_chat(history=formatted_history)

        # Send the last message
        response = await chat_session.send_message_async(last_user_message_text)

        model_response_text = response.text
        logging.info(f"Outgoing model response: {model_response_text}")

        return {"response": model_response_text}

    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
