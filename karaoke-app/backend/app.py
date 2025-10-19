# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.recommendation import RecommendationService
from pathlib import Path
import os
import pandas as pd

app = Flask(__name__)

# =========================================
# CORS設定 - フロントエンドとの通信を許可
# =========================================
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:3001"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# =========================================
# グローバル変数（実際の運用では適切な初期化処理を）
# =========================================
song_catalog = None
recommendation_service = None

def initialize_services():
    """サービスを初期化"""
    global song_catalog, recommendation_service
    try:
        csv_path = Path(__file__).parent / "data" / "songs.csv"
        print(f"CSVファイル読み込み開始: {csv_path}")
        song_catalog = pd.read_csv(csv_path)
        print(f"CSV読み込み成功: {song_catalog.shape}")
        recommendation_service = RecommendationService(song_catalog)
        print("サービス初期化完了")
    except Exception as e:
        print(f"初期化エラー: {e}")
        import traceback
        traceback.print_exc()

# =========================================
# APIエンドポイント
# =========================================
@app.route("/api/recommend-songs", methods=["POST"])
def api_recommend_songs():
    """
    フロントエンドからのリクエスト形式:
    {
        "members": [
            {"id": "1", "nickname": "太郎", "gender": "male", "age": 25}
        ],
        "settings": {
            "mood": "upbeat",
            "situation": "party", 
            "micCount": 2
        }
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), 400

        members = data.get("members", [])
        settings = data.get("settings", {})

        if not members:
            return jsonify({"error": "Members are required"}), 400

        # サービスが初期化されていない場合は初期化
        if not recommendation_service:
            initialize_services()

        # 推薦を実行
        result = recommendation_service.recommend_songs(members, settings)

        return jsonify(result), 200

    except Exception as e:
        # エラーハンドリング
        import traceback
        error_details = traceback.format_exc()
        print(f"エラー詳細: {error_details}")
        return jsonify({"error": str(e), "details": error_details}), 500


# =========================================
# Flaskアプリ起動
# =========================================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
