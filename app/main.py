"""
Arsenal Transfer Planner - Main Flask Application
===================================================
Enterprise-grade transfer planning dashboard for Arsenal FC 2026 summer window.
Combines squad analysis, transfer recommendations, and financial modeling.
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request

from app.data.squad_db import (
    build_arsenal_squad, build_transfer_targets, build_rival_squads,
    SELL_CANDIDATES, PROJECTED_SALE_REVENUE,
)
from app.engine.squad_analyzer import generate_squad_report
from app.engine.transfer_recommender import generate_transfer_plan
from app.engine.financial_model import FinancialModel

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), "templates"),
            static_folder=os.path.join(os.path.dirname(__file__), "static"))

# Default transfer budget (EUR millions)
DEFAULT_BUDGET_M = 150.0


def _build_full_plan(budget_m: float = DEFAULT_BUDGET_M) -> dict:
    """Build the complete transfer plan with all analysis."""
    squad = build_arsenal_squad()
    targets = build_transfer_targets()
    rivals = build_rival_squads()

    squad_report = generate_squad_report(squad)
    transfer_plan = generate_transfer_plan(squad, targets, squad_report, budget_m)

    # Build financial model
    fm = FinancialModel(base_budget_m=budget_m)
    for sell_rec in transfer_plan["sell_recommendations"]:
        fm.add_sale(sell_rec["player"], sell_rec["projected_fee_m"],
                    sell_rec["wage_saving_weekly_k"])

    # Add top 4 buy targets to financial model
    for buy_rec in transfer_plan["buy_recommendations"][:4]:
        fm.add_purchase(buy_rec["player"], buy_rec["estimated_fee_m"],
                        buy_rec["estimated_wages_k"], contract_years=5)

    financial_report = fm.get_complete_financial_report()

    return {
        "squad_report": squad_report,
        "transfer_plan": transfer_plan,
        "financial_report": financial_report,
        "rivals": rivals,
        "squad": [_serialize_player(p) for p in squad],
        "targets": [_serialize_player(p) for p in targets],
    }


def _serialize_player(player) -> dict:
    """Serialize a Player object to dict for JSON."""
    return {
        "name": player.name,
        "age": player.age,
        "position": player.position,
        "nationality": player.nationality,
        "squad_number": player.squad_number,
        "market_value_m": player.market_value_m,
        "wage_weekly_k": player.wage_weekly_k,
        "contract_expiry": player.contract_expiry,
        "status": player.status,
        "loan_club": player.loan_club,
        "role_in_squad": player.role_in_squad,
        "eye_test_notes": player.eye_test_notes,
        "strengths": player.strengths,
        "weaknesses": player.weaknesses,
        "stats": {
            "appearances": player.stats.appearances,
            "goals": player.stats.goals,
            "assists": player.stats.assists,
            "minutes": player.stats.minutes,
            "xg": player.stats.xg,
            "xa": player.stats.xa,
            "progressive_passes": player.stats.progressive_passes,
            "progressive_carries": player.stats.progressive_carries,
            "key_passes": player.stats.key_passes,
            "tackles_won": player.stats.tackles_won,
            "interceptions": player.stats.interceptions,
            "aerials_won": player.stats.aerials_won,
            "dribbles_completed": player.stats.dribbles_completed,
            "shot_accuracy_pct": player.stats.shot_accuracy_pct,
            "pass_completion_pct": player.stats.pass_completion_pct,
            "clean_sheets": player.stats.clean_sheets,
            "saves": player.stats.saves,
            "squawka_score": player.stats.squawka_score,
            "fotmob_rating": player.stats.fotmob_rating,
        },
    }


# ==================== ROUTES ====================

@app.route("/")
def index():
    """Main dashboard page."""
    return render_template("index.html")


@app.route("/api/plan")
def api_plan():
    """Get the full transfer plan as JSON."""
    budget = request.args.get("budget", DEFAULT_BUDGET_M, type=float)
    plan = _build_full_plan(budget)
    return jsonify(plan)


@app.route("/api/squad")
def api_squad():
    """Get current Arsenal squad data."""
    squad = build_arsenal_squad()
    return jsonify([_serialize_player(p) for p in squad])


@app.route("/api/targets")
def api_targets():
    """Get transfer target data."""
    targets = build_transfer_targets()
    return jsonify([_serialize_player(p) for p in targets])


@app.route("/api/squad-report")
def api_squad_report():
    """Get squad analysis report."""
    squad = build_arsenal_squad()
    report = generate_squad_report(squad)
    return jsonify(report)


@app.route("/api/financial")
def api_financial():
    """Get financial model report."""
    budget = request.args.get("budget", DEFAULT_BUDGET_M, type=float)
    plan = _build_full_plan(budget)
    return jsonify(plan["financial_report"])


@app.route("/api/rivals")
def api_rivals():
    """Get rival squad intelligence."""
    return jsonify(build_rival_squads())


@app.route("/api/deal-check")
def api_deal_check():
    """Check feasibility of a specific deal."""
    budget = request.args.get("budget", DEFAULT_BUDGET_M, type=float)
    player = request.args.get("player", "")
    fee = request.args.get("fee", 0, type=float)
    wage = request.args.get("wage", 0, type=float)

    fm = FinancialModel(base_budget_m=budget)
    # Add existing sales
    for name, rev in PROJECTED_SALE_REVENUE.items():
        fm.add_sale(name, rev, 0)
    result = fm.get_deal_feasibility(player, fee, wage)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
