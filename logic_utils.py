def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


# FIX: Extracted this helper with Claude Code (agent mode) to fix the
# "New Game freezes after winning" bug -- the old inline reset never set
# status back to "playing". Now both first-load and New Game share it.
def new_game_state(secret: int):
    """
    Return a fresh game-state dict for a brand-new game.

    Used for both the very first load and the "New Game" button, so the
    two can never drift apart. A new game is always: playing, score 0,
    no attempts used, empty history, with the given secret.
    """
    return {
        "secret": secret,
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
    }


def parse_guess(raw: str, low: int = 1, high: int = 100):
    """
    Parse user input into an int guess.

    Validates that the guess falls within [low, high] (inclusive).

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        number = float(raw)
    except Exception:
        return False, None, "That is not a number."

    # FIX: paired with Claude Code (agent mode). Old code did int(float(raw))
    # which silently truncated "6.6" -> 6 and accepted it. Now reject any
    # non-whole number: reject 6.6, accept 6 or 6.0.
    if number != int(number):
        return False, None, "Enter a whole number (no decimals)."

    value = int(number)

    # FIX: range was hardcoded to 1-100 for every difficulty. Now takes
    # (low, high) so Easy (1-20) and Hard (1-50) validate correctly.
    if value < low or value > high:
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: rewritten with Claude Code (agent mode). Old version had a buggy
    # try/except fallback that swapped the hint directions (Too High -> "Go
    # HIGHER"). Removed the dead branch; directions are now correct.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
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


# FEATURE (stretch): Guess History visualization. Built with Claude Code
# (agent mode). Pure logic so the "how close was each guess" math is unit-
# testable without Streamlit; app.py renders the result in the sidebar.
def guess_closeness(guess: int, secret: int, low: int, high: int):
    """
    Describe how close a guess is to the secret.

    Returns (distance, label, closeness):
      - distance:  abs(guess - secret)
      - label:     "correct" | "hot" | "warm" | "cold"
      - closeness: float in [0.0, 1.0]; 1.0 = exact match, 0.0 = as far as
                   possible within [low, high].
    """
    distance = abs(guess - secret)
    span = max(high - low, 1)  # guard against divide-by-zero
    closeness = max(0.0, 1.0 - distance / span)

    if distance == 0:
        label = "correct"
    elif distance <= 0.10 * span:
        label = "hot"
    elif distance <= 0.25 * span:
        label = "warm"
    else:
        label = "cold"

    return distance, label, closeness


def history_rows(history, secret: int, low: int, high: int):
    """
    Build closeness rows for the numeric guesses in `history`.

    Invalid inputs are stored in history as raw strings; those are skipped.
    Returns a list of dicts (in the same order as history):
        {"guess": int, "distance": int, "label": str, "closeness": float}
    """
    rows = []
    for entry in history:
        # bool is a subclass of int -- exclude it so True/False aren't charted.
        if isinstance(entry, int) and not isinstance(entry, bool):
            distance, label, closeness = guess_closeness(entry, secret, low, high)
            rows.append(
                {
                    "guess": entry,
                    "distance": distance,
                    "label": label,
                    "closeness": closeness,
                }
            )
    return rows
