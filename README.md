# Gemini Chat Application

This is a full-stack web application that provides a chat interface to the Google Gemini API. It features a Python FastAPI backend and a simple frontend built with vanilla HTML, CSS, and JavaScript.

## Description

The application allows users to have a conversation with the Gemini AI model. The backend uses the `google-genai` Python SDK. The conversation history is managed on the client-side and sent to the backend with each new message, following a "Model Context Protocol" (MCP).

### Key Features:

- **Backend**: Built with FastAPI.
- **Frontend**: Vanilla HTML, CSS, and JavaScript.
- **Gemini Integration**: Uses the `google-genai` SDK to interact with the Gemini API (`gemini-2.5-flash` model).
- **Context Management**: The client maintains the full conversation history and sends it with each request.
- **Logging**: All chat interactions are logged to a `chat.log` file.

## Environment Setup and Configuration

Follow these instructions to set up and run the project on your local machine.

### 1. Prerequisites

- Python 3.7+
- An active Google Gemini API key.

### 2. Installation

**a. Clone the repository (if you haven't already):**
```bash
git clone <repository-url>
cd <repository-directory>
```

**b. Create and configure the environment file:**
Create a file named `.env` in the root of the project and add your API key:
```
API_KEY="YOUR_GEMINI_API_KEY"
```
Replace `"YOUR_GEMINI_API_KEY"` with your actual key.

**c. Install dependencies:**
Install the required Python packages using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Running the Application

**a. Start the backend server:**
Use Uvicorn to run the FastAPI application:
```bash
uvicorn main:app --reload
```
The `--reload` flag makes the server restart after code changes.

**b. Open the application:**
Once the server is running, open your web browser and navigate to:
```
http://127.0.0.1:8000
```
You can now start chatting with the Gemini model.
