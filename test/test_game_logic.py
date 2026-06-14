"""
Pytest cases for the pure game logic in logic_utils.py.

Run from the project root with:
    pytest

Each section targets a specific bug that was fixed during refactoring.
"""

import pytest

from streamlit.testing.v1 import AppTest

from logic_utils import (
    parse_guess,
    check_guess,
    get_range_for_difficulty,
    new_game_state,
)


def _attempts_left_text(at):
    """Return the 'Attempts left: N' info box text from a rendered app, or None."""
    for box in at.info:
        if "Attempts left" in box.value:
            return box.value
    return None


def _wrong_guess(at):
    """An in-range guess string guaranteed NOT to equal the secret.

    Avoids accidentally winning (which would freeze further submits and make
    multi-guess tests flaky depending on the random secret).
    """
    secret = at.session_state["secret"]
    return "1" if secret != 1 else "2"


# ---------------------------------------------------------------------------
# THE BUG WE JUST FIXED: decimals were silently truncated and accepted.
# "6.6" became 6, "91.1" became 91 -- a decimal could win the game.
# A guess must be a WHOLE number; decimals are rejected.
# ---------------------------------------------------------------------------
class TestDecimalGuessesRejected:
    def test_6_point_6_is_rejected(self):
        ok, value, err = parse_guess("6.6", 1, 20)
        assert ok is False
        assert value is None
        assert err is not None

    def test_91_point_1_is_rejected(self):
        ok, value, err = parse_guess("91.1", 1, 100)
        assert ok is False
        assert value is None

    @pytest.mark.parametrize("raw", ["3.5", "0.1", "99.9", "12.0001", "-4.2"])
    def test_various_decimals_rejected(self, raw):
        ok, _, _ = parse_guess(raw, 1, 100)
        assert ok is False

    def test_whole_number_string_still_accepted(self):
        assert parse_guess("6", 1, 20) == (True, 6, None)

    def test_whole_number_with_trailing_zero_accepted(self):
        # "6.0" is mathematically a whole number, so it stays valid.
        assert parse_guess("6.0", 1, 20) == (True, 6, None)


# ---------------------------------------------------------------------------
# Range bug: validation was hardcoded to 1-100 for every difficulty.
# It must respect the difficulty's actual (low, high) range.
# ---------------------------------------------------------------------------
class TestRangeIsDifficultyAware:
    def test_50_rejected_on_easy_range(self):
        # Easy is 1-20, so 50 is out of range.
        ok, _, err = parse_guess("50", 1, 20)
        assert ok is False
        assert "1" in err and "20" in err

    def test_in_range_value_accepted(self):
        assert parse_guess("15", 1, 20) == (True, 15, None)

    def test_boundaries_inclusive(self):
        assert parse_guess("1", 1, 20)[0] is True
        assert parse_guess("20", 1, 20)[0] is True

    def test_just_outside_boundaries_rejected(self):
        assert parse_guess("0", 1, 20)[0] is False
        assert parse_guess("21", 1, 20)[0] is False


# ---------------------------------------------------------------------------
# Non-numeric / empty input handling.
# ---------------------------------------------------------------------------
class TestBadInput:
    @pytest.mark.parametrize("raw", ["abc", "", None, "  ", "1.2.3"])
    def test_invalid_input_rejected(self, raw):
        ok, value, err = parse_guess(raw, 1, 100)
        assert ok is False
        assert value is None
        assert err is not None


# ---------------------------------------------------------------------------
# Negative guesses: a guess below the range's low bound must be rejected.
# A negative WHOLE number is rejected by the range check; a negative
# DECIMAL is rejected by the whole-number check first.
# ---------------------------------------------------------------------------
class TestNegativeGuesses:
    @pytest.mark.parametrize("raw", ["-1", "-5", "-100"])
    def test_negative_whole_number_rejected_by_range(self, raw):
        ok, value, err = parse_guess(raw, 1, 100)
        assert ok is False
        assert value is None
        assert "1" in err and "100" in err  # range message

    @pytest.mark.parametrize("raw", ["-4.2", "-0.5", "-99.9"])
    def test_negative_decimal_rejected_as_non_whole(self, raw):
        ok, value, err = parse_guess(raw, 1, 100)
        assert ok is False
        assert value is None
        assert "whole" in err.lower()  # decimal check fires first

    def test_zero_rejected_when_low_is_one(self):
        ok, _, err = parse_guess("0", 1, 100)
        assert ok is False
        assert "1" in err and "100" in err


# ---------------------------------------------------------------------------
# High/Low bug: the hint direction was swapped in the old fallback branch.
# Too High must say "go LOWER"; Too Low must say "go HIGHER".
# ---------------------------------------------------------------------------
class TestCheckGuessDirection:
    def test_correct_guess_wins(self):
        outcome, _ = check_guess(42, 42)
        assert outcome == "Win"

    def test_too_high_tells_you_to_go_lower(self):
        outcome, message = check_guess(60, 42)
        assert outcome == "Too High"
        assert "LOWER" in message.upper()

    def test_too_low_tells_you_to_go_higher(self):
        outcome, message = check_guess(10, 42)
        assert outcome == "Too Low"
        assert "HIGHER" in message.upper()

    def test_one_below_secret_is_too_low(self):
        outcome, message = check_guess(41, 42)
        assert outcome == "Too Low"
        assert "HIGHER" in message.upper()

    def test_one_above_secret_is_too_high(self):
        outcome, message = check_guess(43, 42)
        assert outcome == "Too High"
        assert "LOWER" in message.upper()

    @pytest.mark.parametrize(
        "guess,secret,expected_outcome,expected_word",
        [
            (1, 100, "Too Low", "HIGHER"),    # extreme low end
            (100, 1, "Too High", "LOWER"),    # extreme high end
            (20, 20, "Win", "CORRECT"),       # exact match at a boundary
        ],
    )
    def test_direction_at_extremes(self, guess, secret, expected_outcome, expected_word):
        outcome, message = check_guess(guess, secret)
        assert outcome == expected_outcome
        assert expected_word in message.upper()


# ---------------------------------------------------------------------------
# New Game bug: after winning, the game used to stay frozen because the reset
# never set status back to "playing". A new game must be a truly fresh game,
# regardless of what the previous game's state was.
# ---------------------------------------------------------------------------
class TestNewGameIsFresh:
    def test_fresh_game_is_playing(self):
        assert new_game_state(7)["status"] == "playing"

    def test_fresh_game_has_zero_attempts(self):
        assert new_game_state(7)["attempts"] == 0

    def test_fresh_game_has_zero_score(self):
        assert new_game_state(7)["score"] == 0

    def test_fresh_game_has_empty_history(self):
        assert new_game_state(7)["history"] == []

    def test_fresh_game_uses_given_secret(self):
        assert new_game_state(42)["secret"] == 42

    def test_new_game_after_winning_resets_everything(self):
        # Simulate a finished, won game with score and history built up...
        won_game = {
            "secret": 13,
            "attempts": 6,
            "score": 250,
            "status": "won",
            "history": [5, 20, 13],
        }
        # ...then "click New Game": apply the fresh state on top of it.
        won_game.update(new_game_state(88))

        # It must now be a brand-new, playable game -- not frozen on "won".
        assert won_game["status"] == "playing"
        assert won_game["attempts"] == 0
        assert won_game["score"] == 0
        assert won_game["history"] == []
        assert won_game["secret"] == 88

    def test_history_is_a_fresh_list_each_time(self):
        # Guard against a shared mutable default leaking between games.
        a = new_game_state(1)
        a["history"].append(99)
        b = new_game_state(2)
        assert b["history"] == []


# ---------------------------------------------------------------------------
# Difficulty range table.
# ---------------------------------------------------------------------------
class TestDifficultyRanges:
    @pytest.mark.parametrize(
        "difficulty,expected",
        [
            ("Easy", (1, 20)),
            ("Normal", (1, 100)),
            ("Hard", (1, 50)),
        ],
    )
    def test_known_difficulties(self, difficulty, expected):
        assert get_range_for_difficulty(difficulty) == expected

    def test_unknown_difficulty_defaults_to_1_100(self):
        assert get_range_for_difficulty("???") == (1, 100)


# ---------------------------------------------------------------------------
# Integration tests: run the actual app.py via Streamlit's AppTest harness.
# These catch UI-level bugs the pure-logic tests can't see -- like the
# "Attempts left" counter lagging one click behind because it was rendered
# BEFORE the counter incremented (a render-order bug).
# ---------------------------------------------------------------------------
class TestAttemptsCounterInApp:
    def test_attempts_start_at_zero_before_any_guess(self):
        at = AppTest.from_file("app.py")
        at.run()
        assert at.session_state["attempts"] == 0
        assert _attempts_left_text(at) == "Attempts left: 8"  # Normal limit is 8

    def test_attempts_increment_to_one_after_first_submit(self):
        at = AppTest.from_file("app.py")
        at.run()

        at.text_input[0].set_value("50")
        at.button[0].click().run()  # Submit Guess

        # The counter incremented...
        assert at.session_state["attempts"] == 1
        # ...AND the display reflects it immediately (the render-order fix).
        assert _attempts_left_text(at) == "Attempts left: 7"

    def test_attempts_keep_incrementing_on_each_submit(self):
        at = AppTest.from_file("app.py")
        at.run()

        wrong = _wrong_guess(at)  # never wins, so submits keep working
        for expected in (1, 2, 3):
            at.text_input[0].set_value(wrong)
            at.button[0].click().run()
            assert at.session_state["attempts"] == expected

        assert _attempts_left_text(at) == "Attempts left: 5"  # 8 - 3


class TestNewGameResetsCounterInApp:
    def test_new_game_resets_attempts_to_zero(self):
        at = AppTest.from_file("app.py")
        at.run()

        # Make a couple of (deliberately wrong) guesses...
        wrong = _wrong_guess(at)
        at.text_input[0].set_value(wrong)
        at.button[0].click().run()
        at.text_input[0].set_value(wrong)
        at.button[0].click().run()
        assert at.session_state["attempts"] == 2

        # ...then click "New Game" (second button) -> fresh game.
        at.button[1].click().run()
        assert at.session_state["attempts"] == 0
        assert at.session_state["status"] == "playing"
        assert at.session_state["score"] == 0
        assert at.session_state["history"] == []
