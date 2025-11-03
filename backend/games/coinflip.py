# games/coinflip.py
from secrets import randbits

def flip_coin() -> str:
    """Faire 50/50-Münze, liefert 'heads' oder 'tails'."""
    return "heads" if randbits(1) == 0 else "tails"

if __name__ == "__main__":
    # Test the coin flip function
    results = {"heads": 0, "tails": 0}
    for _ in range(1000):
        result = flip_coin()
        results[result] += 1
    print(f"After 1000 flips: {results}")