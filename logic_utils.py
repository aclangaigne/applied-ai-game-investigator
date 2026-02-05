import random
from typing import Optional, Tuple


def get_range_for_difficulty(difficulty: str) -> Tuple[int, int]:
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: Optional[str]):
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int):
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: Hint direction bug (Too High -> Go LOWER, Too Low -> Go HIGHER)
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def reset_game_state(session_state, low: int, high: int):
    session_state.secret = random.randint(low, high)
    session_state.attempts = 0
    session_state.score = 0
    session_state.status = "playing"
    session_state.history = []
