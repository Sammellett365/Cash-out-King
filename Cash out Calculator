from scenarios.scenarios import get_best_case

def calculate_cashout_value(betslip, current_offer):
    best_case = get_best_case(betslip)
    # Placeholder logic for cashout analysis
    value_ratio = current_offer / best_case if best_case else 0
    return {
        "best_case": best_case,
        "cashout_offer": current_offer,
        "value_ratio": round(value_ratio, 2)
    }

