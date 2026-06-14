import random
import streamlit as st

# FIX: Refactored all pure game logic out of app.py into logic_utils.py
# using Claude Code (agent mode), then imported it here. UI stays in app.py.
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    new_game_state,
)

# UI starts here. All pure game logic now lives in logic_utils.py.
st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "status" not in st.session_state:
    # FIX: paired with Claude Code (agent mode) to share new_game_state() with
    # the New Game button, fixing the attempts 1-vs-0 mismatch. Start at 0.
    st.session_state.update(new_game_state(random.randint(low, high)))

st.subheader("Make a guess")

st.info(f"Guess a number between {low} and {high}.")

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: rewritten with Claude Code (agent mode). Old reset never set status
    # back to "playing", so the game stayed frozen after a win. Full reset now.
    st.session_state.update(new_game_state(random.randint(low, high)))
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    # FIX: paired with Claude Code (agent mode) to pass the difficulty range
    # (low, high) into parse_guess instead of the old hardcoded 1-100.
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: high/low hint bug resolved in logic_utils.check_guess (was a
        # stale "# FIXME: Logic breaks here" marker).
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# FIX: moved here with Claude Code (agent mode). This used to render ABOVE the
# submit handler, so the count lagged one click behind. Rendering it AFTER the
# handler means it reflects the guess just made (attempts incremented above).
st.info(f"Attempts left: {attempt_limit - st.session_state.attempts}")

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
