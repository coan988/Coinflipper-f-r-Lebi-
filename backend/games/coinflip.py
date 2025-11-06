from secrets import randbits
from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, PositiveInt

from db import ensure_user, get_balance, add_balance, log_bet

game = "Coinflipper"
router = APIRouter()


BET_OPTIONS = (10, 25, 50, 100, 500)
CHOICES = ("heads", "tails")

class CoinflipRequest(BaseModel):
    userId: str
    choice: Literal["heads", "tails"]
    bet: PositiveInt

class CoinflipResult(BaseModel):
    outcome: Literal["heads", "tails"]
    win: bool
    balance: int

def flip_coin() -> Literal["heads", "tails"]:
    return "heads" if randbits(1) == 0 else "tails"

@router.post("/play", response_model=CoinflipResult)
def play(req: CoinflipRequest):
    ensure_user(req.userId)

    if req.bet not in BET_OPTIONS:
        raise HTTPException(status_code=400, detail=f"Bet must be one of {BET_OPTIONS}")

    current = get_balance(req.userId)
    if current < req.bet:
        raise HTTPException(status_code=400, detail="Not enough coins!")

    outcome = flip_coin()
    win = (outcome == req.choice)
    delta = req.bet if win else -req.bet
    new_balance = add_balance(req.userId, delta)

    # zentrales Logging über DB
    log_bet(req.userId, game, req.choice, outcome, req.bet, new_balance)

    return CoinflipResult(outcome=outcome, win=win, balance=new_balance)

if __name__ == "__main__":
    results = {"heads": 0, "tails": 0}
    for _ in range(1000):
        result = flip_coin()
        results[result] += 1
    print(f"After 1000 flips: {results}")
