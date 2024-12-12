import logging
import os
from dotenv import load_dotenv
import openai

# 環境変数の読み込み
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AkinatorGame:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("APIキーが設定されていません。")
        
        openai.api_key = self.api_key
        self.messages = []
        self.question_count = 0
        self.max_questions = 25

    def initialize_game(self):
        """ゲームの初期化"""
        system_message = """
        あなたは「アキネーター」のような出題者です。以下のルールに従ってゲームを進行してください：
        1.お題を以下から選び、まずユーザーに教えてください。
           - 実在の有名人（現代または歴史上の人物）
           - 動物（実在の生物）
           - 食べ物や飲み物
           - 場所（国、都市、建造物など）
        2. プレイヤーからの質問には、以下の5つの返答のいずれかで答えてください：
           - はい
           - いいえ
           - 部分的にそう
           - 部分的に違う
           - わからない
        3. 最後にプレイヤーが答えを言った時、正解かどうかを判断してください。
        """
        self.messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": "新しいゲームを始めます。お題を1つ選んでください。その特徴を記録してください。選んだら1.お題を教えてゲームを始めてください。"}
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=self.messages
            )
            self.messages.append({"role": "assistant", "content": response.choices[0].message.content})
            self.question_count = 0
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error initializing game: {e}")
            return f"エラーが発生しました: {e}"

    def chat_with_gpt(self, user_message):
        """ユーザーの質問や回答をGPTに送信し、応答を受け取る"""
        if self.question_count >= self.max_questions:
            return "質問の制限回数に達しました。答えを入力してください。"

        try:
            self.question_count += 1
            self.messages.append({"role": "user", "content": user_message})

            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=self.messages
            )

            assistant_message = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": assistant_message})

            return assistant_message
        except Exception as e:
            logger.error(f"Error during chat: {e}")
            return f"エラーが発生しました: {e}"


# チャット形式の実行ロジック
if __name__ == "__main__":
    game = AkinatorGame()

    # ゲーム初期化
    print("=== Akinator Game ===")
    print(game.initialize_game())

    # チャット形式で進行
    while True:
        user_input = input("\nあなた: ")
        if user_input.lower() in ["終了", "exit", "quit"]:
            print("ゲームを終了します。ありがとうございました！")
            break
        response = game.chat_with_gpt(user_input)
        print(f"アキネーター: {response}")
