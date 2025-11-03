# api.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from games.coinflip import flip_coin
from db import get_balance, add_balance, ensure_user, log_bet

# --- Setup ---
api = FastAPI(title="Coinflipper")

# --- feste Einsätze ---
BET_OPTIONS = (10, 25, 50, 100, 500)


# --- Eingabemodell für das Spiel ---
class FlipRequest(BaseModel):
    userId: str
    choice: str   # "heads" oder "tails"
    bet: int


# --- Spielroute ---
@api.post("/api/flip")
def flip(req: FlipRequest):
    ensure_user(req.userId)

    # Einsatz prüfen
    if req.bet not in BET_OPTIONS:
        raise HTTPException(status_code=400, detail=f"Bet must be one of {BET_OPTIONS}")

    # Guthaben prüfen
    balance = get_balance(req.userId)
    if balance < req.bet:
        raise HTTPException(status_code=400, detail="Not enough coins!")

    # Coin flip
    outcome = flip_coin()
    win = (outcome == req.choice)
    delta = req.bet if win else -req.bet
    new_balance = add_balance(req.userId, delta)

    log_bet(req.userId, req.choice, outcome, req.bet, new_balance)

    return {"outcome": outcome, "win": win, "balance": new_balance}


# --- Guthaben abrufen ---
@api.get("/api/balance")
def balance(userId: str):
    ensure_user(userId)
    return {"userId": userId, "balance": get_balance(userId)}


# --- Frontend ausliefern ---
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
api.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="static")
