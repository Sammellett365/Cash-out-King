from scenarios.scenarios import evaluate_bet_scenarios, get_best_case

def calculate_cashout_value(betslip, current_offer, stake, each_way=False):
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

