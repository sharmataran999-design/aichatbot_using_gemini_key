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

# Handle user input
if prompt := st.chat_input("Type your message..."):
    # Display user message in UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response using Interactions API
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        try:
            interaction = st.session_state.client.interactions.create(
                model="gemini-2.5-flash",
                input=prompt
            )
            
            full_response = interaction.text
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")