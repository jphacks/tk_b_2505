from typing import List, Dict, Optional, Tuple
from collections import Counter
import statistics
import math
import csv


class RecommendationService:
    """
    カラオケ選曲のビジネスロジック
    """
    # 年代
    def __init__(self):
        # 年齢から年代へのマッピング閾値
        self.age_to_era_mapping = {
            (0, 5): 2020,
            (6, 15): 2010,
            (16, 25): 2000,
            (26, 35): 1990,
            (36, 45): 1980,
            (46, 55): 1970,
            (56, 65): 1960,
            (66, 75): 1950,
            (76, 85): 1940,
            (86, 95): 1930,
            (96, 100): 1920,
        }
    
    def calculate_era_from_age(self, age: int) -> int:
        """
        年齢から年代に変換
        
        Args:
            age: 参加者の年齢入力値
            
        Returns:
            era: 年代(10年刻み)
        """
        for (min_age, max_age), era in self.age_to_era_mapping.items():
            if min_age <= age <= max_age:
                return era
        return 2020  # default
    
    # 性別
    def calculate_gender_distribution(self, participants: List[Dict]) -> Dict[str, float]:
        """
        参加者の性別の割合
        
        Args:
            participants: 参加者リスト
            
        Returns:
            性別分布 {"male": 0.6, "female": 0.4, "other": 0.0}
        """
        if not participants:
            return {"male": 0.5, "female": 0.5, "other": 0.0}
        
        gender_counts = Counter(p.get("gender", "other") for p in participants)
        total = len(participants)
        
        return {
            "male": gender_counts.get("male", 0) / total,
            "female": gender_counts.get("female", 0) / total,
            "other": gender_counts.get("other", 0) / total,
        }
    
    # 曲とのマッチ度アルゴリズム
    # 平均年齢
    def calculate_average_era(self, participants: List[Dict]) -> int:
        """
        参加者の平均年代を算出
        
        Args:
            participants: 参加者リスト
            
        Returns:
            平均年代
        """
        if not participants:
            return 2020 # default
        
        eras = [self.calculate_era_from_age(p["age"]) for p in participants]
        avg_era = statistics.mean(eras) # 平均値の算出
        
        # 平均値から10刻み年代に変換
        rounded_era = math.floor(avg_era / 10) * 10
        return int(rounded_era)

    # 曲のスコア算出
    def load_songs_from_csv(csv_path: str = 'data/songs_data.csv') -> List[Dict]:
        """CSVファイルから曲データを読み込む"""
        songs = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                songs.append({
                    'title': row['title'],
                    'year': int(row['year']),
                    'mood_tags': row['mood_tags'],
                    'situation_tags': row['situation_tags']
                })
        return songs

    def select_song(
        self,
        song: Dict,
        target_era: int,
        gender_distribution: Dict[str, float],
        mood: Optional[str] = None,
        situation: Optional[str] = None,
        ) -> float:
        """
        曲のマッチングスコアを計算
        
        Args:
            song: 曲データ {"title": "...", "year": 1999, "mood_tags": "懐かしい", ...}
            target_era: 目標年代
            gender_distribution: 性別分布
            mood: 雰囲気（オプション）
            situation: シチュエーション（オプション）
            
        Returns:
            スコア（0-100）
        """
            

        scored_songs=[]
        for i in range(song): 
            # スコア順にソート
            

            score = 0.0
            
            # 1. 年代マッチング（最大40点）
            # CSVのyearカラムを使用
            song_year = song[i].get("year", 2020)
            era_diff = abs(song_year - target_era)
            if era_diff == 0:
                score += 40
            elif era_diff <= 10:
                score += 30
            elif era_diff <= 20:
                score += 20
            elif era_diff <= 30:
                score += 10
            
            # 2. 性別マッチング（最大30点）
            # 性別情報がCSVにないため、性別分布に基づいて汎用的なスコアを付与
            # 男女比が偏っている場合は、その性別に合う曲を優先
            male_ratio = gender_distribution[i].get("male", 0.5)
            female_ratio = gender_distribution[i].get("female", 0.5)
            
            # バランスが取れている場合は満点、偏っている場合は調整
            balance_score = 30 * (1 - abs(male_ratio - female_ratio))
            score += balance_score
            
            # 3. 雰囲気マッチング（最大15点）
            if mood:
                song_mood_tags = song[i].get("mood_tags", "").lower()
                mood_lower = mood.lower()
                
                # 完全一致
                if mood_lower == song_mood_tags:
                    score += 15
                # 部分一致（カンマ区切りの複数タグに対応）
                elif mood_lower in song_mood_tags or any(
                    mood_lower in tag.strip() for tag in song_mood_tags.split(",")
                ):
                    score += 12
            else:
                score += 7.5  # 雰囲気指定なしの場合は中間点
            
            # 4. シチュエーションマッチング（最大15点）
            if situation:
                song_situation_tags = song[i].get("situation_tags", "").lower()
                situation_lower = situation.lower()
                
                # 完全一致
                if situation_lower == song_situation_tags:
                    score += 15
                # 部分一致（カンマ区切りの複数タグに対応）
                elif situation_lower in song_situation_tags or any(
                    situation_lower in tag.strip() for tag in song_situation_tags.split(",")
                ):
                    score += 12
            else:
                score += 7.5  # シチュエーション指定なしの場合は中間点
            
            score = round(score, 2)

            scored_songs.append({
                **song,
                'score': score
            })
        
        scored_songs.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_songs[:1]
  
    

    # 歌う人の選択
    def select_singer(
        self,
        song: Dict,
        participants: List[Dict],
        sung_counts: Optional[Dict[str, int]] = None,
    ) -> Tuple[Dict, str]:
        """
        曲に最適な歌い手を選択
        
        Args:
            song: 曲データ
            participants: 参加者リスト
            sung_counts: 各参加者の歌唱回数 {"太郎": 2, "花子": 1, ...}
            
        Returns:
            選ばれた参加者
        """
        if not participants:
            return None, "参加者がいません"
        
        sung_counts = sung_counts or {}
        song_gender = song.get("gender", "unisex").lower()
        song_era = song.get("era", 2020)
        
        # 各参加者のスコアを計算
        participant_scores = []
        for participant in participants:
            score = 0.0
            
            # 1. 性別マッチング（40点）
            p_gender = participant.get("gender", "other").lower()
            if song_gender == "unisex":
                score += 30
            elif song_gender == p_gender:
                score += 40
            elif song_gender != p_gender:
                score += 10  # 性別が違っても歌える
            
            # 2. 年代マッチング（30点）
            p_era = self.calculate_era_from_age(participant.get("age", 25))
            era_diff = abs(song_era - p_era)
            if era_diff == 0:
                score += 30
            elif era_diff <= 10:
                score += 20
            elif era_diff <= 20:
                score += 10
            
            # 3. 歌唱回数の均等化（30点）
            p_name = participant.get("name", "")
            sung_count = sung_counts.get(p_name, 0)
            max_sung = max(sung_counts.values()) if sung_counts else 0
            
            # 歌った回数が少ない人を優先
            if max_sung == 0:
                score += 30
            else:
                fairness_score = 30 * (1 - (sung_count / (max_sung + 1)))
                score += fairness_score
            
            participant_scores.append({
                "participant": participant,
                "score": score,
                "sung_count": sung_count,
            })
        
        # スコアでソート
        participant_scores.sort(key=lambda x: x["score"], reverse=True)
        best_match = participant_scores[0]
        
        
        return best_match["participant"]
    
    def create_setlist(
        self,
        songs: List[Dict],
        participants: List[Dict],
        mood: Optional[str] = None,
        situation: Optional[str] = None,
        num_songs: int = 10,
    ) -> List[Dict]:
        """
        セットリストを作成（曲と歌い手のペア）
        
        Args:
            songs: 全曲リスト
            participants: 参加者リスト
            mood: 雰囲気
            situation: シチュエーション
            num_songs: セットリストの曲数
            
        Returns:
            セットリスト [{"song": {...}, "singer": {...}, "reason": "..."}, ...]
        """
        # 推薦曲を取得
        recommended_songs = self.recommend_songs(
            songs, participants, mood, situation, top_n=num_songs
        )
        
        # 各曲に歌い手を割り当て
        setlist = []
        sung_counts = {p.get("name", ""): 0 for p in participants}
        
        for song in recommended_songs:
            singer, reason = self.select_singer(song, participants, sung_counts)
            
            if singer:
                singer_name = singer.get("name", "")
                sung_counts[singer_name] = sung_counts.get(singer_name, 0) + 1
                
                setlist.append({
                    "song": song,
                    "singer": singer,
                    "reason": reason,
                    "order": len(setlist) + 1,
                })
        
        return setlist
