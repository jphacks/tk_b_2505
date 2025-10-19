"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { X, Plus, Users } from "lucide-react"
import type { Member } from "@/app/page"

interface MemberInputScreenProps {
  onComplete: (members: Member[]) => void
}

export function MemberInputScreen({ onComplete }: MemberInputScreenProps) {
  const [members, setMembers] = useState<Member[]>([])
  const [nickname, setNickname] = useState("")
  const [gender, setGender] = useState<"male" | "female" | "other">("male")
  const [age, setAge] = useState("")

  const addMember = () => {
    if (!nickname || !age) return

    const newMember: Member = {
      id: Math.random().toString(36).substr(2, 9),
      nickname,
      gender,
      age: Number.parseInt(age),
    }

    setMembers([...members, newMember])
    setNickname("")
    setAge("")
  }

  const removeMember = (id: string) => {
    setMembers(members.filter((m) => m.id !== id))
  }

  const handleComplete = () => {
    if (members.length > 0) {
      onComplete(members)
    }
  }

  return (
    <div className="min-h-screen p-6 bg-gradient-to-br from-primary/5 via-secondary/5 to-accent/5">
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="text-center space-y-2">
          <div className="flex justify-center">
            <Users className="w-12 h-12 text-primary" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-foreground">メンバー情報入力</h1>
          <p className="text-muted-foreground">参加メンバーの情報を入力してください</p>
        </div>

        <Card className="p-6 space-y-6 bg-card/80 backdrop-blur-sm">
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="nickname">ニックネーム</Label>
              <Input
                id="nickname"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
                placeholder="例: たろう"
                className="text-lg"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="gender">性別</Label>
                <Select value={gender} onValueChange={(v) => setGender(v as any)}>
                  <SelectTrigger id="gender" className="text-lg">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="male">男性</SelectItem>
                    <SelectItem value="female">女性</SelectItem>
                    <SelectItem value="other">その他</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="age">年齢</Label>
                <Input
                  id="age"
                  type="number"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  placeholder="例: 25"
                  className="text-lg"
                  min="1"
                  max="100"
                />
              </div>
            </div>

            <Button onClick={addMember} className="w-full bg-transparent" size="lg" variant="outline">
              <Plus className="w-5 h-5 mr-2" />
              メンバーを追加
            </Button>
          </div>
        </Card>

        {members.length > 0 && (
          <Card className="p-6 space-y-4 bg-card/80 backdrop-blur-sm">
            <h2 className="font-semibold text-lg text-card-foreground">登録済みメンバー ({members.length}人)</h2>
            <div className="space-y-2">
              {members.map((member) => (
                <div key={member.id} className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-primary-foreground font-bold">
                      {member.nickname.charAt(0)}
                    </div>
                    <div>
                      <p className="font-medium text-foreground">{member.nickname}</p>
                      <p className="text-sm text-muted-foreground">
                        {member.gender === "male" ? "男性" : member.gender === "female" ? "女性" : "その他"} ·{" "}
                        {member.age}歳
                      </p>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => removeMember(member.id)}
                    className="text-destructive hover:text-destructive"
                  >
                    <X className="w-5 h-5" />
                  </Button>
                </div>
              ))}
            </div>
          </Card>
        )}

        <Button
          onClick={handleComplete}
          disabled={members.length === 0}
          className="w-full bg-gradient-to-r from-primary to-secondary hover:from-primary/90 hover:to-secondary/90"
          size="lg"
        >
          次へ進む
        </Button>
      </div>
    </div>
  )
}
