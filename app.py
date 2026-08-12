import os
import streamlit as st
from google import genai

# Page configuration
st.set_page_config(page_title="Gemini Assistant", page_icon="🤖", layout="centered")
st.title("🤖 Gemini AI Assistant")

# Safely retrieve API Key from either Environment or Streamlit Secrets
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please set your GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# Initialize GenAI client
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)

# Store message history for UI rendering
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Candidate models to attempt in order
CANDIDATE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-flash"
]

# Handle user input
if prompt := st.chat_input("Type your message..."):
    # Display user message in UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        success = False

        # Build message payload from history
        contents = [{"role": m["role"], "parts": [{"text": m["content"]}]} for m in st.session_state.messages]

        # Try candidate models until one succeeds
        for model_name in CANDIDATE_MODELS:
            try:
                response = st.session_state.client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response.text:
                    full_response = response.text
                    response_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    success = True
                    break
            except Exception as e:
                continue

        if not success:
            st.error("Unable to connect to Gemini models. Please check your API key permissions in Google AI Studio.")