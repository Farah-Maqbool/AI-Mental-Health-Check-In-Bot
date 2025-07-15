import streamlit as st
from backend import retrieve_chunks
import google.generativeai as LLM

LLM.configure(api_key="AIzaSyAYnk8L9S2ahnE0GXggVMEOcRMUJHHsQkI")
config = {
            "temperature": 0.5,
            "response_mime_type": "text/plain"
        }
model = LLM.GenerativeModel('gemini-2.5-flash-preview-04-17',generation_config=config)

st.title("AI Mental Health Check In Bot")

