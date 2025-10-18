"use client"

import { useState } from "react"
import { HomeScreen } from "@/components/home-screen"
import { MemberInputScreen } from "@/components/member-input-screen"
import { SettingsScreen } from "@/components/settings-screen"
import { ResultScreen } from "@/components/result-screen"

export type Member = {
  id: string
  nickname: string
  gender: "male" | "female" | "other"
  age: number
}

export type Settings = {
  mood: string
  situation: string
  micCount: number
}

export default function Page() {
  const [step, setStep] = useState<"home" | "members" | "settings" | "result">("home")
  const [members, setMembers] = useState<Member[]>([])
  const [settings, setSettings] = useState<Settings | null>(null)

  const handleStart = () => {
    setStep("members")
  }

  const handleMembersComplete = (memberList: Member[]) => {
    setMembers(memberList)
    setStep("settings")
  }

  const handleSettingsComplete = (settingsData: Settings) => {
    setSettings(settingsData)
    setStep("result")
  }

  const handleReset = () => {
    setStep("home")
    setMembers([])
    setSettings(null)
  }

  return (
    <main className="min-h-screen">
      {step === "home" && <HomeScreen onStart={handleStart} />}
      {step === "members" && <MemberInputScreen onComplete={handleMembersComplete} />}
      {step === "settings" && <SettingsScreen onComplete={handleSettingsComplete} />}
      {step === "result" && settings && <ResultScreen members={members} settings={settings} onReset={handleReset} />}
    </main>
  )
}
