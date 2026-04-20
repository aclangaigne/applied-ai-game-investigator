import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    update_score,
    reset_game_state,
    validate_guess,
    build_investigation_report,
)

st.set_page_config(page_title="Game Investigator AI", page_icon="🎮")

st.title("🎮 Game Investigator AI")
st.caption("A specialized AI-style investigator for analyzing number guesses.")

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

# Session state initialization
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
if "guess_history" not in st.session_state:
    st.session_state.guess_history = []
if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

# Initialize or reset when difficulty changes
if st.session_state.secret is None or st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    reset_game_state(st.session_state, low, high)

st.markdown("## Investigation Dashboard")
m1, m2, m3 = st.columns(3)
m1.metric("Score", st.session_state.score)
m2.metric("Attempts Used", st.session_state.attempts)
m3.metric("Attempts Left", max(attempt_limit - st.session_state.attempts, 0))

st.info(
    f"Guess a number between {low} and {high}. "
    f"Use the investigator feedback to narrow down the target."
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("Raw history:", st.session_state.history)

raw_guess = st.text_input("Enter your guess:")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_reasoning = st.checkbox("Show reasoning trace", value=True)

if new_game:
    reset_game_state(st.session_state, low, high)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")

if submit and st.session_state.status == "playing":
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    else:
        is_valid, validation_message = validate_guess(guess_int, low, high)

        if not is_valid:
            st.error(validation_message)
        else:
            st.session_state.attempts += 1
            st.session_state.history.append(guess_int)

            report = build_investigation_report(
                guess=guess_int,
                secret=st.session_state.secret,
                difficulty=difficulty,
            )

            st.session_state.guess_history.append(
                {
                    "Guess": guess_int,
                    "Status": report["status"],
                    "Hint": report["hint"],
                    "Confidence": round(report["confidence"], 2),
                }
            )

            st.markdown("### AI Reliability Feedback")
            c1, c2, c3 = st.columns(3)
            c1.metric("Latest Guess", guess_int)
            c2.metric("Outcome", report["status"])
            c3.metric("Confidence", f"{report['confidence']:.2f}")

            st.progress(report["confidence"])

            st.markdown("### Investigator Report")
            st.write(report["summary"])

            if show_reasoning:
                st.markdown("### Reasoning Trace")
                for step in report["reasoning"]:
                    st.write(f"- {step}")

            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=report["status"],
                attempt_number=st.session_state.attempts,
            )

            if report["status"] == "Win":
                st.balloons()
                st.session_state.status = "won"
                st.success(
                    f"You solved it. The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            elif st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts. The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.markdown("### Investigation History")
if st.session_state.guess_history:
    st.table(st.session_state.guess_history)
else:
    st.caption("No guesses submitted yet.")

st.divider()
st.caption("Extended into a specialized AI-style investigator with reliability feedback.")