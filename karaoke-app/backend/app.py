# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.recommendation import recommend_song  # ビジネスロジックを呼び出す
import os

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
# APIエンドポイント
# =========================================
@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    """
    リクエストJSON例:
    {
        "age": 25,
        "gender": "女性",
        "mood": "happy"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), 400

        # services/recommendation.py の関数を呼び出す
        recommended_song = recommend_song(
            age=data.get("age"),
            gender=data.get("gender"),
            mood=data.get("mood")
        )

        return jsonify(recommended_song), 200

    except Exception as e:
        # エラーハンドリング
        return jsonify({"error": str(e)}), 500


# =========================================
# Flaskアプリ起動
# =========================================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
