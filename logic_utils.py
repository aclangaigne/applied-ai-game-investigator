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

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
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
    session_state.guess_history = []


def validate_guess(guess, low: int, high: int):
    if guess is None:
        return False, "Please enter a guess before submitting."

    if not isinstance(guess, int):
        return False, "Your guess must be a whole number."

    if guess < low or guess > high:
        return False, f"Please enter a number between {low} and {high}."

    return True, ""


def confidence_score(guess, secret):
    distance = abs(guess - secret)

    if distance == 0:
        return 1.0
    if distance <= 2:
        return 0.95
    if distance <= 5:
        return 0.85
    if distance <= 10:
        return 0.70
    if distance <= 20:
        return 0.50
    return 0.25


def investigate_guess(guess, secret):
    outcome, hint = check_guess(guess, secret)

    return {
        "status": outcome,
        "hint": hint,
        "confidence": confidence_score(guess, secret),
    }


def build_investigation_report(guess, secret, difficulty):
    result = investigate_guess(guess, secret)
    distance = abs(guess - secret)

    if result["status"] == "Win":
        reasoning = [
            "Validated the guess.",
            "Compared the guess to the hidden target.",
            "Matched the target exactly.",
            "Marked the case as solved.",
        ]
        summary = (
            f"Investigator Report: The guess {guess} solved the case in {difficulty} mode. "
            f"The evidence fully matches the hidden target."
        )
    elif result["status"] == "Too High":
        reasoning = [
            "Validated the guess.",
            "Compared the guess to the hidden target.",
            "Detected that the guess is above the target.",
            "Recommended moving lower on the next attempt.",
        ]
        summary = (
            f"Investigator Report: The guess {guess} is too high for {difficulty} mode. "
            f"The player should move lower. Distance from target: {distance}."
        )
    else:
        reasoning = [
            "Validated the guess.",
            "Compared the guess to the hidden target.",
            "Detected that the guess is below the target.",
            "Recommended moving higher on the next attempt.",
        ]
        summary = (
            f"Investigator Report: The guess {guess} is too low for {difficulty} mode. "
            f"The player should move higher. Distance from target: {distance}."
        )

    return {
        "summary": summary,
        "reasoning": reasoning,
        "status": result["status"],
        "hint": result["hint"],
        "confidence": result["confidence"],
    }