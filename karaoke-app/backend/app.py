from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from typing import List, Dict, Any

app = Flask(__name__)

# CORS設定 - フロントエンドとの通信を許可
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:3001"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# 年代別の曲データベース
SONG_DATABASE = {
    "1990s": [
        {"title": "LOVEマシーン", "artist": "モーニング娘。", "year": 1999, "genre": "J-Pop", "mood": ["盛り上がる", "元気"]},
        {"title": "TSUNAMI", "artist": "サザンオールスターズ", "year": 2000, "genre": "J-Pop", "mood": ["懐かしい", "盛り上がる"]},
        {"title": "CAN YOU CELEBRATE?", "artist": "安室奈美恵", "year": 1997, "genre": "J-Pop", "mood": ["しっとり", "懐かしい"]},
        {"title": "White Love", "artist": "SPEED", "year": 1997, "genre": "J-Pop", "mood": ["しっとり", "懐かしい"]},
        {"title": "HOWEVER", "artist": "GLAY", "year": 1997, "genre": "Rock", "mood": ["盛り上がる", "元気"]},
    ],
    "2000s": [
        {"title": "世界に一つだけの花", "artist": "SMAP", "year": 2003, "genre": "J-Pop", "mood": ["元気", "リラックス"]},
        {"title": "Flavor Of Life", "artist": "宇多田ヒカル", "year": 2007, "genre": "J-Pop", "mood": ["しっとり", "リラックス"]},
        {"title": "千の風になって", "artist": "秋川雅史", "year": 2006, "genre": "Ballad", "mood": ["しっとり", "懐かしい"]},
        {"title": "ハナミズキ", "artist": "一青窈", "year": 2004, "genre": "J-Pop", "mood": ["しっとり", "リラックス"]},
        {"title": "そばにいるね", "artist": "青山テルマ feat. SoulJa", "year": 2008, "genre": "R&B", "mood": ["しっとり", "リラックス"]},
    ],
    "2010s": [
        {"title": "恋", "artist": "星野源", "year": 2016, "genre": "J-Pop", "mood": ["盛り上がる", "元気"]},
        {"title": "Pretender", "artist": "Official髭男dism", "year": 2019, "genre": "J-Pop", "mood": ["しっとり", "盛り上がる"]},
        {"title": "Lemon", "artist": "米津玄師", "year": 2018, "genre": "J-Pop", "mood": ["しっとり", "懐かしい"]},
        {"title": "前前前世", "artist": "RADWIMPS", "year": 2016, "genre": "Rock", "mood": ["盛り上がる", "元気"]},
        {"title": "366日", "artist": "HY", "year": 2008, "genre": "J-Pop", "mood": ["しっとり", "リラックス"]},
    ],
    "2020s": [
        {"title": "ドライフラワー", "artist": "優里", "year": 2020, "genre": "J-Pop", "mood": ["しっとり", "懐かしい"]},
        {"title": "KICK BACK", "artist": "米津玄師", "year": 2022, "genre": "Rock", "mood": ["盛り上がる", "元気"]},
        {"title": "アイドル", "artist": "YOASOBI", "year": 2023, "genre": "J-Pop", "mood": ["盛り上がる", "元気"]},
        {"title": "怪獣の花唄", "artist": "Vaundy", "year": 2020, "genre": "J-Pop", "mood": ["リラックス", "元気"]},
        {"title": "残響散歌", "artist": "Aimer", "year": 2021, "genre": "Rock", "mood": ["盛り上がる", "しっとり"]},
    ],
}


def determine_decade(members: List[Dict[str, Any]]) -> str:
    """メンバーの平均年齢から最適な年代を決定"""
    if not members:
        return "2020s"
    
    avg_age = sum(member["age"] for member in members) / len(members)
    
    if avg_age >= 45:
        return "1990s"
    elif avg_age >= 35:
        return "2000s"
    elif avg_age >= 25:
        return "2010s"
    else:
        return "2020s"


def select_song(decade: str, mood: str) -> Dict[str, Any]:
    """年代とムードに基づいて曲を選択"""
    songs = SONG_DATABASE.get(decade, SONG_DATABASE["2020s"])
    
    # ムードに合う曲をフィルタリング
    matching_songs = [song for song in songs if mood in song["mood"]]
    
    # マッチする曲がない場合は全曲から選択
    if not matching_songs:
        matching_songs = songs
    
    return random.choice(matching_songs)


def select_singers(members: List[Dict[str, Any]], mic_count: int) -> List[Dict[str, Any]]:
    """歌う人をランダムに選択"""
    shuffled = members.copy()
    random.shuffle(shuffled)
    return shuffled[:min(mic_count, len(members))]


@app.route("/api/health", methods=["GET"])
def health_check():
    """ヘルスチェックエンドポイント"""
    return jsonify({"status": "ok", "message": "Flask backend is running"}), 200


@app.route("/api/recommend", methods=["POST"])
def recommend():
    """曲とシンガーを推薦するメインエンドポイント"""
    try:
        # リクエストデータの取得
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "リクエストボディが空です"}), 400
        
        members = data.get("members", [])
        settings = data.get("settings", {})
        
        # バリデーション
        if not members:
            return jsonify({"error": "メンバー情報が必要です"}), 400
        
        if not settings:
            return jsonify({"error": "設定情報が必要です"}), 400
        
        mood = settings.get("mood", "盛り上がる")
        situation = settings.get("situation", "飲み会")
        mic_count = settings.get("micCount", 1)
        
        # 年代を決定
        decade = determine_decade(members)
        
        # 曲を選択
        selected_song = select_song(decade, mood)
        
        # 歌う人を選択
        selected_singers = select_singers(members, mic_count)
        
        # レスポンスを返す
        response = {
            "song": selected_song,
            "singers": selected_singers,
            "metadata": {
                "decade": decade,
                "mood": mood,
                "situation": situation,
                "totalMembers": len(members)
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        # エラーハンドリング
        app.logger.error(f"Error in recommend endpoint: {str(e)}")
        return jsonify({"error": "サーバーエラーが発生しました", "details": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """404エラーハンドラー"""
    return jsonify({"error": "エンドポイントが見つかりません"}), 404


@app.errorhandler(500)
def internal_error(error):
    """500エラーハンドラー"""
    return jsonify({"error": "内部サーバーエラー"}), 500


if __name__ == "__main__":
    # 開発環境での実行
    app.run(debug=True, host="0.0.0.0", port=5000)
