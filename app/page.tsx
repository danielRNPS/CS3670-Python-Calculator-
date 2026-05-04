import { Calculator } from "@/components/calculator"

export default function Home() {
  return (
    <main className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
      <div className="mb-8 text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <div className="flex gap-1">
            <div className="w-6 h-6 rounded-full bg-secondary" />
            <div className="w-6 h-6 rounded-full bg-primary" />
          </div>
          <h1 className="text-3xl font-bold text-foreground font-mono">PyCalc</h1>
        </div>
        <p className="text-muted-foreground text-sm">A Python-inspired calculator</p>
      </div>
      <Calculator />
    </main>
  )
}
