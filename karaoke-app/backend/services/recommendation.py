from typing import List, Dict, Optional, Tuple
import random
from models.song import SongCatalog, Song


class RecommendationService:
    """
    カラオケ選曲のビジネスロジック
    """
    
    def __init__(self, song_catalog: SongCatalog):
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
 
        
        
        # 5. 

        
        # 6. 
        
        selected_song =  # ここに歌の候補のリストが入ればOK
        
        # 7. 歌う人を選択
        mic_count = settings.get("micCount", 1)
        selected_singers = self._select_singers(members, mic_count)
        
        # 8. 結果を整形
        return {
            "selectedSong": {
                "title": selected_song.title,
                "artist": selected_song.artist,
                "year": selected_song.year,
                "genre": selected_song.genre
            },
            "selectedSingers": selected_singers
        }



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