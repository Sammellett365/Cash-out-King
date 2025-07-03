def evaluate_bet_scenarios(betslip, stake, each_way=False):
    """
    Evaluates a betslip for:
    1. Current return based on actual results (treat 'unknown' as 'lost')
    2. Best case: all unknowns win
    3. Place case: all unknowns place (if each_way)
    4. Profit/loss comparison
    """

    def calculate_leg_return(leg, result_override=None):
        """
        Calculates return for a single leg based on result and odds.
        If result_override is provided, it overrides the leg's actual result.
        """
        result = result_override if result_override else leg.get("result", "lost")
        odds = leg.get("odds", 0)
        place_terms = leg.get("place_terms", 0.2) if each_way else 0

        if result == "won":
            return stake * odds
        elif result == "placed" and each_way:
            return stake * (odds * place_terms)
        elif result == "void":
            return stake  # stake returned
        else:
            return 0

    current_return = 0
    best_case_return = 0
    place_case_return = 0

    for leg in betslip.get("legs", []):
        result = leg.get("result", "lost")
        if result == "unknown":
            # Treat as lost for current return
            current_return += 0
            # Best case: assume win
            best_case_return += calculate_leg_return(leg, result_override="won")
            # Place case: assume place if each_way
            if each_way:
                place_case_return += calculate_leg_return(leg, result_override="placed")
        else:
            current_return += calculate_leg_return(leg)

    profit_loss_current = current_return - stake
    profit_loss_best = best_case_return + current_return - stake
    profit_loss_place = place_case_return + current_return - stake if each_way else None

    return {
        "current_return": round(current_return, 2),
        "best_case_return": round(best_case_return + current_return, 2),
        "place_case_return": round(place_case_return + current_return, 2) if each_way else None,
        "profit_loss_current": round(profit_loss_current, 2),
        "profit_loss_best": round(profit_loss_best, 2),
        "profit_loss_place": round(profit_loss_place, 2) if each_way else None
    }

