import { useState } from "react"
import "./style.css"

export default function App() {
  const [result, setResult] = useState<string | null>(null)
  const [balance, setBalance] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [bet, setBet] = useState<number>(10)
  const [userId] = useState("demo-student") // anpassen wenn Loginmaske fertig ist

  const handleFlip = async (choice: "heads" | "tails") => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const res = await fetch("/coinflip/play", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId, choice, bet }),
      })

      if (!res.ok) throw new Error(`Fehler: ${res.status}`)

      const data = await res.json()
      const message = data.win
        ? `🎉 Gewonnen! (${data.outcome.toUpperCase()})`
        : `😢 Verloren! (${data.outcome.toUpperCase()})`
      setResult(message)
      setBalance(data.balance)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <h1>🪙 Coinflipper</h1>

      <p>Einsatz wählen und wette setzten</p>

      <div className="buttons">
        <button onClick={() => setBet(10)}>10</button>
        <button onClick={() => setBet(25)}>25</button>
        <button onClick={() => setBet(50)}>50</button>
        <button onClick={() => setBet(100)}>100</button>
        <button onClick={() => setBet(500)}>500</button>
      </div>

      <p style={{ marginTop: 10 }}>Einsatz: {bet} Coins</p>

      <div className="buttons">
        <button disabled={loading} onClick={() => handleFlip("heads")}>
          Kopf
        </button>
        <button disabled={loading} onClick={() => handleFlip("tails")}>
          Zahl
        </button>
      </div>
      <p>100% Gewinn bei richhtiger Wahl</p>
      
      {loading && <p>Wird geworfen...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {result && <p style={{ fontSize: 18, marginTop: 10 }}>{result}</p>}
      {balance !== null && <p>💰 Guthaben: {balance}</p>}
    </div>
  )
}
