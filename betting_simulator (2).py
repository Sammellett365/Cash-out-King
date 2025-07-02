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

def calculate_number_of_bets(bet_type, n, each_way):
    def base_bets():
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
    bets = base_bets()
    return bets * 2 if each_way else bets

# --- Streamlit UI ---
st.title("💸 Cashout Outcome Simulator")

stake = st.number_input("Total Stake (£)", min_value=0.0, value=10.0)
cashout_offer = st.number_input("Current Cashout Offer (£)", min_value=0.0, value=20.0)

bet_type = st.selectbox("Select Bet Type", ["Single", "Double", "Treble", "Fourfold", "Trixie", "Yankee", "Lucky 15", "Super Heinz"])
each_way = st.checkbox("Each-Way Bet (Win + Place)", value=False)

if bet_type in ["Single", "Double", "Treble", "Fourfold"]:
    num_legs = st.number_input("Number of Selections", min_value=1, max_value=10, value={"Single": 1, "Double": 2, "Treble": 3, "Fourfold": 4}[bet_type])
else:
    num_legs = {
        "Trixie": 3,
        "Yankee": 4,
        "Lucky 15": 4,
        "Super Heinz": 7
    }[bet_type]

# --- Bet Summary ---
num_bets = calculate_number_of_bets(bet_type, num_legs, each_way)
unit_stake = math.floor((stake / num_bets) * 100) / 100 if num_bets > 0 else 0
actual_outlay = unit_stake * num_bets

st.subheader("🧾 Bet Summary")
st.markdown(f"""
- **Bet Type**: {bet_type}  
- **Number of Legs**: {num_legs}  
- **Each-Way**: {"Yes" if each_way else "No"}  
- **Number of Bets**: {num_bets}  
- **Unit Stake**: £{unit_stake:.2f}  
- **Actual Outlay**: £{actual_outlay:.2f}
""")

# --- Odds and Results Input ---
st.subheader(f"Enter Odds, Result, and Place Fraction for {num_legs} Selections")

default_data = pd.DataFrame({
    "Odds": ["" for _ in range(num_legs)],
    "Place Fraction": ["1/5"] * num_legs
})
edited_data = st.data_editor(default_data, num_rows="fixed", use_container_width=True)

results = []
result_options = ["Win", "Place", "Lost", "Void", "Unknown"]

st.markdown("### Select Result for Each Leg")
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

# Summary of all legs win/place
if all(r == "Win" for r in results):
    st.success("✅ All legs WIN!")
elif all(r in ["Win", "Place"] for r in results):
    st.info("✅ All legs PLACED or WON!")
else:
    st.warning("❌ Not all legs won or placed.")

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

# --- Simulation Logic ---
if all(leg["odds"] is not None for leg in legs):
    combinations = get_combinations(bet_type, len(legs))
    if not combinations:
        st.warning("Not enough selections for this bet type.")
    else:
        unknown_indices = [i for i, leg in enumerate(legs) if leg["result"] == "Unknown"]
        scenarios = list(itertools.product(["Win", "Place", "Lost", "Void"], repeat=len(unknown_indices))) if unknown_indices else [()]

        results_table = []
        known_win_return = 0.0

        for scenario in scenarios:
            simulated_legs = [leg.copy() for leg in legs]
            for idx, outcome in zip(unknown_indices, scenario):
                simulated_legs[idx]["result"] = outcome

            win_return = 0.0
            place_return = 0.0

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
                    win_return += unit_stake * odds_product
                if each_way and valid_place:
                    place_return += unit_stake * place_odds_product

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
        st.write(f"✅ Return from known results: £{known_win_return:.2f}")

        if unknown_indices:
            # Best case: all unknowns win
            best_win_legs = [leg.copy() for leg in legs]
            for idx in unknown_indices:
                best_win_legs[idx]["result"] = "Win"

            max_win_return = 0.0
            max_place_return = 0.0

            for combo in combinations:
                combo_legs = [best_win_legs[i] for i in combo]
                if any(leg["result"] == "Lost" for leg in combo_legs):
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
                    max_win_return += unit_stake * odds_product
                if each_way and valid_place:
                    max_place_return += unit_stake * place_odds_product

            st.write(f"🎯 If all unknowns WIN: £{max_win_return + (max_place_return if each_way else 0):.2f}")
            if each_way:
                st.write(f"🔶 If all unknowns PLACE: £{known_win_return + max_place_return:.2f}")
        else:
            st.success(f"🎉 All results known. Total return: £{known_win_return:.2f}")
