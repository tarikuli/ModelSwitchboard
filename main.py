
import streamlit as st
import openai
import os
from openai import OpenAI

# Set up the page
st.set_page_config(page_title="OpenRouter Chatbot", layout="wide")

# Sidebar for model selection and API key input
with st.sidebar:
    st.title("OpenRouter Chatbot")
    
    # API key input
    api_key = st.text_input("OpenRouter API Key", type="password")
    
    # Model selection dropdown
    models = [
        "openai/gpt-4-turbo-preview",
        "openai/gpt-4",
        "openai/gpt-3.5-turbo",
        "anthropic/claude-3-opus",
        "anthropic/claude-3-sonnet",
        "anthropic/claude-2.1",
        "google/gemini-pro",
        "mistralai/mistral-7b-instruct",
        "meta-llama/llama-2-70b-chat"
    ]
    selected_model = st.selectbox("Choose a model", models)
    
    # Additional options
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.number_input("Max Tokens", min_value=100, max_value=4096, value=1000)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    if not api_key:
        st.error("Please enter your OpenRouter API key")
        st.stop()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Initialize the OpenAI client with OpenRouter
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            
            # Get the response from OpenRouter
            response = client.chat.completions.create(
                model=selected_model,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            # Stream the response
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
