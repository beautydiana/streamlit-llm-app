import streamlit as st
from dotenv import load_dotenv
import os

# .env 明示的に読み込み（パス指定）
dotenv_loaded = load_dotenv(dotenv_path=".env")

# 読み込まれたかログに出す
print("✅ dotenv loaded:", dotenv_loaded)

# APIキーを確認
api_key = os.getenv("OPENAI_API_KEY")
print("🔑 API KEY:", api_key)

if not api_key:
    st.error("❌ OpenAI APIキーが読み込まれていません。'.env' ファイルを確認してください。")
    st.stop()


# LangChain
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# LLMモデルのインスタンス生成
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7, model_name="gpt-3.5-turbo")

# タイトルと説明
st.title("💬 LLM相談アプリ")
st.markdown("以下のフォームに質問を入力し、相談したい専門家を選択してください。")

# 専門家の選択肢
expert = st.radio("専門家の種類を選んでください：", ("心理カウンセラー", "ビジネスコンサルタント", "健康アドバイザー"))

# 質問フォーム
user_input = st.text_input("質問を入力してください：")

# 専門家別プロンプト設定関数
def get_response(expert_role, user_text):
    role_dict = {
        "心理カウンセラー": "あなたは思いやりのある心理カウンセラーです。相談者の気持ちに寄り添って答えてください。",
        "ビジネスコンサルタント": "あなたは戦略的思考に優れたビジネスコンサルタントです。論理的かつ実践的なアドバイスをしてください。",
        "健康アドバイザー": "あなたは信頼される健康アドバイザーです。健康と生活習慣に関する知識をもとに回答してください。"
    }

    system_msg = SystemMessage(content=role_dict[expert_role])
    user_msg = HumanMessage(content=user_text)

    try:
        return llm([system_msg, user_msg]).content
    except Exception as e:
        return f"❌ エラーが発生しました: {e}"

# 実行ボタン
if st.button("送信"):
    if user_input.strip() != "":
        with st.spinner("LLMが回答を生成中です..."):
            answer = get_response(expert, user_input)
            st.markdown("#### 回答：")
            st.info(answer)
    else:
        st.warning("質問を入力してください。")
