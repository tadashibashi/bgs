
def clamp(n: float | int, low: float | int, high: float | int) -> float | int:
    return max(min(n, high), low)
