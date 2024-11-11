# OpenAI Assistant API Integration

This project integrates OpenAI's Assistant API to build conversational agents that can process user inputs, generate dynamic responses, and interact with uploaded documents (like PDFs).

## Features:
- Integrate OpenAI's GPT models for conversation.
- Handle user inputs and generate appropriate responses.
- Upload and interact with documents (e.g., PDFs) using OpenAI's API.

## Requirements:
- Python 3.7+
- OpenAI API key
- Required libraries: `openai`, `streamlit`, `dotenv`

## Installation:
1. Clone the repository:
   ```bash
   git clone https://github.com/Sanjay3739/Conversation_chat_with_pdf_usign_openAi.git

2. Create and virtual environment (optional but recommended):   
   ```bash
   python -m venv venv

3. Activate a virtual environment (optional but recommended):
   ```bash
   source venv/bin/activate #for linux
   venv\Scripts\activate #for Windows


4. Install dependencies:
   ```bash
   pip install -r requirements.txt

5. Set your OpenAI API key:
   ```bash
   OPENAI_API_KEY='your-api-key'

6. Run the chatbot:
   ```bash
   python app.py