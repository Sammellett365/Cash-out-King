import streamlit as st

# --- Helper Functions ---
def get_bet_types():
    return ["Singles", "Doubles", "Trebles", "Yankee", "Lucky 15", "Patent", "Trixie", "Canadian", "Heinz", "Super Heinz", "Goliath"]

def get_leg_count(bet_type):
    return {
        "Singles": 1,
        "Doubles": 2,
        "Trebles": 3,
        "Yankee": 4,
        "Lucky 15": 4,
        "Patent": 3,
        "Trixie": 3,
        "Canadian": 5,
        "Heinz": 6,
        "Super Heinz": 7,
        "Goliath": 8
    }.get(bet_type, 1)

def get_result_options(each_way):
    options = ["Won", "Lost", "Void / NR", "Unknown"]
    if each_way:
        options.insert(1, "Placed")
    return options

def get_result_color(result):
    return {
        "Won": "#d4edda",
        "Placed": "#fff3cd",
        "Lost": "#f8d7da",
        "Void / NR": "#e2e3e5",
        "Unknown": "#ffffff"
    }.get(result, "#ffffff")

# --- Streamlit App ---
st.title("Betting Calculator")

entry_mode = st.radio("Choose Entry Mode:", ["Use OCR", "Enter Manually"])

if entry_mode == "Enter Manually":
    st.subheader("Manual Bet Entry")

    bet_type = st.selectbox("Select Bet Type:", get_bet_types())
    each_way = st.checkbox("Each Way Bet?")
    stake_type = st.radio("Stake Type:", ["Combined Stake", "Stake Per Bet"])
    total_stake = st.number_input("Enter Total Stake:", min_value=0.0, step=0.01)

    num_legs = get_leg_count(bet_type)
    st.markdown(f"### Enter Details for {num_legs} Legs")

    for i in range(num_legs):
        st.markdown(f"#### Leg {i+1}")
        cols = st.columns([2, 2, 2, 2])
        with cols[0]:
            odds_format = st.radio(f"Odds Format (Leg {i+1})", ["Fractional", "Decimal"], key=f"odds_format_{i}")
            odds = st.text_input(f"Odds (Leg {i+1})", key=f"odds_{i}")
        with cols[1]:
            if each_way:
                place_terms = st.text_input(f"Place Terms (Leg {i+1})", key=f"place_{i}")
            else:
                st.markdown("Place Terms: N/A")
        with cols[2]:
            result = st.selectbox(f"Result (Leg {i+1})", get_result_options(each_way), key=f"result_{i}")
        with cols[3]:
            color = get_result_color(result)
            st.markdown(f"<div style='background-color:{color};padding:10px;border-radius:5px;'>Result: {result}</div>", unsafe_allow_html=True)

st.markdown("---")
st.info("This is a dynamic form. Based on your selections, the fields above will adapt accordingly.")

