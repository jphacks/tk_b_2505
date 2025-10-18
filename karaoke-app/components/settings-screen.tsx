"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Card } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Settings2, Music2, Sparkles } from "lucide-react"
import type { Settings } from "@/app/page"

interface SettingsScreenProps {
  onComplete: (settings: Settings) => void
}

export function SettingsScreen({ onComplete }: SettingsScreenProps) {
  const [mood, setMood] = useState("盛り上がる")
  const [situation, setSituation] = useState("飲み会")
  const [micCount, setMicCount] = useState(1)

  const handleComplete = () => {
    onComplete({ mood, situation, micCount })
  }

  return (
    <div className="min-h-screen p-6 bg-gradient-to-br from-primary/5 via-secondary/5 to-accent/5">
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="text-center space-y-2">
          <div className="flex justify-center">
            <Settings2 className="w-12 h-12 text-secondary" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-foreground">選曲設定</h1>
          <p className="text-muted-foreground">カラオケのムードを設定してください</p>
        </div>

        <Card className="p-8 space-y-6 bg-card/80 backdrop-blur-sm">
          <div className="space-y-2">
            <Label htmlFor="mood" className="flex items-center gap-2 text-base">
              <Music2 className="w-5 h-5 text-primary" />
              ムード
            </Label>
            <Select value={mood} onValueChange={setMood}>
              <SelectTrigger id="mood" className="text-lg h-12">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="盛り上がる">🎉 盛り上がる</SelectItem>
                <SelectItem value="しっとり">🌙 しっとり</SelectItem>
                <SelectItem value="懐かしい">💫 懐かしい</SelectItem>
                <SelectItem value="元気">⚡ 元気</SelectItem>
                <SelectItem value="リラックス">🌸 リラックス</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="situation" className="flex items-center gap-2 text-base">
              <Sparkles className="w-5 h-5 text-secondary" />
              シチュエーション
            </Label>
            <Select value={situation} onValueChange={setSituation}>
              <SelectTrigger id="situation" className="text-lg h-12">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="飲み会">🍻 飲み会</SelectItem>
                <SelectItem value="二次会">🎊 二次会</SelectItem>
                <SelectItem value="歓迎会">👋 歓迎会</SelectItem>
                <SelectItem value="送別会">👋 送別会</SelectItem>
                <SelectItem value="忘年会">🎄 忘年会</SelectItem>
                <SelectItem value="新年会">🎍 新年会</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="micCount" className="text-base">
              マイクの数（歌う人数）
            </Label>
            <Select value={micCount.toString()} onValueChange={(v) => setMicCount(Number.parseInt(v))}>
              <SelectTrigger id="micCount" className="text-lg h-12">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1">🎤 1本（ソロ）</SelectItem>
                <SelectItem value="2">🎤🎤 2本（デュエット）</SelectItem>
                <SelectItem value="3">🎤🎤🎤 3本（トリオ）</SelectItem>
                <SelectItem value="4">🎤🎤🎤🎤 4本（カルテット）</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </Card>

        <Button
          onClick={handleComplete}
          className="w-full bg-gradient-to-r from-secondary to-accent hover:from-secondary/90 hover:to-accent/90"
          size="lg"
        >
          曲を提案してもらう
        </Button>
      </div>
    </div>
  )
}
