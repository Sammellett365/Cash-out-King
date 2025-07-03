import streamlit as st
from config import DEFAULT_ODDS_FORMAT
from calculator.calculator import calculate_cashout_value

# --- SETTINGS PANEL (Top Right) ---
with st.container():
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        with st.expander("⚙️ Settings", expanded=False):
            odds_format = st.radio(
                "Select Odds Format",
                ["Fractional", "Decimal"],
                index=0 if DEFAULT_ODDS_FORMAT == "Fractional" else 1,
                key="odds_format"
            )

# --- MAIN APP TITLE ---
st.title("Betting Calculator")

# --- ENTRY MODE SELECTION ---
entry_mode = st.radio("Choose Entry Mode", ["Use OCR", "Enter Manually"])

# --- MANUAL ENTRY FORM ---
if entry_mode == "Enter Manually":
    bet_type = st.selectbox("Select Bet Type", ["Single", "Double", "Treble", "Yankee", "Lucky 15"])
    each_way = st.checkbox("Each Way Bet?")
    place_terms = None
    if each_way:
        place_terms = st.text_input("Place Terms (e.g. 1/5)", value="1/5")

    stake_type = st.radio("Stake Type", ["Combined Stake", "Stake Per Bet"])
    total_stake = st.number_input("Enter Total Stake", min_value=0.0, step=0.5)

    num_legs = {
        "Single": 1,
        "Double": 2,
        "Treble": 3,
        "Yankee": 4,
        "Lucky 15": 4
    }.get(bet_type, 1)

    st.markdown("### Enter Bet Details")
    bet_data = []
    for i in range(num_legs):
        st.markdown(f"**Leg {i+1}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            odds = st.text_input(f"Odds (e.g. 5/1 or 6.0)", key=f"odds_{i}")
        with col2:
            result_options = ["Won", "Lost", "Void / NR", "Unknown"]
            if each_way:
                result_options.insert(1, "Placed")
            result = st.selectbox("Result", result_options, key=f"result_{i}")
        with col3:
            potential_win = st.number_input("Potential Win", min_value=0.0, step=0.5, key=f"win_{i}")
            potential_place = 0.0
            if each_way:
                potential_place = st.number_input("Potential Place", min_value=0.0, step=0.5, key=f"place_{i}")

        leg = {
            "odds": odds,
            "result": result.lower().replace(" / ", "_").replace(" ", "_"),
            "potential_win": potential_win,
            "potential_place": potential_place
        }
        bet_data.append(leg)

    # --- CALCULATE RETURNS ---
    st.markdown("---")
    current_offer = st.number_input("Enter Current Cashout Offer", min_value=0.0, step=0.5)

    if st.button("Calculate Returns"):
        result = calculate_cashout_value(
            {"legs": bet_data},
            current_offer=current_offer,
            stake=total_stake,
            each_way=each_way
        )
        st.subheader("📊 Scenario Summary")
        st.write(result["scenario_summary"])
        st.subheader("💰 Cashout Analysis")
        st.write(result["cashout_analysis"])




