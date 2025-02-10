import os
from dotenv import load_dotenv  # Load environment variables from .env
import gradio as gr
import openai

# Load environment variables from the .env file located in the same directory as this script.
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Set API keys from environment variables.
openai.api_key = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Flag for selecting API provider. Set to "openai" or "deepseek".
API_PROVIDER = os.getenv("API_PROVIDER", "openai").lower()

def openai_chat(user_message: str, history: list) -> tuple:
    """
    Call the OpenAI ChatCompletion API and return the updated conversation history.
    """
    if history is None:
        history = []
    # Append the user message to history
    history.append(("user", user_message))
    # Prepare messages in the format expected by OpenAI.
    messages = [{"role": role, "content": msg} for role, msg in history]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        # Use attribute access to retrieve the assistant's reply (new interface)
        assistant_reply = response.choices[0].message.content.strip()
    except Exception as e:
        assistant_reply = f"Error: {str(e)}"
    
    history.append(("assistant", assistant_reply))
    return history, history

def deepseek_chat(user_message: str, history: list) -> tuple:
    """
    Call the DeepSeek API (compatible with the OpenAI interface) and return the updated conversation history.
    Uses DeepSeek's official endpoint and model settings.
    """
    if history is None:
        history = []
    history.append(("user", user_message))
    messages = [{"role": role, "content": msg} for role, msg in history]

    try:
        # Call DeepSeek's API by overriding the api_base and model parameters.
        response = openai.ChatCompletion.create(
            api_key=DEEPSEEK_API_KEY,
            api_base="https://api.deepseek.com",
            model="deepseek-chat",
            messages=messages,
            temperature=0.7
        )
        assistant_reply = response.choices[0].message.content.strip()
    except Exception as e:
        assistant_reply = f"Error: {str(e)}"
    
    history.append(("assistant", assistant_reply))
    return history, history

def chat(user_message: str, history: list) -> tuple:
    """
    Dispatch the chat call based on the selected API provider.
    """
    if API_PROVIDER == "openai":
        return openai_chat(user_message, history)
    elif API_PROVIDER == "deepseek":
        return deepseek_chat(user_message, history)
    else:
        # If an unsupported API provider is set, return the history as-is.
        return history, history

with gr.Blocks() as demo:
    gr.Markdown("# AI Chatbot")
    # Chatbot UI component to display conversation history.
    chatbot = gr.Chatbot(label="Chatbot")
    # Text input component (only for text input, no image input).
    text_input = gr.Textbox(
        label="Your Message", 
        placeholder="Type your message here...", 
        interactive=True
    )
    # State component to manage conversation history.
    state = gr.State([])
    # When the user presses Enter or clicks the button, call the chat function.
    text_input.submit(fn=chat, inputs=[text_input, state], outputs=[chatbot, state])
    send_button = gr.Button("Send")
    send_button.click(fn=chat, inputs=[text_input, state], outputs=[chatbot, state])

if __name__ == "__main__":
    demo.launch()