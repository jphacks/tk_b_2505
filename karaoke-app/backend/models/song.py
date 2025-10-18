from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Set, Tuple, Dict, Optional
from pathlib import Path
import csv
import unicodedata
import re
import itertools


# ========= 例外 =========

class SongValidationError(Exception):
    """1件のレコードに対する検証エラー。"""
    def __init__(self, message: str, row_index: Optional[int] = None, row: Optional[Dict] = None):
        self.row_index = row_index
        self.row = row
        super().__init__(message)


class BulkLoadError(Exception):
    """CSV一括読み込み時の複数エラー集約。"""
    def __init__(self, errors: List[SongValidationError]):
        self.errors = errors
        msgs = "\n".join(
            f"[row {e.row_index}] {e}" if e.row_index is not None else str(e) for e in errors
        )
        super().__init__(f"{len(errors)} error(s) while loading CSV:\n{msgs}")


# ========= 正規化ユーティリティ =========

_TAG_SPLIT_RE = re.compile(r"[,\u3001;\s/｜|]+")

def normalize_text(s: str) -> str:
    """日本語を含む文字列をNFKC正規化＋前後空白除去。"""
    return unicodedata.normalize("NFKC", s).strip()

def normalize_tag(tag: str) -> str:
    """タグを検索しやすいように小文字化＋正規化。"""
    return normalize_text(tag).lower()

def parse_tags(raw: str) -> Set[str]:
    """
    タグ文字列を集合へ変換。
    区切りは , / ; スペース | 全角読点 などを許容。
    """
    if raw is None:
        return set()
    raw = normalize_text(raw)
    tokens = [t for t in _TAG_SPLIT_RE.split(raw) if t]
    return {normalize_tag(t) for t in tokens}


def decade_from_year(year: int) -> str:
    """例: 1999 -> '1990s'"""
    d = (year // 10) * 10
    return f"{d}s"


# ========= モデル =========

@dataclass(frozen=True)
class Song:
    title: str
    artist: str
    year: int
    genre: str
    mood_tags: frozenset[str] = field(default_factory=frozenset)
    situation_tags: frozenset[str] = field(default_factory=frozenset)

    # 派生プロパティ
    @property
    def decade(self) -> str:
        return decade_from_year(self.year)

    # --- 検証・正規化 ---
    def __post_init__(self):
        # 基本フィールドの正規化
        object.__setattr__(self, "title", normalize_text(self.title))
        object.__setattr__(self, "artist", normalize_text(self.artist))
        object.__setattr__(self, "genre", normalize_text(self.genre))

        # 年の検証（必要に応じて境界は調整）
        if not (1900 <= int(self.year) <= 2100):
            raise SongValidationError(f"invalid year: {self.year}")

        # 必須文字列
        if not self.title:
            raise SongValidationError("title is required")
        if not self.artist:
            raise SongValidationError("artist is required")

        # タグは正規化済みの小文字集合へ
        mt = frozenset(normalize_tag(t) for t in self.mood_tags if t)
        st = frozenset(normalize_tag(t) for t in self.situation_tags if t)
        object.__setattr__(self, "mood_tags", mt)
        object.__setattr__(self, "situation_tags", st)

    # --- CSV → モデル ---
    @staticmethod
    def from_row(row: Dict[str, str]) -> "Song":
        """
        CSV 1行を Song へ変換。
        期待ヘッダ: title, artist, year, genre, mood_tags, situation_tags
        """
        try:
            title = row.get("title", "")
            artist = row.get("artist", "")
            year_str = row.get("year", "")
            genre = row.get("genre", "")
            mood_raw = row.get("mood_tags", "") or ""
            situation_raw = row.get("situation_tags", "") or ""

            year = int(str(year_str).strip())
            mood = parse_tags(mood_raw)
            situation = parse_tags(situation_raw)

            return Song(
                title=title,
                artist=artist,
                year=year,
                genre=genre,
                mood_tags=frozenset(mood),
                situation_tags=frozenset(situation),
            )
        except ValueError as ve:
            raise SongValidationError(f"year must be integer: {row.get('year')}") from ve


# ========= カタログ（検索・読み込み） =========

class SongCatalog:
    """
    不変の曲カタログ。
    ・CSVロード
    ・年代/ムード/シチュエーションでのフィルタ
    将来的にDBへ差し替えるときもインターフェースを維持しやすい。
    """
    def __init__(self, songs: Iterable[Song]):
        self._songs: Tuple[Song, ...] = tuple(songs)

    @classmethod
    def from_csv(cls, path: Path | str, encoding: str = "utf-8-sig") -> "SongCatalog":
        """
        CSV を読み込み、検証エラーがあれば BulkLoadError に集約。
        """
        path = Path(path)
        errors: List[SongValidationError] = []
        songs: List[Song] = []

        with path.open("r", encoding=encoding, newline="") as f:
            reader = csv.DictReader(f)
            expected = {"title", "artist", "year", "genre", "mood_tags", "situation_tags"}
            missing = expected - set(reader.fieldnames or [])
            if missing:
                raise BulkLoadError([
                    SongValidationError(f"missing columns: {', '.join(sorted(missing))}")
                ])

            for idx, row in enumerate(reader, start=2):  # 1行目はヘッダ、2行目をrow index=2とする
                try:
                    songs.append(Song.from_row(row))
                except SongValidationError as e:
                    e.row_index = idx
                    e.row = row
                    errors.append(e)

        if errors:
            # 1つでもエラーがあればまとめて例外
            raise BulkLoadError(errors)
        return cls(songs)

    # ---- クエリAPI ----
    def all(self) -> Tuple[Song, ...]:
        return self._songs

    def filter(
        self,
        decade: Optional[str] = None,
        mood: Optional[str] = None,
        situation: Optional[str] = None,
    ) -> List[Song]:
        """
        条件に合致する曲を返す。
        ・decade: '1990s' のような文字列。Noneなら無条件
        ・mood/situation: タグ部分一致（小文字化して比較）
        """
        mood = normalize_tag(mood) if mood else None
        situation = normalize_tag(situation) if situation else None

        result: Iterable[Song] = self._songs

        if decade:
            d = normalize_text(decade)
            result = (s for s in result if s.decade == d)

        if mood:
            result = (s for s in result if mood in s.mood_tags)

        if situation:
            result = (s for s in result if situation in s.situation_tags)

        return list(result)

    def decades(self) -> List[str]:
        """存在する年代の一覧（昇順）。"""
        return sorted({s.decade for s in self._songs})


# ========= 簡易の手動テスト =========
if __name__ == "__main__":
    # 例: backend/data/songs.csv を読み込む
    catalog = SongCatalog.from_csv(Path(__file__).parents[1] / "data" / "songs.csv")
    print(f"loaded: {len(catalog.all())} songs, decades={catalog.decades()}")

    # 1990s かつ mood=party を確認
    sample = catalog.filter(decade="1990s", mood="party")
    for s in itertools.islice(sample, 5):
        print(s.decade, s.title, s.artist, s.mood_tags, s.situation_tags)

