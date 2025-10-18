"use client"

import { Button } from "@/components/ui/button"
import { Music, Mic2, Sparkles } from "lucide-react"

interface HomeScreenProps {
  onStart: () => void
}

export function HomeScreen({ onStart }: HomeScreenProps) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gradient-to-br from-primary/10 via-secondary/10 to-accent/10">
      <div className="max-w-2xl w-full text-center space-y-8">
        <div className="space-y-4">
          <div className="flex justify-center gap-4 mb-6">
            <Music className="w-12 h-12 text-primary animate-bounce" />
            <Mic2 className="w-12 h-12 text-secondary animate-bounce delay-100" />
            <Sparkles className="w-12 h-12 text-accent animate-bounce delay-200" />
          </div>

          <h1 className="text-5xl md:text-6xl font-bold text-balance bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
            カラオケ選曲AI
          </h1>

          <p className="text-xl md:text-2xl text-muted-foreground text-balance">世代を超えた選曲と歌う人を提案</p>
        </div>

        <div className="bg-card/50 backdrop-blur-sm rounded-2xl p-8 space-y-4 border border-border/50">
          <h2 className="text-lg font-semibold text-card-foreground">このアプリでできること</h2>
          <ul className="space-y-3 text-left text-muted-foreground">
            <li className="flex items-start gap-3">
              <span className="text-primary text-xl">✓</span>
              <span>メンバーの年齢に合わせた曲を自動選曲</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-secondary text-xl">✓</span>
              <span>誰が歌うかをランダムに決定</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-accent text-xl">✓</span>
              <span>ムードやシチュエーションに応じた曲提案</span>
            </li>
          </ul>
        </div>

        <Button
          onClick={onStart}
          size="lg"
          className="text-lg px-12 py-6 h-auto bg-gradient-to-r from-primary to-secondary hover:from-primary/90 hover:to-secondary/90 shadow-lg hover:shadow-xl transition-all"
        >
          はじめる
        </Button>
      </div>
    </div>
  )
}
