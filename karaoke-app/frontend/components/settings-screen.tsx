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
  const [mood, setMood] = useState("最新ヒット")
  const [situation, setSituation] = useState("友人と")
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
          <p className="text-muted-foreground">カラオケのスタイルを設定しましょう！</p>
        </div>

        <Card className="p-8 space-y-6 bg-card/80 backdrop-blur-sm">
          <div className="space-y-2">
            <Label htmlFor="mood" className="flex items-center gap-2 text-base">
              <Music2 className="w-5 h-5 text-primary" />
              年代・ジャンルは？
            </Label>
            <Select value={mood} onValueChange={setMood}>
              <SelectTrigger id="mood" className="text-lg h-12">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="最新ヒット">⚡️ 最新ヒット</SelectItem>
                <SelectItem value="定番曲・懐メロ">💫 定番曲・懐メロ</SelectItem>
                <SelectItem value="演歌・昭和歌謡">📺 演歌・昭和歌謡</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="situation" className="flex items-center gap-2 text-base">
              <Sparkles className="w-5 h-5 text-secondary" />
              誰と歌う？
            </Label>
            <Select value={situation} onValueChange={setSituation}>
              <SelectTrigger id="situation" className="text-lg h-12">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="友人と">👥 友人と</SelectItem>
                <SelectItem value="恋人と">💑 恋人と</SelectItem>
                <SelectItem value="家族と">👪 家族と</SelectItem>
                <SelectItem value="会社の人と">👨‍💼 会社の人と</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="micCount" className="text-base">
              マイクの数（歌う人数）は？
            </Label>
            <Select value={micCount.toString()} onValueChange={(v) => setMicCount(Number.parseInt(v))}>
              <SelectTrigger id="micCount" className="text-lg h-12">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1">🎤 1本</SelectItem>
                <SelectItem value="2">🎤🎤 2本</SelectItem>
                <SelectItem value="3">🎤🎤🎤 3本</SelectItem>
                <SelectItem value="4">🎤🎤🎤🎤 4本</SelectItem>
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
