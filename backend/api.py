from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db import init_db, ensure_user, get_balance
from games import all_games

api = FastAPI(title="Casino API")
api.include_router(coinflip_router)
# DB vorbereiten
init_db()

@api.on_event("startup")
def _print_routes():
    for r in api.routes:
        print(r.path, getattr(r, "methods", None))

@api.post("/api/flip", response_model=CoinflipResult)
def legacy_flip(req: CoinflipRequest):
    return play(req)
        
# user anlage
@api.get("/api/balance")
def balance(userId: str):
    ensure_user(userId)
    return {"userId": userId, "balance": get_balance(userId)}

# verweist auf games/__init__
for name, router in all_games.items():
    api.include_router(router, prefix=f"/{name}", tags=[name])

# Verknüpfung mit Frontend
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
api.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="static")
