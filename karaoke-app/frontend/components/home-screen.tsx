"use client"

import { Button } from "@/components/ui/button"
import { Music, Mic2, Sparkles } from "lucide-react"
import React from "react"

interface HomeScreenProps {
  onStart: () => void
}

export function HomeScreen({ onStart }: HomeScreenProps) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gradient-to-br from-primary/10 via-secondary/10 to-accent/10">
      <div className="max-w-2xl w-full text-center space-y-8">
        {/* 一番上：中央にアニメーションペンギン */}
        <div style={{ position: "relative", height: "78px", width: "100%", margin: "0 auto 18px auto", display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <div className="absolute left-1/2 -translate-x-1/2 animate-penguin-walk-simple" style={{ width: "110px", height: "78px", bottom: 0 }}>
            <svg viewBox="0 0 84 60" width="110" height="78" xmlns="http://www.w3.org/2000/svg">
              {/* 足交互感用 */}
              <ellipse cx="30" cy="55" rx="6" ry="4" fill="#F9B24B"/>
              <ellipse cx="54" cy="55" rx="6" ry="4" fill="#F9B24B"/>
              {/* 体 */}
              <ellipse cx="42" cy="34" rx="22" ry="24" fill="#263147" stroke="#22293e" strokeWidth="2" />
              {/* 白いおなか */}
              <ellipse cx="42" cy="37" rx="16" ry="17.5" fill="#fff" />
              {/* 左ほっぺ */}
              <ellipse cx="32" cy="43" rx="3.5" ry="2" fill="#F7D1C5" opacity="0.45" />
              {/* 右ほっぺ */}
              <ellipse cx="52" cy="43" rx="3.5" ry="2" fill="#F7D1C5" opacity="0.45" />
              {/* 顔丸 */}
              <ellipse cx="42" cy="20" rx="15" ry="13" fill="#263147" />
              {/* 大きな目 */}
              <ellipse cx="36" cy="24" rx="3.2" ry="4" fill="#fff" />
              <ellipse cx="48" cy="24" rx="3.2" ry="4" fill="#fff" />
              <ellipse cx="37" cy="25" rx="1.2" ry="1.9" fill="#222" />
              <ellipse cx="49" cy="25" rx="1.2" ry="1.9" fill="#222" />
              {/* ハイライト */}
              <ellipse cx="35.5" cy="23" rx=".7" ry="1" fill="#fff" opacity=".7" />
              <ellipse cx="48.5" cy="23" rx=".7" ry="1" fill="#fff" opacity=".7" />
              {/* くちばし */}
              <polygon points="42,28 45,31 39,31" fill="#FFA800" />
              {/* 両手短く可愛く */}
              <ellipse cx="22" cy="37" rx="5.7" ry="2.7" fill="#263147" transform="rotate(-20 22 37)" />
              <ellipse cx="62" cy="37" rx="5.7" ry="2.7" fill="#263147" transform="rotate(20 62 37)" />
            </svg>
          </div>
        </div>
        {/* タイトル行：音符・タイトル・マイク 横並び */}
        <div className="flex flex-row items-center justify-center gap-6 mb-4 w-full" style={{maxWidth:'640px'}}>
          <Music className="w-12 h-12 text-primary animate-bounce" />
          <h1 className="text-5xl md:text-6xl font-bold text-balance bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
            First Singin'!
          </h1>
          <Mic2 className="w-12 h-12 text-secondary animate-bounce delay-100" />
        </div>
        <p className="text-xl md:text-2xl text-muted-foreground text-balance mb-2">もう迷わない。AIがみなさんの1曲目を選びます。</p>
        {/* -- ここから下は既存のコンテンツ -- */}
        <div className="bg-card/50 backdrop-blur-sm rounded-2xl p-8 space-y-4 border border-border/50">
          <h2 className="text-lg font-semibold text-card-foreground">このアプリでできること</h2>
          <ul className="space-y-3 text-left text-muted-foreground">
            <li className="flex items-start gap-3">
              <span className="text-primary text-xl">✓</span>
              <span>世代に合わせた“盛り上がる1曲”をAIが提案</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-secondary text-xl">✓</span>
              <span>誰が歌うかをランダムに決定</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-accent text-xl">✓</span>
              <span>雰囲気にぴったりな曲で、空気をさらに盛り上げる</span>
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
