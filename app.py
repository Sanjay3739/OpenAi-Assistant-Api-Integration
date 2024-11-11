import streamlit as st
import openai
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Set your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY  # Replace with your actual API key

# Function to upload the file to OpenAI
def upload_file_to_openai(file):
    url = "https://api.openai.com/v1/files"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
    }
    
    # Read file as binary and upload it as multipart/form-data
    files = {'file': (file.name, file, file.type)}
    data = {'purpose': 'fine-tune'}  # Set the purpose in the data payload
    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("File upload failed: " + response.json().get("error", {}).get("message", "Unknown error"))
        return None

# Function to create an assistant
def create_assistant(file_id):
    url = "https://api.openai.com/v1/assistants"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": "Document Analyzer",
        "description": "Analyzes documents and provides insights.",
        "model": "gpt-4o",
        "tools": [{"type": "code_interpreter"}],
        "tool_resources": {
            "code_interpreter": {
                "file_ids": [file_id]
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Assistant creation failed: " + response.json().get("error", {}).get("message", "Unknown error"))
        return None

# Function to create a thread for conversation
def create_thread(assistant_id, file_id):
    url = "https://api.openai.com/v1/threads"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Analyze this document and provide insights.",
                "attachments": [
                    {
                        "file_id": file_id,
                        "tools": [{"type": "code_interpreter"}]
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Thread creation failed: " + response.json().get("error", {}).get("message", "Unknown error"))
        return None

# Function to run the conversation
def run_conversation(thread_id, assistant_id):
    url = f"https://api.openai.com/v1/threads/{thread_id}/runs"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "assistant_id": assistant_id
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Run conversation failed: " + response.json().get("error", {}).get("message", "Unknown error"))
        return None

# Streamlit application
st.title("Document Analyzer with OpenAI")

# File upload
uploaded_file = st.file_uploader("Upload a document (PDF or DOC)", type=["pdf", "doc", "docx"])

if uploaded_file is not None:
    # Step 1: Upload file to OpenAI
    file_response = upload_file_to_openai(uploaded_file)
    if file_response is not None:
        file_id = file_response.get("id")
        st.success(f"File uploaded successfully. File ID: {file_id}")

        # Step 2: Create an assistant
        assistant_response = create_assistant(file_id)
        if assistant_response is not None:
            assistant_id = assistant_response.get("id")
            st.success(f"Assistant created successfully. Assistant ID: {assistant_id}")

            # Step 3: Create a thread for conversation
            thread_response = create_thread(assistant_id, file_id)
            if thread_response is not None:
                thread_id = thread_response.get("id")
                st.success(f"Thread created successfully. Thread ID: {thread_id}")

                # Step 4: Run the conversation
                run_response = run_conversation(thread_id, assistant_id)
                if run_response is not None:
                    message_content = run_response.get("messages", [])
                    st.subheader("Assistant Response:")
                    for message in message_content:
                        st.write(f"{message['role']}: {message['content']}")

