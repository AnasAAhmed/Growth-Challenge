import streamlit as st
from PIL import Image
import google.generativeai as genai
from io import BytesIO
import requests


genai.configure(api_key=st.secrets['GEMINI_API_KEY'])

st.set_page_config(page_title='ImageWrite | Chatbot', layout='wide')
st.title('📝Chatbot, GIAIC Growth Challenge.')
st.write('provide a prompt to get AI-generated insights in chunks using streaming logic!')
model = genai.GenerativeModel("gemini-1.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input field
prompt = st.chat_input("Type your message here...")

if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare conversation history for Gemini
    conversation_history = [
        {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages
    ]

    # AI Response with Streaming
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response_stream = model.generate_content(conversation_history, stream=True)
                
                ai_response = ""  # Store AI response dynamically
                response_placeholder = st.empty()

                for chunk in response_stream:
                    if chunk.text:
                        ai_response += chunk.text  
                        response_placeholder.markdown(ai_response)

                # Save AI response to history
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")