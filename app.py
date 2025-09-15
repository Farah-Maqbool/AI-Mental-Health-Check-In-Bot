import streamlit as st
from backend import retrieve_chunks
import requests
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

st.title("AI Mental Health Check In Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def call_gemini(llm_prompt: str) -> str:
    """Send prompt to Gemini via REST API and return text response."""
    payload = {
        "contents": [
            {
                "parts": [{"text": llm_prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.5
        }
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "⚠️ Sorry, I couldn’t generate a response. Please try again."


if prompt := st.chat_input("Type your message here..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Retrieve context with FAISS
    rag = retrieve_chunks(prompt)
    context = "\n\n".join(rag)

    # Build the LLM prompt
    llm_prompt = f"""
    You are a compassionate and supportive mental health check-in assistant.

    Your role is to respond to user query and follow these conditions:
    Listen without judgment
    Respond with empathy and warmth
    Offer gentle encouragement and practical coping suggestions
    NEVER give medical, clinical, or crisis advice

    If a user seems to be in crisis or mentions self-harm, gently suggest they talk to a trusted person or call a local mental health helpline

    Use the conversational context below to help guide your response.

    When responding:
    Keep messages short and friendly
    Use a calm and understanding tone
    Ask open-ended questions to help the user express their feelings
    Always prioritize safety, kindness, and emotional support

    Make sure that response is correctly formatted and never add context in answer.

    context: {context}
    User Query: {prompt}
    answer:
    """

    # Call Gemini via REST API
    bot_reply = call_gemini(llm_prompt)

    # Save bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
