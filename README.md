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
- [ ] 1. game accepted negative numbers which is wrong
- [ ] 2. prompted to go higher/lower when it meant the opposite
- [ ] 3. attempt count was off by 1. Overcounted.
- [ ] 4. even integer was casted to string, so it never matches the target.
- [ ] 5. kept UI logic in app.py and moved pure game logic to logic_utils.py
- [x] Explain what fixes you applied.
- [ ]  Step 1 — Refactored logic out of the UI

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

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
