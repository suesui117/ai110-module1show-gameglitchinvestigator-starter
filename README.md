# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose. This is a fun mini game where user are prompt to enter an integer number between the range indicated by the level. User has x amount of attempts. If the user guessed the target correctly, game ends with a successful message. Within the attempts allowed, user is allowed multiple attempts.
- [x] Detail which bugs you found.
- [x] 1. game accepted negative numbers which is wrong
- [x] 2. prompted to go higher/lower when it meant the opposite
- [x] 3. attempt count was off by 1. Overcounted.
- [x] 4. even integer was casted to string, so it never matches the target.
- [x] 5. kept UI logic in app.py and moved pure game logic to logic_utils.py
- [x] Explain what fixes you applied.
- [x]  Step 1 — Refactored logic out of the UI

Moved check_guess, parse_guess, get_range_for_difficulty, update_score from app.py → logic_utils.py.
app.py now imports them; UI (anything st.) stayed put. This made the logic testable on its own.
Step 2 — Fixed the high/low hint bug

check_guess had a dead try/except branch that said "Go HIGHER" when you guessed too high. Removed it so directions are correct.
Step 3 — Fixed the hardcoded range bug

Validation accepted 1–100 for every difficulty. Made parse_guess take (low, high), and synced the info box, validation, secret generation, and New Game to the real range (Easy 1–20, Hard 1–50).
Step 4 — Fixed the decimal bug

6.6 / 91.1 were silently truncated and accepted. Now parse_guess rejects non-whole numbers (keeps 6 and 6.0).
Step 5 — Fixed New Game freezing after a win

The reset never set status back to "playing". Built one new_game_state() helper for a full, clean reset (status, score, history, attempts).
Step 6 — Fixed the attempts off-by-one

First load started attempts at 1, New Game at 0. Unified both to 0 via new_game_state().
Step 7 — Fixed the "Attempts left" display lag

It was rendered before the counter incremented, so it lagged a click. Moved the display below the submit handler.
Step 8 — Wrote tests

Added test/test_game_logic.py: 48 pytest cases (pure-logic + Streamlit AppTest integration) covering every fix above.
Step 9 — Documented & shipped

Added # FIX: comments at each fix, then committed and pushed to GitHub.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User can select the diffculty of the game on the left panel
2. User enters an integer between the range indicated such as 40
3. Game returns "Go Higher" if target is 59, and user entered 40
4. Score is updated after each guess
5. When the user guessed the target correctly, game ends.
6. User has the option to start a new game anytime and score and attempts reset.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```Bash
============================= test session starts ==============================
platform darwin -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0 -- /Users/sue/Desktop/codepath-AI110/week2/ai110-module1show-gameglitchinvestigator-starter/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/sue/Desktop/codepath-AI110/week2/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collecting ... collected 48 items

test/test_game_logic.py::TestDecimalGuessesRejected::test_6_point_6_is_rejected PASSED [  2%]
test/test_game_logic.py::TestDecimalGuessesRejected::test_91_point_1_is_rejected PASSED [  4%]
test/test_game_logic.py::TestDecimalGuessesRejected::test_various_decimals_rejected[3.5] PASSED [  6%]
test/test_game_logic.py::TestDecimalGuessesRejected::test_various_decimals_rejected[0.1] PASSED [  8%]
test/test_game_logic.py::TestDecimalGuessesRejected::test_various_decimals_rejected[99.9] PASSED [ 10%]
test/test_game_logic.py::TestDecimalGuessesRejected::test_various_decimals_rejected[12.0001] PASSED [ 12%]
test/test_game_logic.py::TestDecimalGuessesRejected::test_various_decimals_rejected[-4.2] PASSED [ 14%]
test/test_game_logic.py::TestDecimalGuessesRejected::test_whole_number_string_still_accepted PASSED [ 16%]
test/test_game_logic.py::TestDecimalGuessesRejected::test_whole_number_with_trailing_zero_accepted PASSED [ 18%]
test/test_game_logic.py::TestRangeIsDifficultyAware::test_50_rejected_on_easy_range PASSED [ 20%]
test/test_game_logic.py::TestRangeIsDifficultyAware::test_in_range_value_accepted PASSED [ 22%]
test/test_game_logic.py::TestRangeIsDifficultyAware::test_boundaries_inclusive PASSED [ 25%]
test/test_game_logic.py::TestRangeIsDifficultyAware::test_just_outside_boundaries_rejected PASSED [ 27%]
test/test_game_logic.py::TestBadInput::test_invalid_input_rejected[abc] PASSED [ 29%]
test/test_game_logic.py::TestBadInput::test_invalid_input_rejected[] PASSED [ 31%]
test/test_game_logic.py::TestBadInput::test_invalid_input_rejected[None] PASSED [ 33%]
test/test_game_logic.py::TestBadInput::test_invalid_input_rejected[  ] PASSED [ 35%]
test/test_game_logic.py::TestBadInput::test_invalid_input_rejected[1.2.3] PASSED [ 37%]
test/test_game_logic.py::TestNegativeGuesses::test_negative_whole_number_rejected_by_range[-1] PASSED [ 39%]
test/test_game_logic.py::TestNegativeGuesses::test_negative_whole_number_rejected_by_range[-5] PASSED [ 41%]
test/test_game_logic.py::TestNegativeGuesses::test_negative_whole_number_rejected_by_range[-100] PASSED [ 43%]
test/test_game_logic.py::TestNegativeGuesses::test_negative_decimal_rejected_as_non_whole[-4.2] PASSED [ 45%]
test/test_game_logic.py::TestNegativeGuesses::test_negative_decimal_rejected_as_non_whole[-0.5] PASSED [ 47%]
test/test_game_logic.py::TestNegativeGuesses::test_negative_decimal_rejected_as_non_whole[-99.9] PASSED [ 50%]
test/test_game_logic.py::TestNegativeGuesses::test_zero_rejected_when_low_is_one PASSED [ 52%]
test/test_game_logic.py::TestCheckGuessDirection::test_correct_guess_wins PASSED [ 54%]
test/test_game_logic.py::TestCheckGuessDirection::test_too_high_tells_you_to_go_lower PASSED [ 56%]
test/test_game_logic.py::TestCheckGuessDirection::test_too_low_tells_you_to_go_higher PASSED [ 58%]
test/test_game_logic.py::TestCheckGuessDirection::test_one_below_secret_is_too_low PASSED [ 60%]
test/test_game_logic.py::TestCheckGuessDirection::test_one_above_secret_is_too_high PASSED [ 62%]
test/test_game_logic.py::TestCheckGuessDirection::test_direction_at_extremes[1-100-Too Low-HIGHER] PASSED [ 64%]
test/test_game_logic.py::TestCheckGuessDirection::test_direction_at_extremes[100-1-Too High-LOWER] PASSED [ 66%]
test/test_game_logic.py::TestCheckGuessDirection::test_direction_at_extremes[20-20-Win-CORRECT] PASSED [ 68%]
test/test_game_logic.py::TestNewGameIsFresh::test_fresh_game_is_playing PASSED [ 70%]
test/test_game_logic.py::TestNewGameIsFresh::test_fresh_game_has_zero_attempts PASSED [ 72%]
test/test_game_logic.py::TestNewGameIsFresh::test_fresh_game_has_zero_score PASSED [ 75%]
test/test_game_logic.py::TestNewGameIsFresh::test_fresh_game_has_empty_history PASSED [ 77%]
test/test_game_logic.py::TestNewGameIsFresh::test_fresh_game_uses_given_secret PASSED [ 79%]
test/test_game_logic.py::TestNewGameIsFresh::test_new_game_after_winning_resets_everything PASSED [ 81%]
test/test_game_logic.py::TestNewGameIsFresh::test_history_is_a_fresh_list_each_time PASSED [ 83%]
test/test_game_logic.py::TestDifficultyRanges::test_known_difficulties[Easy-expected0] PASSED [ 85%]
test/test_game_logic.py::TestDifficultyRanges::test_known_difficulties[Normal-expected1] PASSED [ 87%]
test/test_game_logic.py::TestDifficultyRanges::test_known_difficulties[Hard-expected2] PASSED [ 89%]
test/test_game_logic.py::TestDifficultyRanges::test_unknown_difficulty_defaults_to_1_100 PASSED [ 91%]
test/test_game_logic.py::TestAttemptsCounterInApp::test_attempts_start_at_zero_before_any_guess PASSED [ 93%]
test/test_game_logic.py::TestAttemptsCounterInApp::test_attempts_increment_to_one_after_first_submit PASSED [ 95%]
test/test_game_logic.py::TestAttemptsCounterInApp::test_attempts_keep_incrementing_on_each_submit PASSED [ 97%]
test/test_game_logic.py::TestNewGameResetsCounterInApp::test_new_game_resets_attempts_to_zero PASSED [100%]

============================== 48 passed in 0.68s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
