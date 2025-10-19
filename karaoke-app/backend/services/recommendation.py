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
            settings: 設定 {"mood": "upbeat", "situation": "party", "micCount": 2}
            
        Returns:
            推薦結果 {"selectedSong": {...}, "selectedSingers": [...]}
        """
        # 1. 平均年齢から年代を決定
        decade = self._determine_decade(members)
        
        # 2. 年代に応じた曲を取得
        songs = self.song_catalog.filter(decade=decade)
        
        # 3. ムードに応じてフィルタリング
        mood = settings.get("mood")
        if mood:
            songs = [s for s in songs if mood in s.mood_tags]
        
        # 4. シチュエーションに応じてフィルタリング
        situation = settings.get("situation")
        if situation:
            songs = [s for s in songs if situation in s.situation_tags]
        
        # 5. 曲が見つからない場合は年代のみで再検索
        if not songs:
            songs = self.song_catalog.filter(decade=decade)
        
        # 6. ランダム選曲
        if not songs:
            # 最後の手段：全曲からランダム選択
            songs = list(self.song_catalog.all())
        
        selected_song = random.choice(songs)
        
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
    
    def _determine_decade(self, members: List[Dict]) -> str:
        """
        メンバーの平均年齢から年代を決定
        元のJavaScriptロジックを移植
        """
        if not members:
            return "2010s"
        
        avg_age = sum(member.get("age", 25) for member in members) / len(members)
        
        if avg_age >= 45:
            return "1990s"
        elif avg_age >= 35:
            return "2000s"
        elif avg_age >= 25:
            return "2010s"
        else:
            return "2020s"
    
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