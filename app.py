import os
from flask import Flask, request, jsonify
from supabase import create_client, Client
from flask_cors import CORS
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# Flaskアプリを初期化
app = Flask(__name__)
# CORSを有効にし、どのオリジンからのリクエストも許可する
CORS(app)

# Supabaseの接続情報を環境変数から取得
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_KEY")

# === ここからデバッグ用のコードです ===
print("--- Supabase Connection Info ---")
print(f"URL: {url}")
if key:
    # キー全体は表示せず、読み込めたかと末尾4文字だけ表示
    print(f"Key Loaded: True (ends with: {key[-4:]})")
else:
    print("Key Loaded: False")
print("---------------------------------")
# =================================

# URLかキーが読み込めていない場合は、ここで処理を止めることもできますが、
# まずはログで確認します。
if not url or not key:
    print("CRITICAL ERROR: SUPABASE_URL or SUPABASE_SERVICE_KEY not found.")
    print("Please check if the .env file exists and is in the same directory as app.py.")

# Supabaseクライアントを作成
supabase: Client = create_client(url, key)


# /record-visit というエンドポイントを作成
@app.route("/record-visit", methods=["POST"])
def record_visit():
    try:
        # リクエストのJSONボディからデータを取得
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
            
        line_user_id = data.get("lineUserId")
        memo = data.get("memo")
        #memo = "これはPythonからのテストです" # ← この行を新しく追加

        if not line_user_id:
            return jsonify({"error": "lineUserId is required"}), 400

        # Supabaseの'visits'テーブルにデータを挿入
        response = supabase.table('line_miniapp_visits').insert({
            "line_user_id": line_user_id,
            "memo": memo
        }).execute()
        
        if response.data:
            return jsonify({"message": "訪問記録を保存しました！"}), 200
        else:
            print(f"Supabase response error: {response}") # エラー時のレスポンスを詳しく表示
            return jsonify({"error": "Failed to insert data into Supabase"}), 500

    except Exception as e:
        print(f"An error occurred in record_visit: {e}")
        return jsonify({"error": str(e)}), 500
# ローカルでテスト実行するための設定
if __name__ == "__main__":
    app.run(debug=True, port=5001)