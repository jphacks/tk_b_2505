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

  const fetchRecommendation = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/recommend-songs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          members: members,
          settings: settings
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      // バックエンドからのレスポンスを処理
      setSelectedSong(data.selectedSong)
      setSelectedSingers(data.selectedSingers)
      setIsRevealing(false)
    } catch (error) {
      console.error('推薦取得エラー:', error)
      // エラー時はフォールバック処理
      setIsRevealing(false)
      // エラーメッセージを表示するか、デフォルトの曲を設定
    }
  }

  useEffect(() => {
    // 2秒のローディング時間を維持
    setTimeout(() => {
      fetchRecommendation()
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
            onClick={() => {
              setIsRevealing(true)
              setSelectedSong(null)
              setSelectedSingers([])
              // 2秒のローディング時間を維持
              setTimeout(() => {
                fetchRecommendation()
              }, 2000)
            }}
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
