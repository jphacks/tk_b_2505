from typing import List, Dict, Optional, Tuple
import random
from models.song import SongCatalog, Song
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np


class RecommendationService:
    """
    カラオケ選曲のビジネスロジック
    """
    
    def __init__(self, song_catalog: pd):
        self.song_catalog = song_catalog
    
    def recommend_songs(self, members: List[Dict], settings: Dict) -> Dict:
        """
        メンバーと設定に基づいて曲と歌う人を推薦
        
        Args:
            members: メンバーリスト [{"id": "1", "nickname": "太郎", "gender": "male", "age": 25}]
            settings: 設定 {"mood": "upbeat", "micCount": 2}
            
        Returns:
            推薦結果 {"selectedSong": {...}, "selectedSingers": [...]}
        """
        # 1. 年を出力
        year = self._determine_year(members, settings)
        
        # 2. 性別グループ番号を出力
        gender = self._divide_gender(members)

        # 3. シチュエーションからムード番号を出力
        mood = self._determine_mood(settings)
        
        
        # 4. 

        # ===== 1. データ読み込み =====
        df = self.song_catalog

        # ===== 2. 年代グループ分け =====
        showa_group = df[df["year"] < 1990].copy()                   # 昭和歌謡
        classic_group = df[(df["year"] >= 1990) & (df["year"] <= 2022)].copy()  # 定番
        latest_group = df[df["year"] >= 2023].copy()                # 最新曲


        def _cluster(df_group):
            if df_group.empty:
                return None, None, None, None, None

            # カテゴリ数値化
            le_gender = LabelEncoder()
            le_mood = LabelEncoder()
            df_group["gender_enc"] = le_gender.fit_transform(df_group["gender"])
            df_group["mood_enc"] = le_mood.fit_transform(df_group["mood_tags"])
            
            # 年代を0-1スケーリング
            df_group["year_scaled"] = (df_group["year"] - df_group["year"].min()) / (df_group["year"].max() - df_group["year"].min() + 1e-6)
            
            # 特徴量行列と標準化
            X = df_group[["gender_enc", "mood_enc", "year_scaled"]]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # KMeansクラスタリング
            k = min(8, len(df_group))
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            df_group["cluster_id"] = kmeans.fit_predict(X_scaled)
 
            
            return df_group, le_gender, le_mood, scaler, kmeans

        # ===== 8. 赤星に近いクラスタからランダム曲を選択 =====
        def pick_random_nearby_song(clustered_df, custom_song, kmeans_model):
            custom_vec = np.array([custom_song["gender_enc"], custom_song["mood_enc"], custom_song["year_scaled"]])
            centers = kmeans_model.cluster_centers_
            distances = np.linalg.norm(centers - custom_vec, axis=1)
            nearest_cluster_id = np.argmin(distances)
            cluster_songs = clustered_df[clustered_df["cluster_id"] == nearest_cluster_id]
            return cluster_songs.sample(1) if not cluster_songs.empty else None
        

        # ===== 7. 任意の赤星曲を設定 =====
        custom_param = {
            "gender_enc": gender,   # 男性=0, 混合=1, 女性=2
            "mood_enc": mood,     # しっとり=0, リラックス=1, 元気=2, 盛り上がる=3
            "year_scaled": (year - classic_group["year"].min()) / (classic_group["year"].max() - classic_group["year"].min() + 1e-6)
        }

        # ===== 3. 昭和歌謡はランダムに1曲選択 =====
        generation = settings.get("mood")
        if generation == "演歌・昭和歌謡":
            if not showa_group.empty:
                showa_song = showa_group.sample(1)
        

        elif generation == "定番曲・懐メロ":
            classic_clustered, classic_le_gender, classic_le_mood, classic_scaler, classic_kmeans = _cluster(classic_group)
            # 定番・最新グループから曲選択
            selected_song = pick_random_nearby_song(classic_clustered, custom_param, classic_kmeans)
            return selected_song

        elif generation == "最新ヒット":
            latest_clustered, latest_le_gender, latest_le_mood, latest_scaler, latest_kmeans = _cluster(latest_group)
            # 定番・最新グループから曲選択
            selected_song = pick_random_nearby_song(latest_clustered, custom_param, latest_kmeans)
            return selected_song
        
        # 7. 歌う人を選択
        mic_count = settings.get("micCount", 1)
        selected_singers = self._select_singers(members, mic_count)
        
        # 8. 結果を整形
        return {
            "selectedSong": {
                "title": selected_song.iloc["title"],
                "artist": selected_song.iloc["artist"],
                "year": selected_song.iloc["year"]
            },
            "selectedSingers": selected_singers
        }



    def _cluster(df_group, group_name):
            if df_group.empty:
                print(f"{group_name} に曲がありません。")
                return None, None, None, None, None

            # カテゴリ数値化
            le_gender = LabelEncoder()
            le_mood = LabelEncoder()
            df_group["gender_enc"] = le_gender.fit_transform(df_group["gender"])
            df_group["mood_enc"] = le_mood.fit_transform(df_group["mood_tags"])
            
            # 年代を0-1スケーリング
            df_group["year_scaled"] = (df_group["year"] - df_group["year"].min()) / (df_group["year"].max() - df_group["year"].min() + 1e-6)
            
            # 特徴量行列と標準化
            X = df_group[["gender_enc", "mood_enc", "year_scaled"]]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # KMeansクラスタリング
            k = min(8, len(df_group))
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            df_group["cluster_id"] = kmeans.fit_predict(X_scaled)
 
            
            return df_group, le_gender, le_mood, scaler, kmeans


    def _divide_gender(self, members: List[Dict]) -> int:
        """
        メンバーの性別からグループの性別構成を判定して返す。
        返り値は 男のみなら0 / 女のみなら2 / 混合なら1 のいずれか。
        未知・未設定の性別は無視し、結果が空になった場合は 混合として1を返す。
        """
        if not members:
            return 1  # メンバーがいない場合も混合扱い

        normalized = set()

        for member in members:
            gender = member.get("gender")
            if gender in ("male", "female"):
                normalized.add(gender)
            # "others" または None は無視

        if not normalized:
            return 1  # 全員が others か未設定なら混合扱い

        if "male" in normalized and "female" in normalized:
            return 1  # 混合
        elif "male" in normalized:
            return 0  # 男のみ
        elif "female" in normalized:
            return 2  # 女のみ
        else:
            return 1  # 念のため混合



    def _determine_year(self, members: List[Dict], settings: Dict) -> str:
        """
        メンバーの平均年齢から年代を決定
        """
        
        # 平均年齢から
        generation = settings.get("mood")
        if generation == "演歌・昭和歌謡": 
            candidate_year = random.randint(1980, 1989)
            return candidate_year
        
        elif generation == "定番曲・懐メロ": 
            avg_age = sum(member.get("age", 25) for member in members) / len(members)
            candidate_year = 2025 - avg_age + 20 # +20は二十歳想定
            return candidate_year 
        
        elif generation == "最新ヒット":
            candidate_year = random.randint(2023, 2024)
            return candidate_year
        
        return candidate_year



    def _determine_mood(self, settings: Dict) -> str:
        situation = settings.get("situation")

        if situation == "友人と"or"会社の人と":
            l = [2,3]
            candidate_mood = random.choice(l)
            return candidate_mood
        
        elif situation == "恋人と":
            l = [0,1]
            candidate_mood = random.choice(l)
            return candidate_mood
        
        elif situation == "家族と":
            l = [0,1,2,3]
            candidate_mood = random.choice(l)
            return candidate_mood
        
        return candidate_mood

    
    
    def _select_singers(self, members: List[Dict], mic_count: int) -> List[Dict]:
        """
        歌う人をランダムに選択
        元のJavaScriptロジックを移植
        """
        if not members:
            return []
        
        # メンバーをシャッフル
        shuffled_members = members.copy()
        random.shuffle(shuffled_members)
        
        # micCount分だけ選択
        return shuffled_members[:mic_count]