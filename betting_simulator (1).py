import streamlit as st
import itertools
from fractions import Fraction
import pandas as pd
import math

# --- Helper Functions ---
def fractional_to_decimal(odds_str):
    try:
        if odds_str.lower() == "evens":
            return 2.0
        return float(Fraction(odds_str)) + 1
    except:
        return None

def get_combinations(bet_type, n):
    if bet_type == "Single":
        return list(itertools.combinations(range(n), 1))
    elif bet_type == "Double":
        return list(itertools.combinations(range(n), 2))
    elif bet_type == "Treble":
        return list(itertools.combinations(range(n), 3))
    elif bet_type == "Fourfold":
        return list(itertools.combinations(range(n), 4))
    elif bet_type == "Trixie" and n >= 3:
        return list(itertools.combinations(range(n), 2)) + list(itertools.combinations(range(n), 3))
    elif bet_type == "Yankee" and n >= 4:
        return list(itertools.combinations(range(n), 2)) + list(itertools.combinations(range(n), 3)) + list(itertools.combinations(range(n), 4))
    elif bet_type == "Lucky 15" and n >= 4:
        return list(itertools.combinations(range(n), 1)) + list(itertools.combinations(range(n), 2)) + list(itertools.combinations(range(n), 3)) + list(itertools.combinations(range(n), 4))
    elif bet_type == "Super Heinz" and n == 7:
        return [c for r in range(2, 8) for c in itertools.combinations(range(n), r)]
    else:
        return []

def calculate_number_of_bets(bet_type, n):
    if bet_type == "Single":
        return n
    elif bet_type == "Double":
        return math.comb(n, 2)
    elif bet_type == "Treble":
        return math.comb(n, 3)
    elif bet_type == "Fourfold":
        return math.comb(n, 4)
    elif bet_type == "Trixie" and n >= 3:
        return math.comb(n, 2) + math.comb(n, 3)
    elif bet_type == "Yankee" and n >= 4:
        return math.comb(n, 2) + math.comb(n, 3) + math.comb(n, 4)
    elif bet_type == "Lucky 15" and n >= 4:
        return math.comb(n, 1) + math.comb(n, 2) + math.comb(n, 3) + math.comb(n, 4)
    elif bet_type == "Super Heinz" and n == 7:
        return sum(math.comb(n, r) for r in range(2, 8))
    else:
        return 0

# --- Streamlit UI ---
st.title("💸 Multi-Bet Cashout Simulator")

num_legs = st.number_input("Number of Selections", min_value=1, max_value=10, value=8)

# --- Odds and Place Fraction Input ---
st.subheader(f"Enter Odds and Place Fraction for {num_legs} Selections")

default_data = pd.DataFrame({
    "Odds": ["" for _ in range(num_legs)],
    "Place Fraction": ["1/5"] * num_legs
})
edited_data = st.data_editor(default_data, num_rows="fixed", use_container_width=True)

# --- Result Selection ---
st.subheader("Select Result for Each Leg")
results = []
result_options = ["Win", "Place", "Lost", "Void", "Unknown"]

for i in range(num_legs):
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(f"**Leg {i+1} ({edited_data['Odds'][i]})**")
    with col2:
        result = st.radio(
            label="",
            options=result_options,
            index=result_options.index("Unknown"),
            key=f"result_{i}",
            horizontal=True
        )
        results.append(result)

# --- Bet Types and Stakes ---
st.subheader("Select Bet Types and Stakes")
available_bet_types = ["Double", "Treble", "Fourfold"]
selected_bets = {}
for bet_type in available_bet_types:
    col1, col2 = st.columns([2, 1])
    with col1:
        selected = st.checkbox(f"Include {bet_type}", key=f"include_{bet_type}")
    with col2:
        if selected:
            stake = st.number_input(f"Stake for {bet_type} (£)", min_value=0.0, value=0.1, key=f"stake_{bet_type}")
            selected_bets[bet_type] = stake

each_way = st.checkbox("Each-Way Bet (Win + Place)", value=False)
cashout_offer = st.number_input("Current Cashout Offer (£)", min_value=0.0, value=20.0)

# --- Parse Legs ---
legs = []
for i, row in edited_data.iterrows():
    odds_str = row["Odds"]
    result = results[i]
    place_frac = row["Place Fraction"]
    odds = fractional_to_decimal(odds_str) if odds_str else None
    place_multiplier = float(Fraction(place_frac)) if each_way else 0.0
    legs.append({
        "odds": odds,
        "result": result,
        "display": odds_str,
        "place_multiplier": place_multiplier
    })

# --- Simulation ---
if all(leg["odds"] is not None for leg in legs) and selected_bets:
    unknown_indices = [i for i, leg in enumerate(legs) if leg["result"] == "Unknown"]
    scenarios = list(itertools.product(["Win", "Place", "Lost", "Void"], repeat=len(unknown_indices))) if unknown_indices else [()]

    results_table = []
    known_win_return = 0.0

    for scenario in scenarios:
        simulated_legs = [leg.copy() for leg in legs]
        for idx, outcome in zip(unknown_indices, scenario):
            simulated_legs[idx]["result"] = outcome

        total_return = 0.0
        win_return = 0.0
        place_return = 0.0

        for bet_type, stake in selected_bets.items():
            combinations = get_combinations(bet_type, len(simulated_legs))
            for combo in combinations:
                combo_legs = [simulated_legs[i] for i in combo]
                if any(leg["result"] in ["Lost", "Unknown"] for leg in combo_legs):
                    continue

                odds_product = 1
                place_odds_product = 1
                valid_win = True
                valid_place = True

                for leg in combo_legs:
                    if leg["result"] == "Void":
                        continue
                    if leg["result"] not in ["Win", "Void"]:
                        valid_win = False
                    if leg["result"] not in ["Win", "Place", "Void"]:
                        valid_place = False
                    odds_product *= leg["odds"]
                    place_odds_product *= (1 + (leg["odds"] - 1) * leg["place_multiplier"])

                if valid_win:
                    win_return += stake * odds_product
                if each_way and valid_place:
                    place_return += stake * place_odds_product

        total_return = win_return + (place_return if each_way else 0)
        if not scenario:
            known_win_return = total_return
        outcome_str = ", ".join([f"Leg {unknown_indices[i]+1} ({legs[unknown_indices[i]]['display']}): {scenario[i]}" for i in range(len(scenario))]) if scenario else "All results known"
        results_table.append({
            "Scenario": outcome_str,
            "Win Return (£)": round(win_return, 2),
            "Place Return (£)": round(place_return, 2) if each_way else 0.0,
            "Total Return (£)": round(total_return, 2),
            "Beats Cashout": total_return > cashout_offer
        })

    st.subheader("📊 Results Summary")
    st.write(f"Return from known results: £{known_win_return:.2f}")

    if unknown_indices:
        best_win_return = 0.0
        best_place_return = 0.0
        best_win_legs = [leg.copy() for leg in legs]
        best_place_legs = [leg.copy() for leg in legs]

        for idx in unknown_indices:
            best_win_legs[idx]["result"] = "Win"
            best_place_legs[idx]["result"] = "Place"

        for bet_type, stake in selected_bets.items():
            combos = get_combinations(bet_type, len(legs))

            for combo in combos:
                combo_win_legs = [best_win_legs[i] for i in combo]
                combo_place_legs = [best_place_legs[i] for i in combo]

                odds_product = 1
                place_odds_product = 1
                valid_win = True
                valid_place = True

                for leg in combo_win_legs:
                    if leg["result"] == "Void":
                        continue
                    if leg["result"] not in ["Win", "Void"]:
                        valid_win = False
                    odds_product *= leg["odds"]

                for leg in combo_place_legs:
                    if leg["result"] == "Void":
                        continue
                    if leg["result"] not in ["Win", "Place", "Void"]:
                        valid_place = False
                    place_odds_product *= (1 + (leg["odds"] - 1) * leg["place_multiplier"])

                if valid_win:
                    best_win_return += stake * odds_product
                if each_way and valid_place:
                    best_place_return += stake * place_odds_product

        st.info(f"🎯 If all unknowns WIN: £{best_win_return:.2f}")
        if each_way:
            st.info(f"🔶 If all unknowns PLACE: £{best_place_return:.2f}")
    else:
        st.success(f"🎉 All results known. Total return: £{known_win_return:.2f}")

    st.subheader("🔍 Simulation Results")
    df_results = pd.DataFrame(results_table)
    st.dataframe(df_results.sort_values(by="Total Return (£)", ascending=False), use_container_width=True)

    num_beating = sum(df_results["Beats Cashout"])
    st.success(f"{num_beating} out of {len(scenarios)} scenarios beat the cashout offer (£{cashout_offer:.2f}).")
