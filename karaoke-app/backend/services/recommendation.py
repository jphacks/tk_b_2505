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
    
    def __init__(self, song_catalog: pd.DataFrame):
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
        
        # デバッグ用ログ
        print(f"デバッグ情報:")
        print(f"  メンバー: {[m.get('gender') for m in members]}")
        print(f"  性別グループ: {gender} (0=男性, 1=混合, 2=女性)")
        print(f"  年: {year}")
        print(f"  ムード: {mood}")
        print(f"  設定: {settings.get('mood')}")
        
        # データ分布確認
        try:
            print(f"データ分布:")
            print(f"  全曲数: {len(df)}")
            print(f"  昭和歌謡: {len(showa_group)}")
            print(f"  定番曲: {len(classic_group)}")
            print(f"  最新曲: {len(latest_group)}")
            if not showa_group.empty:
                print(f"  昭和歌謡性別分布: {showa_group['gender'].value_counts().to_dict()}")
            if not classic_group.empty:
                print(f"  定番曲性別分布: {classic_group['gender'].value_counts().to_dict()}")
            if not latest_group.empty:
                print(f"  最新曲性別分布: {latest_group['gender'].value_counts().to_dict()}")
        except Exception as e:
            print(f"データ分布確認エラー: {e}")
            import traceback
            traceback.print_exc()
        
        
        # 4. 

        # ===== 1. データ読み込み =====
        df = self.song_catalog

        # ===== 2. 年代グループ分け =====
        showa_group = df[df["year"] < 1990].copy()                   # 昭和歌謡
        classic_group = df[(df["year"] >= 1990) & (df["year"] <= 2022)].copy()  # 定番
        latest_group = df[df["year"] >= 2023].copy()                # 最新曲
        
        # 昭和歌謡にも性別エンコーディングを追加
        if not showa_group.empty:
            le_gender_showa = LabelEncoder()
            showa_group["gender_enc"] = le_gender_showa.fit_transform(showa_group["gender"])
            print(f"  昭和歌謡性別エンコーディング: {dict(zip(le_gender_showa.classes_, le_gender_showa.transform(le_gender_showa.classes_)))}")


        def _cluster(df_group):
            if df_group.empty:
                return None, None, None, None, None

            # カテゴリ数値化
            le_gender = LabelEncoder()
            le_mood = LabelEncoder()
            df_group["gender_enc"] = le_gender.fit_transform(df_group["gender"])
            df_group["mood_enc"] = le_mood.fit_transform(df_group["mood_tags"])
            
            # デバッグ: エンコーディング値を表示
            print(f"    性別エンコーディング: {dict(zip(le_gender.classes_, le_gender.transform(le_gender.classes_)))}")
            print(f"    ムードエンコーディング: {dict(zip(le_mood.classes_, le_mood.transform(le_mood.classes_)))}")
            
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

        # ===== 8. 性別重み付きで曲を選択 =====
        def pick_gender_weighted_song(clustered_df, custom_song, kmeans_model, target_gender):
            """
            性別を重視した曲選択
            target_gender: 0=男性, 1=混合, 2=女性
            """
            custom_vec = np.array([custom_song["gender_enc"], custom_song["mood_enc"], custom_song["year_scaled"]])
            centers = kmeans_model.cluster_centers_
            
            # 各クラスタのスコアを計算（性別重み付き）
            cluster_scores = []
            print(f"    クラスタ分析 (目標性別: {target_gender}):")
            for i, center in enumerate(centers):
                # 基本距離
                base_distance = np.linalg.norm(center - custom_vec)
                
                # 性別マッチングボーナス
                gender_bonus = 0
                cluster_songs = clustered_df[clustered_df["cluster_id"] == i]
                if not cluster_songs.empty:
                    # クラスタ内の性別分布を確認
                    gender_dist = cluster_songs["gender_enc"].value_counts(normalize=True)
                    gender_counts = cluster_songs["gender_enc"].value_counts()
                    
                    if target_gender == 0:  # 男性希望
                        gender_bonus = gender_dist.get(0, 0) * 2.0  # 男性曲が多いほど高スコア
                    elif target_gender == 2:  # 女性希望
                        gender_bonus = gender_dist.get(2, 0) * 2.0  # 女性曲が多いほど高スコア
                    else:  # 混合
                        gender_bonus = gender_dist.get(1, 0) * 1.5  # 混合曲が多いほど高スコア
                    
                    print(f"      クラスタ{i}: 性別分布={gender_counts.to_dict()}, ボーナス={gender_bonus:.2f}")
                
                # スコア = 距離の逆数 + 性別ボーナス
                score = 1.0 / (base_distance + 0.1) + gender_bonus
                cluster_scores.append(score)
            
            # 最高スコアのクラスタを選択
            best_cluster_id = np.argmax(cluster_scores)
            cluster_songs = clustered_df[clustered_df["cluster_id"] == best_cluster_id]
            
            # さらに性別でフィルタリング
            if target_gender in [0, 2]:  # 男性または女性を希望
                gender_filtered = cluster_songs[cluster_songs["gender_enc"] == target_gender]
                if not gender_filtered.empty:
                    cluster_songs = gender_filtered
            
            return cluster_songs.sample(1) if not cluster_songs.empty else None
        

        # ===== 7. 任意の赤星曲を設定 =====
        # 年スケーリングを各グループに応じて動的に計算
        def get_year_scaled(target_year, df_group):
            if df_group.empty:
                return 0.5  # デフォルト値
            year_min = df_group["year"].min()
            year_max = df_group["year"].max()
            return (target_year - year_min) / (year_max - year_min + 1e-6)
        
        custom_param = {
            "gender_enc": gender,   # 男性=0, 混合=1, 女性=2
            "mood_enc": mood,     # しっとり=0, リラックス=1, 元気=2, 盛り上がる=3
            "year_scaled": get_year_scaled(year, classic_group)  # 動的に計算
        }

        # ===== 3. 昭和歌謡はランダムに1曲選択 =====
        generation = settings.get("mood")
        selected_song = None
        
        if generation == "演歌・昭和歌謡":
            if not showa_group.empty:
                # 昭和歌謡でも性別フィルタリング
                if gender in [0, 2]:  # 男性または女性を希望
                    gender_filtered = showa_group[showa_group["gender_enc"] == gender]
                    if not gender_filtered.empty:
                        selected_song = gender_filtered.sample(1)
                    else:
                        selected_song = showa_group.sample(1)
                else:
                    selected_song = showa_group.sample(1)
            else:
                # フォールバック: 全曲からランダム選択
                selected_song = df.sample(1)

        elif generation == "定番曲・懐メロ":
            # 定番グループ用の年スケーリング
            custom_param["year_scaled"] = get_year_scaled(year, classic_group)
            classic_clustered, classic_le_gender, classic_le_mood, classic_scaler, classic_kmeans = _cluster(classic_group)
            if classic_clustered is not None:
                selected_song = pick_gender_weighted_song(classic_clustered, custom_param, classic_kmeans, gender)
            if selected_song is None:
                selected_song = df.sample(1)

        elif generation == "最新ヒット":
            # 最新グループ用の年スケーリング
            custom_param["year_scaled"] = get_year_scaled(year, latest_group)
            latest_clustered, latest_le_gender, latest_le_mood, latest_scaler, latest_kmeans = _cluster(latest_group)
            if latest_clustered is not None:
                selected_song = pick_gender_weighted_song(latest_clustered, custom_param, latest_kmeans, gender)
            if selected_song is None:
                selected_song = df.sample(1)
        else:
            # デフォルト: 全曲からランダム選択
            selected_song = df.sample(1)
        
        # 7. 歌う人を選択
        mic_count = settings.get("micCount", 1)
        selected_singers = self._select_singers(members, mic_count)
        
        # 8. 結果を整形
        if selected_song is not None and not selected_song.empty:
            # デバッグ: 選ばれた曲の性別を確認
            selected_gender = selected_song.iloc[0]["gender"]
            print(f"  選ばれた曲の性別: {selected_gender}")
            
            return {
                "selectedSong": {
                    "title": selected_song.iloc[0]["title"],
                    "artist": selected_song.iloc[0]["artist"],
                    "year": int(selected_song.iloc[0]["year"]),
                    "genre": selected_song.iloc[0]["genre"]
                },
                "selectedSingers": selected_singers
            }
        else:
            # エラー時のフォールバック
            return {
                "selectedSong": {
                    "title": "エラーが発生しました",
                    "artist": "システム",
                    "year": 2024,
                    "genre": "エラー"
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



    def _determine_year(self, members: List[Dict], settings: Dict) -> int:
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
        
        # デフォルト値
        return 2020



    def _determine_mood(self, settings: Dict) -> int:
        situation = settings.get("situation")

        if situation == "友人と" or situation == "会社の人と":
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
        
        # デフォルト値
        return random.choice([0,1,2,3])

    
    
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