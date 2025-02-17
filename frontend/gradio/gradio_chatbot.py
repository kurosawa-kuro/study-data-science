import os
from typing import List, Tuple, Optional, Literal
from dotenv import load_dotenv  # Load environment variables from .env file.
import gradio as gr
import openai

# Constant flag for DeepSeek model selection.
# Set to True to use 'deepseek-chat', or False to use 'deepseek-reasoner'
USE_DEEPSEEK_CHAT_MODEL: bool = False

# Data type for conversation history
ConversationHistory = List[Tuple[str, str]]

# 定数定義
API_PROVIDERS = Literal["openai", "deepseek"]
DEFAULT_MODEL = "gpt-3.5-turbo"
DEEPSEEK_API_BASE = "https://api.deepseek.com"
DEFAULT_TEMPERATURE = 0.7

class ConfigManager:
    """環境変数と設定の管理を担当するクラス"""
    
    def __init__(self):
        self._load_environment()
        
    def _load_environment(self) -> None:
        """環境変数をロード"""
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(dotenv_path)
        
    def get_api_keys(self) -> Tuple[Optional[str], str]:
        """APIキーとプロバイダーを取得"""
        openai.api_key = os.getenv("OPENAI_API_KEY")
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        api_provider = os.getenv("API_PROVIDER", "openai").lower()
        return deepseek_api_key, api_provider

class ChatServiceFactory:
    """適切なチャットサービスを生成するファクトリクラス"""
    
    @staticmethod
    def create_service(api_provider: API_PROVIDERS, deepseek_api_key: Optional[str]) -> "ChatService":
        """APIプロバイダーに基づいて適切なチャットサービスを生成"""
        if api_provider == "openai":
            return OpenAIChatService()
        elif api_provider == "deepseek":
            if not deepseek_api_key:
                raise ValueError("DeepSeek APIキーが必要です")
            return DeepSeekChatService(deepseek_api_key)
        raise ValueError(f"サポートされていないAPIプロバイダー: {api_provider}")

class ChatService:
    """チャットサービスの基底クラス"""
    
    def send_chat(self, user_message: str, history: Optional[List[Tuple[str, str]]]) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        """チャットメッセージを送信し、会話履歴を更新"""
        raise NotImplementedError("サブクラスで実装が必要です")
    
    def _prepare_messages(self, history: List[Tuple[str, str]]) -> List[dict]:
        """会話履歴をAPI用のメッセージ形式に変換"""
        return [{"role": role, "content": msg} for role, msg in history]

    def get_model_name(self) -> str:
        raise NotImplementedError("サブクラスで実装が必要です")

class OpenAIChatService(ChatService):
    """OpenAI用のチャットサービス実装"""
    
    def get_model_name(self) -> str:
        return DEFAULT_MODEL

    def send_chat(self, user_message: str, history: Optional[List[Tuple[str, str]]]) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        history = history or []
        history.append(("user", user_message))
        
        try:
            response = openai.ChatCompletion.create(
                model=DEFAULT_MODEL,
                messages=self._prepare_messages(history),
                temperature=DEFAULT_TEMPERATURE
            )
            assistant_reply = response.choices[0].message.content.strip()
        except Exception as e:
            assistant_reply = f"エラーが発生しました: {str(e)}"
            
        history.append(("assistant", assistant_reply))
        return history, history

class DeepSeekChatService(ChatService):
    """DeepSeek用のチャットサービス実装"""
    
    def get_model_name(self) -> str:
        return "deepseek-chat" if USE_DEEPSEEK_CHAT_MODEL else "deepseek-reasoner"

    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def send_chat(self, user_message: str, history: Optional[List[Tuple[str, str]]]) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        history = history or []
        history.append(("user", user_message))
        
        model_name = "deepseek-chat" if USE_DEEPSEEK_CHAT_MODEL else "deepseek-reasoner"
        try:
            response = openai.ChatCompletion.create(
                api_key=self.api_key,
                api_base=DEEPSEEK_API_BASE,
                model=model_name,
                messages=self._prepare_messages(history),
                temperature=DEFAULT_TEMPERATURE
            )
            assistant_reply = response.choices[0].message.content.strip()
        except Exception as e:
            assistant_reply = f"エラーが発生しました: {str(e)}"
            
        history.append(("assistant", assistant_reply))
        return history, history

# 初期化処理
config_manager = ConfigManager()
deepseek_api_key, api_provider = config_manager.get_api_keys()
chat_service = ChatServiceFactory.create_service(api_provider, deepseek_api_key)

def chat(user_message: str, history: Optional[List[Tuple[str, str]]]) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    """チャットメッセージを処理し、更新された会話履歴を返す"""
    return chat_service.send_chat(user_message, history)

# Set up Gradio UI components.
with gr.Blocks() as demo:
    gr.Markdown("# AI Chatbot")
    # Display the currently used API provider and model to the user.
    gr.Markdown(f"**使用中のAIモデル:** {api_provider.upper()} ({chat_service.get_model_name()})")
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