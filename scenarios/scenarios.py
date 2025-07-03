def parse_fractional_odds(odds_str):
    try:
        num, denom = map(float, odds_str.strip().split("/"))
        return round(num / denom + 1, 2)
    except:
        return 1.0

def parse_place_term(term_str):
    try:
        num, denom = map(float, term_str.strip().split("/"))
        return round(num / denom, 2)
    except:
        return 0.2

def evaluate_bet_scenarios(betslip, stake, each_way=False):
    current_return = 0
    best_case_return = 0
    place_case_return = 0

    for leg in betslip.get("legs", []):
        result = leg.get("result", "unknown")
        potential_win = leg.get("potential_win", 0)
        potential_place = leg.get("potential_place", 0) if each_way else 0

        if result == "won":
            current_return += potential_win
        elif result == "placed" and each_way:
            current_return += potential_place
        elif result == "void":
            current_return += 0

        if result in ["won", "unknown"]:
            best_case_return += potential_win
        elif result == "placed" and each_way:
            best_case_return += potential_place

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

def get_best_case(betslip):
    return sum(leg.get("potential_win", 0) for leg in betslip.get("legs", []))

