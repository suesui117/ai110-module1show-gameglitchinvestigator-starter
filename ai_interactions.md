# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**Agent used:** Claude Code (agent mode)

**What task did you give the agent?**

"Plan and implement a Guess History visualization: a sidebar that shows each
previous guess and how close it was to the secret (hot / warm / cold), then add
tests and document the work." I asked it to keep the closeness math as pure,
testable logic (no Streamlit) and only render in `app.py`.

**Files modified:**

- `logic_utils.py` — added two pure functions:
  - `guess_closeness(guess, secret, low, high)` → `(distance, label, closeness)`
    where label is `correct/hot/warm/cold` and closeness is a 0.0–1.0 bar value.
  - `history_rows(history, secret, low, high)` → builds one row per numeric
    guess, skipping invalid string entries.
- `app.py` — imported `history_rows` and added a "📊 Guess History" sidebar
  section that renders a `st.sidebar.progress` bar + emoji label per guess
  (newest first). Placed after the submit handler so it includes the latest guess.
- `test/test_game_logic.py` — added `TestGuessCloseness` (7 tests) and
  `TestHistoryRows` (4 tests).

**What did the agent do?**

1. Asked which feature to build (High Score vs Guess History) before starting.
2. Wrote a short plan (pure logic + sidebar UI + tests + docs).
3. Implemented the two pure functions, then wired the sidebar render.
4. Added 11 new pytest cases; ran the full suite → 59 passed.
5. Verified the app runs with no exceptions via Streamlit's `AppTest`, then
   restarted the local server so the feature could be viewed.

**What did you have to verify or fix manually?**

- The agent's *verification probe* used `at.sidebar.progress` / `at.progress`,
  which aren't valid accessors in this Streamlit version — that crashed the probe
  script (not the app). It self-corrected to check `at.exception` and the sidebar
  subheader instead, confirming the app rendered cleanly.
- Known limitation we noted together: because the sidebar history renders after
  the `st.stop()` game-over guard, it shows during play and on the winning/losing
  turn, but not on later reruns of the game-over screen. Acceptable for now;
  fixing it would mean restructuring the status guard.
- I confirmed the feature visually in the browser (hot/warm/cold bars matched how
  close my guesses actually were).

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| | | | | |
| | | | | |
| | | | | |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
