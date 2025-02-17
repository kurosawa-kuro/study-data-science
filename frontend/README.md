
# 開発環境セットアップ
## 仮想環境
python3 -m venv myenv
source myenv/bin/activate
pip3 install --upgrade pip setuptools wheel

## パッケージインストール
pip3 install -r requirements.txt

## 依存関係の更新
pip freeze > requirements.txt

# アプリケーション実行
cd api
uvicorn main:app --reload

# 終了時
deactivate

pip3 install notebook
pip3 install streamlit
pip3 install gradio

jupyter notebook

streamlit run streamlit_micropost.py

python gradio/gradio_chatbot.py




