import streamlit as st
from scenarios.scenarios import (
    parse_fractional_odds,
    parse_place_term,
    evaluate_bet_scenarios
)
from config import DEFAULT_ODDS_FORMAT

# --- SETTINGS PANEL ---
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

# --- BET TYPE OPTIONS ---
bet_types = {
    "Single": 1,
    "Double": 2,
    "Treble": 3,
    "Yankee": 4,
    "Lucky 15": 4,
    "Canadian": 5,
    "Lucky 31": 5,
    "Heinz": 6,
    "Lucky 63": 6,
    "Super Heinz": 7,
    "Goliath": 8
}

if entry_mode == "Enter Manually":
    st.subheader("📋 Manual Bet Entry")

    bet_type = st.selectbox("Select Bet Type", list(bet_types.keys()))
    num_legs = bet_types[bet_type]

    each_way = st.checkbox("Each Way Bet?")
    if each_way:
        ew_terms = st.text_input("Place Terms (e.g. 1/5)", value="1/5")
    else:
        ew_terms = None

    stake_type = st.radio("Stake Type", ["Combined Stake", "Stake Per Bet"])
    total_stake = st.number_input("Enter Total Stake", min_value=0.0, step=0.5)

    st.markdown("### 🧾 Bet Details")
    bet_data = []

    for i in range(num_legs):
        st.markdown(f"**Leg {i+1}**")
        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:
            odds = st.text_input(f"Odds (Leg {i+1})", key=f"odds_{i}")

        with col2:
            if each_way:
                place_term = st.text_input(f"Place Term (Leg {i+1})", value=ew_terms, key=f"place_{i}")
            else:
                place_term = None

        with col3:
            result_options = ["Won", "Lost", "Void / NR", "Unknown"]
            if each_way:
                result_options.insert(1, "Placed")

            result = st.radio(
                f"Result (Leg {i+1})",
                result_options,
                horizontal=True,
                key=f"result_{i}"
            )

        # Color coding logic
        result_color = {
            "Won": "#d4edda",
            "Placed": "#fff3cd",
            "Lost": "#f8d7da",
            "Void / NR": "#e2e3e5",
            "Unknown": "#ffffff"
        }

        st.markdown(
            f"<div style='background-color:{result_color[result]}; padding:10px; border-radius:5px;'>"
            f"Leg {i+1} Summary: Odds = {odds}, Result = {result}"
            f"</div>",
            unsafe_allow_html=True
        )

        decimal_odds = parse_fractional_odds(odds)
        place_multiplier = parse_place_term(place_term) if each_way and place_term else 0.2

        potential_win = round(total_stake * decimal_odds, 2)
        potential_place = round(total_stake * (decimal_odds - 1) * place_multiplier + total_stake, 2) if each_way else 0

        bet_data.append({
            "result": result.lower().replace(" / nr", "").strip(),
            "potential_win": potential_win,
            "potential_place": potential_place
        })

    betslip = {"legs": bet_data}

    if st.button("Evaluate Scenarios"):
        results = evaluate_bet_scenarios(betslip, total_stake, each_way)

        st.subheader("📊 Scenario Results")
        st.write(f"**Current Return:** £{results['current_return']} (Profit/Loss: £{results['profit_loss_current']})")
        st.write(f"**Best Case Return:** £{results['best_case_return']} (Profit/Loss: £{results['profit_loss_best']})")
        if each_way:
            st.write(f"**Place Case Return:** £{results['place_case_return']} (Profit/Loss: £{results['profit_loss_place']})")
