# games/__init__.py
from .coinflip import router as coinflip_router
# from .blackjack import router as blackjack_router  # Beispiel für weiteres Spiel

all_games = {
    "coinflip": coinflip_router
    # "blackjack": blackjack_router,
}
