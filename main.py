import streamlit as st

# Odds format selector at the top
odds_format = st.selectbox("Select Odds Format", ["Fractional", "Decimal"])

# Entry mode selection
entry_mode = st.radio("Choose Entry Mode", ["Use OCR", "Enter Manually"])

if entry_mode == "Enter Manually":
    # Bet type selection
    bet_type = st.selectbox("Select Bet Type", ["Singles", "Doubles", "Trebles", "Lucky 15", "Yankee", "Canadian", "Heinz", "Super Heinz", "Goliath"])

    # Each Way option
    each_way = st.checkbox("Each Way Bet")

    # Stake type and input
    stake_type = st.selectbox("Stake Type", ["Combined Stake", "Stake Per Bet"])
    total_stake = st.number_input("Enter Total Stake", min_value=0.0, step=0.01)

    # Determine number of legs based on bet type
    bet_legs = {
        "Singles": 1,
        "Doubles": 2,
        "Trebles": 3,
        "Lucky 15": 4,
        "Yankee": 4,
        "Canadian": 5,
        "Heinz": 6,
        "Super Heinz": 7,
        "Goliath": 8
    }
    num_legs = bet_legs.get(bet_type, 1)

    st.subheader("Enter Bet Details")

    # Default place terms
    if each_way:
        place_terms = st.text_input("Place Terms (e.g., 1/5)", value="1/5")

    # Create dynamic table for bet legs
    for i in range(num_legs):
        st.markdown(f"### Leg {i+1}")
        odds = st.text_input(f"Odds for Leg {i+1} ({odds_format})", key=f"odds_{i}")
        if each_way:
            st.text(f"Place Terms: {place_terms}")
        result = st.radio(
            f"Result for Leg {i+1}",
            ["Won", "Placed", "Lost", "Void / NR", "Unknown"] if each_way else ["Won", "Lost", "Void / NR", "Unknown"],
            key=f"result_{i}"
        )

        # Color coding based on result
        result_colors = {
            "Won": "#d4edda",
            "Placed": "#fff3cd" if each_way else None,
            "Lost": "#f8d7da",
            "Void / NR": "#e2e3e5",
            "Unknown": "#ffffff"
        }
        color = result_colors.get(result, "#ffffff")
        st.markdown(
            f"<div style='background-color:{color};padding:10px;'>Leg {i+1} Result: {result}</div>",
            unsafe_allow_html=True
        )

# Clarification about result summaries
st.info("🔍 Result summaries and calculations are handled in a separate module (e.g., calculator.py or scenarios.py). This interface is for data entry only.")



