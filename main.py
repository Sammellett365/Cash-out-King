import streamlit as st
from scenarios.scenarios import parse_fractional_odds, parse_place_term, evaluate_bet_scenarios

st.title("🎯 Betting Scenario Calculator")

st.subheader("Enter Bet Details")

num_legs = st.number_input("Number of Legs", min_value=1, max_value=10, value=3)
each_way = st.checkbox("Each Way Bet?")
stake = st.number_input("Total Stake (£)", min_value=0.0, step=0.5)

bet_data = []
for i in range(num_legs):
    st.markdown(f"**Leg {i+1}**")
    col1, col2, col3 = st.columns(3)

    with col1:
        odds_str = st.text_input(f"Odds (e.g. 5/2)", key=f"odds_{i}")
    with col2:
        place_term_str = st.text_input(f"Place Term (e.g. 1/5)", value="1/5", key=f"place_{i}") if each_way else None
    with col3:
        result = st.selectbox("Result", ["Won", "Placed", "Lost", "Void", "Unknown"], key=f"result_{i}")

    decimal_odds = parse_fractional_odds(odds_str)
    place_multiplier = parse_place_term(place_term_str) if each_way else 0

    potential_win = round(stake * decimal_odds, 2)
    potential_place = round(stake * (decimal_odds - 1) * place_multiplier + stake, 2) if each_way else 0

    bet_data.append({
        "result": result.lower(),
        "potential_win": potential_win,
        "potential_place": potential_place
    })

betslip = {"legs": bet_data}

if st.button("Evaluate Scenarios"):
    results = evaluate_bet_scenarios(betslip, stake, each_way)

    st.subheader("📊 Scenario Results")
    st.write(f"**Current Return:** £{results['current_return']} (Profit/Loss: £{results['profit_loss_current']})")
    st.write(f"**Best Case Return:** £{results['best_case_return']} (Profit/Loss: £{results['profit_loss_best']})")
    if each_way:
        st.write(f"**Place Case Return:** £{results['place_case_return']} (Profit/Loss: £{results['profit_loss_place']})")

