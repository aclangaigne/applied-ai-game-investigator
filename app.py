# app.py
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    reset_game_state,
)

# FIX: Refactored core game logic into logic_utils.py (separates UI from logic; easier to test).


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


# ---- Session State Init ----
if "secret" not in st.session_state:
    st.session_state.secret = None
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []

# Track difficulty/range so a change can re-seed the game cleanly.
if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty
if "range" not in st.session_state:
    st.session_state.range = (low, high)

# If first load OR difficulty changed, start a fresh game in the correct range.
if st.session_state.secret is None or st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.range = (low, high)
    reset_game_state(st.session_state, low, high)
    #FIX Cleared the input widget value for this difficulty so the box is empty on difficulty change
    st.session_state[f"guess_input_{difficulty}"] = ""


st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("check_guess comes from:", check_guess.__module__)
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)
#FIX: Refactored logic into app.py using Copilot Agent mode
    # Diagnostic: show the current stored value for the guess input widget
    st.write(
        "Stored widget value (guess_input key):",
        st.session_state.get(f"guess_input_{difficulty}"),
    )


raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIXME: New Game previously did not fully reset session_state and ignored difficulty range.
if new_game:
    # FIX: Reset all relevant session_state fields consistently (secret/attempts/score/status/history),
    # and re-roll secret inside the selected difficulty range.
    reset_game_state(st.session_state, low, high)
    # Also clear the visible text input (Streamlit preserves widget values by key across reruns)
    st.session_state[f"guess_input_{difficulty}"] = ""
    st.success("New game started.")
    st.rerun()

# Stop if game already ended
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret  # FIX: Keep secret as int; avoid unreliable string comparisons.
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

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
