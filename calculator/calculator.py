from scenarios.scenarios import get_best_case

def evaluate_bet_scenarios(betslip, stake, each_way=False):
    """
    Evaluates current, best-case, and place-case returns for a given betslip.
    Treats 'unknown' results as 'lost' for current return.
    Assumes 'unknown' results as 'won' for best-case and 'placed' for place-case (if EW).
    """
    current_return = 0
    best_case_return = 0
    place_case_return = 0

    for leg in betslip.get("legs", []):
        result = leg.get("result", "unknown")
        potential_win = leg.get("potential_win", 0)
        potential_place = leg.get("potential_place", 0) if each_way else 0

        # Current return
        if result == "won":
            current_return += potential_win
        elif result == "placed" and each_way:
            current_return += potential_place
        elif result == "void":
            current_return += 0  # void returns nothing

        # Best-case return
        if result in ["won", "unknown"]:
            best_case_return += potential_win
        elif result == "placed" and each_way:
            best_case_return += potential_place

        # Place-case return
        if each_way:
            if result in ["placed", "unknown"]:
                place_case_return += potential_place
            elif result == "won":
                place_case_return += potential_win

    return {
        "current_return": round(current_return, 2),
        "best_case_return": round(best_case_return, 2),
        "place_case_return": round(place_case_return, 2) if each_way else None,
        "profit_loss_current": round(current_return - stake, 2),
        "profit_loss_best": round(best_case_return - stake, 2),
        "profit_loss_place": round(place_case_return - stake, 2) if each_way else None
    }

def calculate_cashout_value(betslip, current_offer, stake, each_way=False):
    """
    Combines cashout value analysis with full scenario evaluation.
    """
    best_case = get_best_case(betslip)
    value_ratio = current_offer / best_case if best_case else 0

    scenario_summary = evaluate_bet_scenarios(betslip, stake, each_way)

    return {
        "cashout_analysis": {
            "best_case": round(best_case, 2),
            "cashout_offer": round(current_offer, 2),
            "value_ratio": round(value_ratio, 2)
        },
        "scenario_summary": scenario_summary
    }
