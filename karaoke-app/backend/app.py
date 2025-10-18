from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import csv
from typing import List, Dict, Any
import os

app = Flask(__name__)

# CORS設定 - フロントエンドとの通信を許可
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:3001"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})


# =========================================
# 🎵 外部CSVから曲データを読み込む関数
# =========================================
def load_song_database(csv_path: str) -> Dict[str, List[Dict[str, Any]]]:
    database = {}
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            decade = row["decade"]
            if decade not in database:
                database[decade] = []
            database[decade].append({
                "title": row["title"],
                "artist": row["artist"],
                "year": int(row["year"]),
                "genre": row["genre"],
                # ムードをカンマ区切りでリストに変換
                "mood": [m.strip() for m in row["mood"].split(",") if m.strip()]
            })
    return database


# =========================================
# 🎼 データベースを ./backend/data/songs.csv から読み込み
# =========================================
SONG_CSV_PATH = os.path.join(os.path.dirname(__file__), "backend", "data", "songs.csv")
SONG_DATABASE = load_song_database(SONG_CSV_PATH)
