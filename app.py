import streamlit as st
from backend import retrieve_chunks
import google.generativeai as LLM

LLM.configure(api_key="AIzaSyAYnk8L9S2ahnE0GXggVMEOcRMUJHHsQkI")
config = {
            "temperature": 0.5,
            "response_mime_type": "text/plain"
        }
model = LLM.GenerativeModel('gemini-2.5-pro',generation_config=config)

st.title("AI Mental Health Check In Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your message here..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate bot reply (replace with your model logic)
    rag = retrieve_chunks(prompt)
    context = "\n\n".join(rag)
    
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

    make sure that response is correctly formatted and never add context in answer

    context: {context}
    User Query: {prompt}
    answer:

    """
    response = model.generate_content(llm_prompt)
    bot_reply = response.text    

    # Save bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
