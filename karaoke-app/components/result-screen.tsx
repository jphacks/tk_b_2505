"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Music, Mic, RotateCcw, Sparkles } from "lucide-react"
import type { Member, Settings } from "@/app/page"

interface ResultScreenProps {
  members: Member[]
  settings: Settings
  onReset: () => void
}

interface Song {
  title: string
  artist: string
  year: number
  genre: string
}

export function ResultScreen({ members, settings, onReset }: ResultScreenProps) {
  const [selectedSong, setSelectedSong] = useState<Song | null>(null)
  const [selectedSingers, setSelectedSingers] = useState<Member[]>([])
  const [isRevealing, setIsRevealing] = useState(true)

  useEffect(() => {
    // 年代別の曲データベース（モックデータ）
    const songDatabase: Record<string, Song[]> = {
      "1990s": [
        { title: "LOVEマシーン", artist: "モーニング娘。", year: 1999, genre: "J-Pop" },
        { title: "TSUNAMI", artist: "サザンオールスターズ", year: 2000, genre: "J-Pop" },
        { title: "CAN YOU CELEBRATE?", artist: "安室奈美恵", year: 1997, genre: "J-Pop" },
      ],
      "2000s": [
        { title: "世界に一つだけの花", artist: "SMAP", year: 2003, genre: "J-Pop" },
        { title: "Flavor Of Life", artist: "宇多田ヒカル", year: 2007, genre: "J-Pop" },
        { title: "千の風になって", artist: "秋川雅史", year: 2006, genre: "Ballad" },
      ],
      "2010s": [
        { title: "恋", artist: "星野源", year: 2016, genre: "J-Pop" },
        { title: "Pretender", artist: "Official髭男dism", year: 2019, genre: "J-Pop" },
        { title: "Lemon", artist: "米津玄師", year: 2018, genre: "J-Pop" },
      ],
      "2020s": [
        { title: "ドライフラワー", artist: "優里", year: 2020, genre: "J-Pop" },
        { title: "KICK BACK", artist: "米津玄師", year: 2022, genre: "Rock" },
        { title: "アイドル", artist: "YOASOBI", year: 2023, genre: "J-Pop" },
      ],
    }

    // メンバーの平均年齢から年代を決定
    const avgAge = members.reduce((sum, m) => sum + m.age, 0) / members.length
    let decade = "2010s"

    if (avgAge >= 45) decade = "1990s"
    else if (avgAge >= 35) decade = "2000s"
    else if (avgAge >= 25) decade = "2010s"
    else decade = "2020s"

    // ムードに応じて曲を選択
    const songs = songDatabase[decade]
    const randomSong = songs[Math.floor(Math.random() * songs.length)]

    // 歌う人をランダムに選択
    const shuffled = [...members].sort(() => Math.random() - 0.5)
    const singers = shuffled.slice(0, settings.micCount)

    setTimeout(() => {
      setSelectedSong(randomSong)
      setSelectedSingers(singers)
      setIsRevealing(false)
    }, 2000)
  }, [members, settings])

  if (isRevealing) {
    return (
      <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-primary/10 via-secondary/10 to-accent/10">
        <div className="text-center space-y-6">
          <Sparkles className="w-16 h-16 text-primary mx-auto animate-spin" />
          <h2 className="text-2xl md:text-3xl font-bold text-foreground">最適な曲を選んでいます...</h2>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen p-6 bg-gradient-to-br from-primary/5 via-secondary/5 to-accent/5">
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="text-center space-y-2">
          <div className="flex justify-center">
            <Music className="w-12 h-12 text-accent animate-bounce" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-foreground">選曲結果</h1>
          <p className="text-muted-foreground">この曲で盛り上がりましょう！</p>
        </div>

        {selectedSong && (
          <Card className="p-8 space-y-6 bg-gradient-to-br from-primary/10 to-secondary/10 border-2 border-primary/20">
            <div className="text-center space-y-4">
              <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-primary to-secondary">
                <Music className="w-10 h-10 text-primary-foreground" />
              </div>

              <div className="space-y-2">
                <h2 className="text-3xl md:text-4xl font-bold text-foreground text-balance">{selectedSong.title}</h2>
                <p className="text-xl text-muted-foreground">{selectedSong.artist}</p>
                <div className="flex items-center justify-center gap-4 text-sm text-muted-foreground">
                  <span className="px-3 py-1 bg-muted rounded-full">{selectedSong.year}年</span>
                  <span className="px-3 py-1 bg-muted rounded-full">{selectedSong.genre}</span>
                </div>
              </div>
            </div>
          </Card>
        )}

        <Card className="p-8 space-y-4 bg-card/80 backdrop-blur-sm">
          <div className="flex items-center gap-2 text-lg font-semibold text-card-foreground">
            <Mic className="w-6 h-6 text-secondary" />
            歌う人
          </div>

          <div className="grid gap-4">
            {selectedSingers.map((singer, index) => (
              <div
                key={singer.id}
                className="flex items-center gap-4 p-4 bg-gradient-to-r from-secondary/10 to-accent/10 rounded-lg border border-secondary/20"
              >
                <div className="flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-br from-secondary to-accent text-secondary-foreground font-bold text-lg">
                  {index + 1}
                </div>
                <div className="flex-1">
                  <p className="font-semibold text-lg text-foreground">{singer.nickname}</p>
                  <p className="text-sm text-muted-foreground">
                    {singer.age}歳 ·{" "}
                    {singer.gender === "male" ? "男性" : singer.gender === "female" ? "女性" : "その他"}
                  </p>
                </div>
                <Mic className="w-6 h-6 text-secondary" />
              </div>
            ))}
          </div>
        </Card>

        <div className="flex gap-4">
          <Button onClick={onReset} variant="outline" size="lg" className="flex-1 bg-transparent">
            <RotateCcw className="w-5 h-5 mr-2" />
            最初から
          </Button>
          <Button
            onClick={() => window.location.reload()}
            size="lg"
            className="flex-1 bg-gradient-to-r from-primary to-secondary hover:from-primary/90 hover:to-secondary/90"
          >
            もう一度提案
          </Button>
        </div>
      </div>
    </div>
  )
}
