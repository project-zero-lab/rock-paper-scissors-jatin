import random
import streamlit as st

st.set_page_config(page_title="Rock Paper Scissors", page_icon="✊", layout="centered")

st.markdown(
    """
    <style>
        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.22);
            padding: 14px 16px;
            border-radius: 14px;
        }
        .choice-emoji {
            font-size: 2.4rem;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✊ Rock, Paper, Scissors")
st.caption("Welcome to the classic game!")

EMOJI = {"rock": "✊", "paper": "✋", "scissors": "✌️"}
choices = list(EMOJI.keys())

# -------------------------------
# SESSION STATE
# -------------------------------

if "wins" not in st.session_state:
    st.session_state.wins = 0
if "losses" not in st.session_state:
    st.session_state.losses = 0
if "ties" not in st.session_state:
    st.session_state.ties = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# -------------------------------
# PLAY
# -------------------------------

st.subheader("🎮 Make Your Move")

user_choice = st.selectbox(
    "Choose rock, paper, or scissors:",
    choices,
    format_func=lambda c: f"{EMOJI[c]} {c.capitalize()}",
)

if st.button("Play!", type="primary", use_container_width=True):
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        outcome = "tie"
        st.session_state.ties += 1
    elif (
        (user_choice == "rock" and computer_choice == "scissors")
        or (user_choice == "paper" and computer_choice == "rock")
        or (user_choice == "scissors" and computer_choice == "paper")
    ):
        outcome = "win"
        st.session_state.wins += 1
    else:
        outcome = "lose"
        st.session_state.losses += 1

    st.session_state.last_result = {
        "user_choice": user_choice,
        "computer_choice": computer_choice,
        "outcome": outcome,
    }
    st.rerun()

# -------------------------------
# LAST ROUND RESULT
# -------------------------------

if st.session_state.last_result:
    result = st.session_state.last_result

    with st.container(border=True):
        col1, col2 = st.columns(2)
        col1.markdown(f"<div class='choice-emoji'>{EMOJI[result['user_choice']]}</div>", unsafe_allow_html=True)
        col1.markdown(f"<p style='text-align:center;'>You chose <b>{result['user_choice'].capitalize()}</b></p>", unsafe_allow_html=True)

        col2.markdown(f"<div class='choice-emoji'>{EMOJI[result['computer_choice']]}</div>", unsafe_allow_html=True)
        col2.markdown(f"<p style='text-align:center;'>Computer chose <b>{result['computer_choice'].capitalize()}</b></p>", unsafe_allow_html=True)

        st.divider()

        if result["outcome"] == "tie":
            st.info("🤝 It's a tie!")
        elif result["outcome"] == "win":
            st.success(
                f"🎉 You win! {result['user_choice'].capitalize()} beats "
                f"{result['computer_choice'].capitalize()}"
            )
            st.balloons()
        else:
            st.error(
                f"💀 Computer wins! {result['computer_choice'].capitalize()} beats "
                f"{result['user_choice'].capitalize()}"
            )

st.divider()

# -------------------------------
# SCOREBOARD
# -------------------------------

st.subheader("📊 Scoreboard")

s1, s2, s3 = st.columns(3)
s1.metric("🧑 Wins", st.session_state.wins)
s2.metric("🤖 Losses", st.session_state.losses)
s3.metric("🤝 Ties", st.session_state.ties)

total_rounds = st.session_state.wins + st.session_state.losses + st.session_state.ties
if total_rounds > 0:
    win_rate = st.session_state.wins / total_rounds
    st.caption(f"Your win rate: {win_rate * 100:.0f}% over {total_rounds} round(s)")

if st.button("🔄 Reset Score", use_container_width=True):
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.ties = 0
    st.session_state.last_result = None
    st.success("Thanks for playing! Score reset. 👋")
    st.rerun()

st.divider()
st.caption("Rock, Paper, Scissors · Built with Streamlit")
