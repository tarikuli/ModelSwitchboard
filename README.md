# ModelSwitchboard

ModelSwitchboard is a Streamlit-based chatbot interface that lets you interact with a variety of large language models (LLMs) hosted on [OpenRouter.ai](https://openrouter.ai). The app makes it easy to experiment with and compare different AI models for chat-based tasks, all from a single, user-friendly web interface.

---

## 🚀 App Goal

The goal of ModelSwitchboard is to provide a simple way for users and teams to:
- Try out different LLMs (OpenAI, Anthropic, Google, Mistral, Meta, etc.) via OpenRouter.
- Compare model responses and behaviors side-by-side.
- Adjust model parameters (temperature, max tokens) for experimentation.

---

## 🛠️ How to Use

1. **Enter your OpenRouter API Key** in the sidebar to authenticate.
2. **Select a model** from the dropdown menu to choose which AI model you want to chat with.
3. **Adjust the temperature and max tokens** sliders to control the creativity and length of the responses.
4. **Type your question or prompt** in the chat input at the bottom and press Enter.
5. **View the conversation history** in the main area, showing both your messages and the model’s responses.

This setup makes it easy for anyone on the team to test different LLMs and settings for various use cases.

---

## 💻 Running Locally

1. **Create a Python virtual environment:**
    ```bash
    python -m venv .env
    ```

2. **Activate the virtual environment:**
    ```bash
    source .env/bin/activate
    ```

3. **Install the requirements:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the app:**
    ```bash
    streamlit run main.py
    ```

---

## 📋 Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [requests](https://pypi.org/project/requests/)

---

## 📝 Notes

- You need an [OpenRouter API key](https://openrouter.ai/) to use the app.
- The app fetches available models dynamically from OpenRouter, but falls back to a default list if the API is unavailable.

---

Enjoy experimenting with different LLMs!