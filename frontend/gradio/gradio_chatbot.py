import os
from typing import List, Tuple, Optional
from dotenv import load_dotenv  # Load environment variables from .env file.
import gradio as gr
import openai

# Data type for conversation history
ConversationHistory = List[Tuple[str, str]]

def load_configuration() -> Tuple[Optional[str], str]:
    """
    Load configuration from .env file and return DeepSeek API key and selected API provider.
    """
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    # Set OpenAI API key from env variable.
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # Retrieve DeepSeek API key and API provider.
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    api_provider = os.getenv("API_PROVIDER", "openai").lower()
    return deepseek_api_key, api_provider

def prepare_messages(history: ConversationHistory) -> List[dict]:
    """
    Convert conversation history to the list of messages expected by the API.
    """
    return [{"role": role, "content": msg} for role, msg in history]

class ChatService:
    """
    Abstract ChatService to handle chat interactions.
    """
    def send_chat(self, user_message: str, history: Optional[ConversationHistory]) -> Tuple[ConversationHistory, ConversationHistory]:
        """
        Abstract method to send a chat message and update conversation history.
        """
        raise NotImplementedError("send_chat must be implemented in subclass.")

class OpenAIChatService(ChatService):
    """
    Chat service implementation for OpenAI.
    """
    def send_chat(self, user_message: str, history: Optional[ConversationHistory]) -> Tuple[ConversationHistory, ConversationHistory]:
        if history is None:
            history = []  # Initialize history if None
        # Add user message to conversation history.
        history.append(("user", user_message))
        messages = prepare_messages(history)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7
            )
            # Retrieve the assistant's reply.
            assistant_reply = response.choices[0].message.content.strip()
        except Exception as e:
            assistant_reply = f"Error: {str(e)}"
        # Append assistant reply to conversation history.
        history.append(("assistant", assistant_reply))
        return history, history

class DeepSeekChatService(ChatService):
    """
    Chat service implementation for DeepSeek.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key

    def send_chat(self, user_message: str, history: Optional[ConversationHistory]) -> Tuple[ConversationHistory, ConversationHistory]:
        if history is None:
            history = []  # Initialize history if None
        # Add user message to conversation history.
        history.append(("user", user_message))
        messages = prepare_messages(history)
        try:
            response = openai.ChatCompletion.create(
                api_key=self.api_key,
                api_base="https://api.deepseek.com",
                model="deepseek-chat",
                messages=messages,
                temperature=0.7
            )
            # Retrieve the assistant's reply.
            assistant_reply = response.choices[0].message.content.strip()
        except Exception as e:
            assistant_reply = f"Error: {str(e)}"
        # Append assistant reply to conversation history.
        history.append(("assistant", assistant_reply))
        return history, history

def get_chat_service(api_provider: str, deepseek_api_key: Optional[str]) -> ChatService:
    """
    Factory function to get the appropriate ChatService based on the API provider.
    """
    if api_provider == "openai":
        return OpenAIChatService()
    elif api_provider == "deepseek":
        if deepseek_api_key is None:
            raise ValueError("DEEPSEEK_API_KEY must be provided for DeepSeek provider.")
        return DeepSeekChatService(deepseek_api_key)
    else:
        raise ValueError(f"Unsupported API provider: {api_provider}")

# Load configuration and obtain the proper chat service.
deepseek_api_key, api_provider = load_configuration()
chat_service = get_chat_service(api_provider, deepseek_api_key)

def chat(user_message: str, history: Optional[ConversationHistory]) -> Tuple[ConversationHistory, ConversationHistory]:
    """
    Dispatch chat to the appropriate chat service.
    """
    return chat_service.send_chat(user_message, history)

# Set up Gradio UI components.
with gr.Blocks() as demo:
    gr.Markdown("# AI Chatbot")
    # 表示用のマークダウンコンポーネントで、使用中のAPIプロバイダーをユーザーに明示
    gr.Markdown(f"**使用中のAIモデル API:** {api_provider.upper()}")
    # Chatbot UI component to display conversation history.
    chatbot = gr.Chatbot(label="Chatbot")
    # Text input component.
    text_input = gr.Textbox(
        label="Your Message",
        placeholder="Type your message here...",
        interactive=True
    )
    # State component to manage conversation history.
    state = gr.State([])
    # Bind the chat message submit action.
    text_input.submit(fn=chat, inputs=[text_input, state], outputs=[chatbot, state])
    send_button = gr.Button("Send")
    send_button.click(fn=chat, inputs=[text_input, state], outputs=[chatbot, state])

if __name__ == "__main__":
    demo.launch()