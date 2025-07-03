def get_best_case(betslip):
    # Placeholder logic to calculate best case scenario
    total_win = 0
    for leg in betslip.get("legs", []):
        if leg.get("status") != "lost":
            total_win += leg.get("potential_win", 0)
    return total_win
