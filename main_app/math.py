
def clamp(n: float | int, low: float | int, high: float | int) -> float | int:
    """
        Clamps a number between two values inclusively.

        Args:
            n: number to clamp
            low: lower limit
            high: upper limit
    """
    return max(min(n, high), low)
