import os
from typing import List, Tuple, Optional, Literal
from dotenv import load_dotenv  # Load environment variables from .env file.
import gradio as gr
import openai
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Constant flag for DeepSeek model selection.
# Set to True to use 'deepseek-chat', or False to use 'deepseek-reasoner'
USE_DEEPSEEK_CHAT_MODEL: bool = False

# Data type for conversation history
# ※ 今回は各メッセージを辞書形式に変更
ConversationHistory = List[dict]

# 定数定義
API_PROVIDERS = Literal["openai", "deepseek"]
DEFAULT_MODEL = "gpt-3.5-turbo"
DEEPSEEK_API_BASE = "https://api.deepseek.com"
DEFAULT_TEMPERATURE = 0.7

# SQLiteデータベースの設定
Base = declarative_base()

class ChatHistory(Base):
    """チャット履歴を保存するデータベースモデル"""
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    model_name = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# データベースエンジンの初期化
engine = create_engine("sqlite:///chat_history.db", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class ChatHistoryManager:
    """チャット履歴の管理を担当するクラス"""
    
    def __init__(self):
        self.session = Session()
        
    def save_chat(self, question: str, answer: str, model_name: str) -> None:
        """チャット履歴をデータベースに保存"""
        new_entry = ChatHistory(
            question=question,
            answer=answer,
            model_name=model_name
        )
        self.session.add(new_entry)
        self.session.commit()
        
    def get_history(self) -> List[ChatHistory]:
        """チャット履歴を取得"""
        return self.session.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).all()
    
    def close(self) -> None:
        """セッションを閉じる"""
        self.session.close()

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
    def create_service(api_provider: API_PROVIDERS, deepseek_api_key: Optional[str], history_manager: ChatHistoryManager) -> "ChatService":
        """APIプロバイダーに基づいて適切なチャットサービスを生成"""
        if api_provider == "openai":
            return OpenAIChatService(history_manager)
        elif api_provider == "deepseek":
            if not deepseek_api_key:
                raise ValueError("DeepSeek APIキーが必要です")
            return DeepSeekChatService(deepseek_api_key, history_manager)
        raise ValueError(f"サポートされていないAPIプロバイダー: {api_provider}")

class ChatService:
    """チャットサービスの基底クラス"""
    
    def send_chat(self, user_message: str, history: Optional[ConversationHistory]) -> Tuple[ConversationHistory, ConversationHistory]:
        """チャットメッセージを送信し、会話履歴を更新"""
        raise NotImplementedError("サブクラスで実装が必要です")
    
    def get_model_name(self) -> str:
        raise NotImplementedError("サブクラスで実装が必要です")

class OpenAIChatService(ChatService):
    """OpenAI用のチャットサービス実装"""
    
    def __init__(self, history_manager: ChatHistoryManager):
        self.history_manager = history_manager
        
    def get_model_name(self) -> str:
        return DEFAULT_MODEL

    def send_chat(self, user_message: str, history: Optional[ConversationHistory]) -> Tuple[ConversationHistory, ConversationHistory]:
        history = history or []
        # 会話状態を辞書形式で更新
        history.append({"role": "user", "content": user_message})
        
        try:
            response = openai.ChatCompletion.create(
                model=DEFAULT_MODEL,
                messages=history,
                temperature=DEFAULT_TEMPERATURE
            )
            assistant_reply = response.choices[0].message.content.strip()
        except Exception as e:
            assistant_reply = f"エラーが発生しました: {str(e)}"
            
        history.append({"role": "assistant", "content": assistant_reply})
        # チャット履歴を保存（DBにはテキスト部分のみ記録）
        self.history_manager.save_chat(user_message, assistant_reply, self.get_model_name())
        return history, history

class DeepSeekChatService(ChatService):
    """DeepSeek用のチャットサービス実装"""
    
    def __init__(self, api_key: str, history_manager: ChatHistoryManager):
        self.api_key = api_key
        self.history_manager = history_manager
        
    def get_model_name(self) -> str:
        return "deepseek-chat" if USE_DEEPSEEK_CHAT_MODEL else "deepseek-reasoner"

    def send_chat(self, user_message: str, history: Optional[ConversationHistory]) -> Tuple[ConversationHistory, ConversationHistory]:
        history = history or []
        history.append({"role": "user", "content": user_message})
        
        model_name = "deepseek-chat" if USE_DEEPSEEK_CHAT_MODEL else "deepseek-reasoner"
        try:
            response = openai.ChatCompletion.create(
                api_key=self.api_key,
                api_base=DEEPSEEK_API_BASE,
                model=model_name,
                messages=history,
                temperature=DEFAULT_TEMPERATURE
            )
            assistant_reply = response.choices[0].message.content.strip()
        except Exception as e:
            # DeepSeek APIのエラー原因を取得・表示する
            error_detail = getattr(e, 'response', None)
            if error_detail is not None:
                try:
                    error_text = error_detail.text
                except Exception:
                    error_text = str(error_detail)
            else:
                error_text = str(e)
            assistant_reply = f"エラーが発生しました: {error_text}"
            
        history.append({"role": "assistant", "content": assistant_reply})
        self.history_manager.save_chat(user_message, assistant_reply, self.get_model_name())
        return history, history

# 初期化処理
config_manager = ConfigManager()
deepseek_api_key, api_provider = config_manager.get_api_keys()
history_manager = ChatHistoryManager()
chat_service = ChatServiceFactory.create_service(api_provider, deepseek_api_key, history_manager)

def chat(user_message: str, history: Optional[ConversationHistory]) -> Tuple[ConversationHistory, ConversationHistory]:
    """チャットメッセージを処理し、更新された会話履歴を返す"""
    return chat_service.send_chat(user_message, history)

def toggle_history(history_display):
    """チャット履歴の表示/非表示を切り替える"""
    new_visibility = not history_display.visible
    if new_visibility:
        history = history_manager.get_history()
        history_data = [
            [h.id, h.question, h.answer, h.model_name, h.timestamp.strftime("%Y-%m-%d %H:%M:%S")]
            for h in history
        ]
        return gr.update(visible=True, value=history_data)
    return gr.update(visible=False)

# Set up Gradio UI components.
with gr.Blocks() as demo:
    gr.Markdown("# AI Chatbot")
    gr.Markdown(f"**使用中のAIモデル:** {api_provider.upper()} ({chat_service.get_model_name()})")
    
    # Chatbotコンポーネントを新しい形式で初期化
    chatbot = gr.Chatbot(label="Chatbot", type="messages")
    
    # チャット履歴表示用のコンポーネント
    history_display = gr.Dataframe(
        headers=["ID", "質問", "回答", "モデル", "日時"],
        interactive=False,
        visible=False
    )
    
    with gr.Row():
        # redundant chatbot initialization commented out
        # chatbot = gr.Chatbot(label="Chatbot")
        history_display = gr.Dataframe(
            headers=["ID", "質問", "回答", "モデル", "日時"],
            interactive=False,
            visible=False
        )
    
    with gr.Row():
        text_input = gr.Textbox(
            label="Your Message",
            placeholder="Type your message here...",
            interactive=True
        )
        history_button = gr.Button("履歴表示")
    
    state = gr.State([])
    
    text_input.submit(fn=chat, inputs=[text_input, state], outputs=[chatbot, state])
    send_button = gr.Button("Send")
    send_button.click(fn=chat, inputs=[text_input, state], outputs=[chatbot, state])
    history_button.click(
        fn=toggle_history,
        inputs=[history_display],
        outputs=[history_display]  # gr.update() を使うので .visible は不要
    )

if __name__ == "__main__":
    try:
        demo.launch()
    finally:
        history_manager.close()