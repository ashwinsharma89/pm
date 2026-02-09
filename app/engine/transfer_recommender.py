"""
Transfer Recommendation Engine
===============================
Generates buy and sell recommendations with full justification
based on squad analysis, financial modeling, and scouting data.

Decision Framework:
1. Identify needs from squad analysis (deficiency detection)
2. Match targets to needs (position, profile, budget fit)
3. Score each recommendation (impact, feasibility, value)
4. Generate detailed rationale with stats, eye-test, and strategic reasoning
"""

from app.data.squad_db import Player, SELL_CANDIDATES, PROJECTED_SALE_REVENUE


# Priority weights for recommendation scoring
WEIGHTS = {
    "squad_need": 0.25,      # How much does the squad need this position?
    "player_quality": 0.20,  # How good is the player (stats + eye test)?
    "financial_value": 0.20, # Value for money (fee vs quality)
    "age_profile": 0.15,    # Age-appropriate for squad sustainability
    "feasibility": 0.20,    # Can we actually do this deal?
}


def generate_sell_recommendations(squad: list[Player], squad_report: dict) -> list[dict]:
    """Generate recommendations for players to sell, with full justification."""
    recommendations = []

    for player in squad:
        if player.name not in SELL_CANDIDATES and player.contract_expiry[:4] != "2026":
            continue

        rec = _build_sell_recommendation(player, squad, squad_report)
        if rec:
            recommendations.append(rec)

    # Sort by priority (highest revenue first, then most urgent)
    recommendations.sort(key=lambda x: x["priority_score"], reverse=True)
    return recommendations


def _build_sell_recommendation(player: Player, squad: list[Player],
                                squad_report: dict) -> dict:
    """Build a detailed sell recommendation for a single player."""
    projected_fee = PROJECTED_SALE_REVENUE.get(player.name, 0.0)
    is_expiring = player.contract_expiry[:4] == "2026"

    # Calculate priority score
    urgency = 0
    if is_expiring:
        urgency = 95  # Must decide now
    elif player.contract_expiry[:4] == "2027":
        urgency = 80  # Last chance for fee
    else:
        urgency = 50

    replaceability = _assess_replaceability(player, squad)
    financial_benefit = min(100, projected_fee * 2 + (player.wage_weekly_k / 3))
    performance_justification = _assess_performance_case(player)

    priority_score = int(
        urgency * 0.30 +
        replaceability * 0.25 +
        financial_benefit * 0.25 +
        performance_justification * 0.20
    )

    # Build rationale
    reasons = []
    if is_expiring:
        reasons.append(f"Contract expires June 2026. Will leave for FREE if not sold/renewed.")
    elif player.contract_expiry[:4] == "2027":
        reasons.append(f"Contract expires 2027. This summer is the last chance to get a transfer fee.")

    if player.stats.squawka_score < 60 and player.stats.minutes > 400:
        reasons.append(f"Below squad quality threshold: Squawka score {player.stats.squawka_score}/100.")
    if player.wage_weekly_k > 100 and player.role_in_squad in ("backup", "rotation"):
        reasons.append(f"High wages ({player.wage_weekly_k}k/wk) for a {player.role_in_squad} player.")
    if player.status == "loaned_out":
        reasons.append(f"Currently on loan at {player.loan_club}. Not in Arteta's plans.")
    if player.role_in_squad == "backup" and player.age > 27:
        reasons.append(f"Aging backup (age {player.age}) with limited contribution.")

    # Add performance-specific reasons
    for weakness in player.weaknesses:
        reasons.append(f"Weakness: {weakness}")

    return {
        "player": player.name,
        "position": player.position,
        "age": player.age,
        "current_role": player.role_in_squad,
        "contract_expiry": player.contract_expiry,
        "projected_fee_m": projected_fee,
        "wage_saving_weekly_k": player.wage_weekly_k,
        "wage_saving_annual_m": round(player.wage_weekly_k * 52 / 1000, 1),
        "priority_score": priority_score,
        "urgency": "immediate" if urgency >= 80 else "summer" if urgency >= 50 else "optional",
        "reasons": reasons,
        "eye_test": player.eye_test_notes,
        "recommendation_summary": _build_sell_summary(player, projected_fee, is_expiring),
    }


def _assess_replaceability(player: Player, squad: list[Player]) -> int:
    """How easily can this player be replaced? Higher = more replaceable."""
    same_pos = [p for p in squad if p.position == player.position
                and p.status == "available" and p.name != player.name]
    if len(same_pos) >= 2:
        return 80
    elif len(same_pos) >= 1:
        return 60
    return 30


def _assess_performance_case(player: Player) -> int:
    """How strong is the performance case for selling? Higher = stronger case to sell."""
    score = 50
    if player.stats.squawka_score < 55:
        score += 20
    if player.stats.minutes < 800 and player.role_in_squad != "youth":
        score += 15  # Barely playing
    if player.age > 29:
        score += 10
    if player.status == "loaned_out":
        score += 20
    return min(100, score)


def _build_sell_summary(player: Player, fee: float, is_expiring: bool) -> str:
    """Build a human-readable sell recommendation summary."""
    if is_expiring:
        return (f"SELL/LET GO: {player.name}'s contract expires this summer. "
                f"No realistic chance of renewal given squad competition. "
                f"Will depart as a free agent. Wage savings: {player.wage_weekly_k}k/week.")
    if fee > 0:
        return (f"SELL: {player.name} should be sold for an estimated EUR {fee}m. "
                f"Combined with {player.wage_weekly_k}k/week wage savings, "
                f"this frees significant resources for upgrades.")
    return f"RELEASE: {player.name} should be allowed to leave."


def generate_buy_recommendations(targets: list[Player], squad: list[Player],
                                  squad_report: dict, budget_m: float) -> list[dict]:
    """Generate buy recommendations ranked by priority and fit."""
    recommendations = []

    for target in targets:
        rec = _build_buy_recommendation(target, squad, squad_report, budget_m)
        if rec:
            recommendations.append(rec)

    recommendations.sort(key=lambda x: x["priority_score"], reverse=True)
    return recommendations


def _build_buy_recommendation(target: Player, squad: list[Player],
                               squad_report: dict, budget_m: float) -> dict:
    """Build a detailed buy recommendation for a transfer target."""

    # Squad need assessment
    pos_depth = next((d for d in squad_report["depth_analysis"]
                      if d["position"] == target.position), None)
    need_score = 50
    if pos_depth:
        if pos_depth["status"] == "critical":
            need_score = 95
        elif pos_depth["status"] == "thin":
            need_score = 80
        elif pos_depth["status"] == "adequate":
            need_score = 50
        else:
            need_score = 30

    # Check if this position is being vacated by a sale
    vacated_positions = _get_vacated_positions()
    if target.position in vacated_positions:
        need_score = min(100, need_score + 20)

    # Player quality score
    quality_score = min(100, int(target.stats.squawka_score * 1.2))

    # Financial value (lower fee = better value)
    if target.market_value_m == 0:
        value_score = 100  # Free transfer
    else:
        value_score = max(10, min(100, int(100 - (target.market_value_m / budget_m) * 80)))

    # Age profile score
    if target.age <= 23:
        age_score = 90
    elif target.age <= 27:
        age_score = 80
    elif target.age <= 30:
        age_score = 60
    else:
        age_score = 40

    # Feasibility score
    feasibility_score = _assess_deal_feasibility(target, budget_m)

    # Weighted priority score
    priority_score = int(
        need_score * WEIGHTS["squad_need"] +
        quality_score * WEIGHTS["player_quality"] +
        value_score * WEIGHTS["financial_value"] +
        age_score * WEIGHTS["age_profile"] +
        feasibility_score * WEIGHTS["feasibility"]
    )

    # Determine who this player would replace/compete with
    competing_with = [p.name for p in squad
                      if p.position == target.position and p.status == "available"]

    # Build the detailed why
    reasons = _build_buy_reasons(target, squad, pos_depth, need_score)

    return {
        "player": target.name,
        "position": target.position,
        "age": target.age,
        "nationality": target.nationality,
        "estimated_fee_m": target.market_value_m,
        "estimated_wages_k": target.wage_weekly_k,
        "current_club": _infer_club(target),
        "contract_expiry": target.contract_expiry,
        "priority_score": priority_score,
        "score_breakdown": {
            "squad_need": need_score,
            "player_quality": quality_score,
            "financial_value": value_score,
            "age_profile": age_score,
            "feasibility": feasibility_score,
        },
        "competing_with": competing_with,
        "reasons": reasons,
        "eye_test": target.eye_test_notes,
        "stats_summary": _build_stats_summary(target),
        "deal_structure": _suggest_deal_structure(target, budget_m),
        "risk_factors": target.weaknesses,
        "why_works": target.why_works,
        "why_wont_work": target.why_wont_work,
        "recommendation_summary": _build_buy_summary(target, priority_score),
    }


def _get_vacated_positions() -> set:
    """Positions being vacated by sell candidates."""
    position_map = {
        "Gabriel Martinelli": "LW",
        "Ben White": "RB",
        "Gabriel Jesus": "ST",
        "Leandro Trossard": "LW",
        "Jakub Kiwior": "CB",
        "Reiss Nelson": "RW",
        "Fabio Vieira": "AM",
    }
    return set(position_map.values())


def _assess_deal_feasibility(target: Player, budget_m: float) -> int:
    """Assess how feasible the deal is (0-100)."""
    score = 70  # Base feasibility

    # Free transfer = very feasible
    if target.market_value_m == 0:
        return 95

    # Budget check
    if target.market_value_m > budget_m * 0.6:
        score -= 20  # Takes up most of budget
    if target.market_value_m > budget_m:
        score -= 30  # Over budget

    # Competition from rivals
    risk_keywords = ["City", "Liverpool", "Real Madrid", "already signed"]
    for weakness in target.weaknesses:
        if any(kw.lower() in weakness.lower() for kw in risk_keywords):
            score -= 15

    # Willing to join
    for strength in target.strengths:
        if "wants" in strength.lower() or "arsenal" in strength.lower():
            score += 10

    return max(10, min(100, score))


def _build_buy_reasons(target: Player, squad: list[Player],
                        pos_depth: dict, need_score: int) -> list[str]:
    """Build detailed reasons for why Arsenal should sign this player."""
    reasons = []

    if need_score >= 80:
        reasons.append(f"HIGH NEED: {target.position} is a priority position for reinforcement.")
    elif need_score >= 50:
        reasons.append(f"MODERATE NEED: {target.position} depth could be improved.")

    if target.market_value_m == 0:
        reasons.append("FREE TRANSFER: Available on a free - exceptional value.")
    elif target.market_value_m < 30:
        reasons.append(f"GOOD VALUE: Estimated fee of EUR {target.market_value_m}m is reasonable.")

    for strength in target.strengths:
        reasons.append(f"Strength: {strength}")

    if target.age <= 24:
        reasons.append(f"YOUTH INVESTMENT: At {target.age}, significant development potential and resale value.")

    if target.stats.squawka_score >= 70:
        reasons.append(f"HIGH PERFORMANCE: Squawka score of {target.stats.squawka_score} indicates elite level.")

    return reasons


def _build_stats_summary(target: Player) -> dict:
    """Build a stats summary card for the target."""
    per90 = target.stats.minutes / 90.0 if target.stats.minutes > 0 else 1
    return {
        "appearances": target.stats.appearances,
        "goals": target.stats.goals,
        "assists": target.stats.assists,
        "minutes": target.stats.minutes,
        "goals_per90": round(target.stats.goals / per90, 2) if per90 > 0 else 0,
        "assists_per90": round(target.stats.assists / per90, 2) if per90 > 0 else 0,
        "xg": target.stats.xg,
        "xa": target.stats.xa,
        "progressive_passes": target.stats.progressive_passes,
        "progressive_carries": target.stats.progressive_carries,
        "key_passes": target.stats.key_passes,
        "squawka_score": target.stats.squawka_score,
        "fotmob_rating": target.stats.fotmob_rating,
    }


def _suggest_deal_structure(target: Player, budget_m: float) -> dict:
    """Suggest an optimal deal structure."""
    fee = target.market_value_m

    if fee == 0:
        return {
            "type": "Free Transfer",
            "upfront": 0,
            "installments": 0,
            "add_ons": 0,
            "signing_bonus_est_m": round(fee * 0.1 + 5, 1),
            "total": 5.0,
            "notes": "Free agent. Budget only for signing bonus and agent fees."
        }

    # Suggest structured deal
    upfront_pct = 0.5 if fee < 50 else 0.4 if fee < 80 else 0.35
    addon_pct = 0.15

    upfront = round(fee * upfront_pct, 1)
    addons = round(fee * addon_pct, 1)
    installments = round(fee - upfront - addons, 1)

    return {
        "type": "Permanent Transfer",
        "upfront": upfront,
        "installments": installments,
        "installment_years": 3 if fee > 50 else 2,
        "add_ons": addons,
        "total": fee,
        "notes": f"Structured as EUR {upfront}m upfront + EUR {installments}m in installments "
                 f"+ EUR {addons}m in performance add-ons."
    }


def _infer_club(target: Player) -> str:
    """Infer the current club from eye test notes."""
    club_map = {
        "Tino Livramento": "Newcastle United",
        "Ayyoub Bouaddi": "LOSC Lille",
        "Arda Guler": "Real Madrid",
        "Julian Alvarez": "Atletico Madrid",
        "Davide Bartesaghi": "AC Milan",
        "Konstantinos Koulierakis": "VfL Wolfsburg",
        "Giorgio Scalvini": "Atalanta BC",
        "Karim Adeyemi": "Borussia Dortmund",
        "Castello Lukeba": "RB Leipzig",
        "Lutsharel Geertruida": "RB Leipzig",
        "Vanderson": "AS Monaco",
        "Milos Kerkez": "AFC Bournemouth",
        "Alejandro Balde": "FC Barcelona",
        "Adam Wharton": "Crystal Palace",
        "Ederson": "Atalanta BC",
        "Desire Doue": "Paris Saint-Germain",
        "Takefusa Kubo": "Real Sociedad",
        "Benjamin Sesko": "RB Leipzig",
        "Jonathan David": "LOSC Lille",
        "Nico Williams": "Athletic Bilbao",
        "Johan Bakayoko": "PSV Eindhoven",
    }
    return club_map.get(target.name, "Unknown")


def _build_buy_summary(target: Player, score: int) -> str:
    """Build a human-readable buy recommendation summary."""
    tier = "PRIORITY 1" if score >= 75 else "PRIORITY 2" if score >= 60 else "PRIORITY 3"
    return (f"{tier}: Sign {target.name} ({target.position}, {target.age}). "
            f"Estimated fee: EUR {target.market_value_m}m. "
            f"Recommendation score: {score}/100.")


def generate_transfer_plan(squad: list[Player], targets: list[Player],
                            squad_report: dict, budget_m: float) -> dict:
    """Generate the complete transfer plan combining buy and sell recommendations."""
    sells = generate_sell_recommendations(squad, squad_report)
    buys = generate_buy_recommendations(targets, squad, squad_report, budget_m)

    # Calculate financial summary
    total_sale_revenue = sum(s["projected_fee_m"] for s in sells)
    total_wage_savings = sum(s["wage_saving_annual_m"] for s in sells)
    total_purchase_cost = sum(b["estimated_fee_m"] for b in buys[:5])  # Top 5 targets
    total_new_wages = sum(b["estimated_wages_k"] * 52 / 1000 for b in buys[:5])

    net_spend = total_purchase_cost - total_sale_revenue
    net_wage_change = total_new_wages - total_wage_savings

    return {
        "sell_recommendations": sells,
        "buy_recommendations": buys,
        "financial_summary": {
            "transfer_budget_m": budget_m,
            "projected_sale_revenue_m": round(total_sale_revenue, 1),
            "total_available_m": round(budget_m + total_sale_revenue, 1),
            "projected_purchase_cost_m": round(total_purchase_cost, 1),
            "net_spend_m": round(net_spend, 1),
            "wage_savings_annual_m": round(total_wage_savings, 1),
            "new_wages_annual_m": round(total_new_wages, 1),
            "net_wage_change_annual_m": round(net_wage_change, 1),
        },
        "squad_report": squad_report,
        "transfer_window_strategy": _build_strategy_summary(sells, buys, budget_m),
    }


def _build_strategy_summary(sells: list, buys: list, budget_m: float) -> dict:
    """Build the overall transfer window strategy summary."""
    priority_buys = [b for b in buys if b["priority_score"] >= 70]
    secondary_buys = [b for b in buys if 55 <= b["priority_score"] < 70]
    opportunistic = [b for b in buys if b["priority_score"] < 55]

    return {
        "phase_1_early_summer": {
            "description": "Secure priority targets before World Cup distraction",
            "targets": [b["player"] for b in priority_buys[:3]],
            "sales": [s["player"] for s in sells if s["urgency"] == "immediate"],
        },
        "phase_2_mid_summer": {
            "description": "Complete secondary business after World Cup",
            "targets": [b["player"] for b in secondary_buys[:2]],
            "sales": [s["player"] for s in sells if s["urgency"] == "summer"],
        },
        "phase_3_late_window": {
            "description": "Opportunistic deals and final squad trimming",
            "targets": [b["player"] for b in opportunistic[:2]],
            "sales": [s["player"] for s in sells if s["urgency"] == "optional"],
        },
        "total_priority_signings": len(priority_buys),
        "total_sales_planned": len(sells),
    }
