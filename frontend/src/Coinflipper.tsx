import { useState } from "react"
import "./style.css"

type Face = "heads" | "tails"
type CoinState = "idle" | "flipping" | "heads" | "tails"

export default function App() {
  const [selected, setSelected] = useState<Face | null>(null)
  const [result, setResult] = useState<string | null>(null)
  const [balance, setBalance] = useState<number | null>(null)
  const [isFlipping, setIsFlipping] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [bet, setBet] = useState<number>(10)
  const [userId] = useState("demo-student") // anpassen wenn Login fertig ist
  const [coinState, setCoinState] = useState<CoinState>("idle")

  const startFlip = async () => {
    if (isFlipping) return
    if (!selected) {
      setError("Bitte wähle zuerst Kopf oder Zahl.")
      return
    }

    setError(null)
    setResult(null)
    setIsFlipping(true)
    setCoinState("flipping")

    const playReq = (async () => {
      const res = await fetch("/coinflip/play", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId, choice: selected, bet }),
      })
      if (!res.ok) throw new Error(`Fehler: ${res.status}`)
      return res.json() as Promise<{ win: boolean; outcome: Face; balance: number }>
    })()

    const minDelay = new Promise<void>((resolve) => setTimeout(() => resolve(), 2000))

    try {
      const [data] = await Promise.all([playReq, minDelay])

      setCoinState(data.outcome === "heads" ? "heads" : "tails")
      const message = data.win
        ? `🎉 Gewonnen! (${data.outcome.toUpperCase()})`
        : `😢 Verloren! (${data.outcome.toUpperCase()})`
      setResult(message)
      setBalance(data.balance)
    } catch (e: any) {
      setError(e?.message ?? "Unbekannter Fehler")
      // In Fehlerfall Münze wieder in Ruheposition bringen
      setCoinState("idle")
    } finally {
      setIsFlipping(false)
    }
  }

  const select = (choice: Face) => {
    if (isFlipping) return
    setSelected(choice)
    setError(null)
  }

  const coinClass = ["coin"]
  if (coinState === "flipping") coinClass.push("flipping")
  if (coinState === "heads") coinClass.push("show-heads")
  if (coinState === "tails") coinClass.push("show-tails")

  return (
    <div className="page">
      <h1>🪙 Coinflipper</h1>

      <div className="coin-container">
        <div className={coinClass.join(" ")} id="coin">
          <div className="coin-face heads">H</div>
          <div className="coin-face tails">T</div>
        </div>
      </div>

      <button
        className="start-button"
        id="startButton"
        onClick={startFlip}
        disabled={isFlipping || !selected}
      >
        {isFlipping ? "WIRF..." : "FLIP COIN"}
      </button>

      <p>Einsatz wählen und Seite auswählen</p>

      <div className="buttons">
        <button onClick={() => setBet(10)} disabled={isFlipping}>10</button>
        <button onClick={() => setBet(25)} disabled={isFlipping}>25</button>
        <button onClick={() => setBet(50)} disabled={isFlipping}>50</button>
        <button onClick={() => setBet(100)} disabled={isFlipping}>100</button>
        <button onClick={() => setBet(500)} disabled={isFlipping}>500</button>
      </div>

      <p style={{ marginTop: 10 }}>Einsatz: {bet} Coins</p>

      <div className="buttons">
        <button
          className={selected === "heads" ? "selected" : undefined}
          onClick={() => select("heads")}
          disabled={isFlipping}
        >
          Kopf
        </button>
        <button
          className={selected === "tails" ? "selected" : undefined}
          onClick={() => select("tails")}
          disabled={isFlipping}
        >
          Zahl
        </button>
      </div>

      <p>100% Gewinn bei richtiger Wahl</p>

      {isFlipping && <p>Wird geworfen...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {result && <p style={{ fontSize: 18, marginTop: 10 }}>{result}</p>}
      {balance !== null && <p>💰 Guthaben: {balance}</p>}
    </div>
  )
}
