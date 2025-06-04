import streamlit as st
import requests

st.set_page_config(page_title="OpenRouter Chatbot", layout="wide")


def sidebar():
    with st.sidebar:
        st.title("OpenRouter Chatbot")
        api_key = st.text_input("OpenRouter API Key", type="password")
        selected_model = st.selectbox("Choose a model", fetch_models())
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
        max_tokens = st.number_input(
            "Max Tokens", min_value=100, max_value=4096, value=1000)
        return api_key, selected_model, temperature, max_tokens


def fetch_models():
    """Fetch available models from OpenRouter API, fallback to default list on failure."""
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models", timeout=10)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            return [model["id"] for model in data["data"]]
        else:
            st.warning("No models found in API response.")
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not fetch models: {e}")
    # Fallback to a default list if API fails
    return [
        # "openai/gpt-4-turbo-preview",
        # "openai/gpt-4",
        # "openai/gpt-3.5-turbo",
        # "anthropic/claude-3-opus",
        # "anthropic/claude-3-sonnet",
        # "anthropic/claude-2.1",
        # "google/gemini-pro",
        # "mistralai/mistral-7b-instruct",
        # "meta-llama/llama-2-70b-chat"
    ]


def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_assistant_response(api_key, selected_model, temperature, max_tokens):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": selected_model,
        "messages": [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    try:
        response = requests.post(url, headers=headers,
                                 json=payload, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as req_err:
        st.error(f"Payload sent: {payload}")
        st.error(
            f"Response content: {getattr(req_err.response, 'text', None)}")
        raise RuntimeError(f"OpenRouter API error: {req_err}") from req_err
    return response.json()


def main():
    api_key, selected_model, temperature, max_tokens = sidebar()
    init_chat_history()
    display_chat()

    if prompt := st.chat_input("What would you like to ask?"):
        if not api_key:
            st.error("Please enter your OpenRouter API key")
            st.stop()
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                response = get_assistant_response(
                    api_key, selected_model, temperature, max_tokens)
                # Extract assistant reply from response
                if "choices" in response and len(response["choices"]) > 0:
                    full_response = response["choices"][0]["message"]["content"]
                    message_placeholder.markdown(full_response)
                else:
                    message_placeholder.markdown("No response from assistant.")
            except RuntimeError as e:
                st.error(f"An error occurred: {str(e)}")
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
