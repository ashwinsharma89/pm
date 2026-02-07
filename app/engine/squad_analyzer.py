"""
Squad Analyzer Engine
=====================
Analyzes the Arsenal squad to identify deficiencies, strengths, and areas
requiring reinforcement for a triple-competition campaign (PL, CL, FA Cup).

Methodology:
- Position-by-position depth scoring
- Performance metric analysis (xG over/underperformance, progressive actions, etc.)
- Contract and financial risk assessment
- Age profile and squad sustainability analysis
- Comparison against elite benchmarks
"""

from app.data.squad_db import Player, PlayerStats


# Minimum depth requirements for a triple-competition squad
IDEAL_DEPTH = {
    "GK": {"starters": 1, "total": 2, "quality_threshold": 60},
    "CB": {"starters": 2, "total": 4, "quality_threshold": 65},
    "RB": {"starters": 1, "total": 2, "quality_threshold": 65},
    "LB": {"starters": 1, "total": 2, "quality_threshold": 65},
    "DM": {"starters": 1, "total": 2, "quality_threshold": 65},
    "CM": {"starters": 1, "total": 2, "quality_threshold": 65},
    "AM": {"starters": 1, "total": 2, "quality_threshold": 60},
    "RW": {"starters": 1, "total": 2, "quality_threshold": 65},
    "LW": {"starters": 1, "total": 2, "quality_threshold": 65},
    "ST": {"starters": 1, "total": 2, "quality_threshold": 65},
}

# Elite benchmark stats per 90 (for comparison)
ELITE_BENCHMARKS = {
    "ST": {"goals_per90": 0.55, "xg_per90": 0.60, "shot_accuracy": 45.0},
    "LW": {"goals_per90": 0.35, "assists_per90": 0.25, "dribbles_per90": 2.5},
    "RW": {"goals_per90": 0.30, "assists_per90": 0.30, "key_passes_per90": 2.0},
    "AM": {"assists_per90": 0.30, "key_passes_per90": 2.5, "progressive_passes_per90": 5.0},
    "CM": {"progressive_carries_per90": 4.0, "tackles_per90": 2.0, "interceptions_per90": 1.5},
    "DM": {"pass_completion": 90.0, "interceptions_per90": 2.0, "progressive_passes_per90": 4.0},
    "CB": {"aerials_per90": 2.5, "interceptions_per90": 1.5, "pass_completion": 90.0},
    "RB": {"progressive_carries_per90": 3.0, "tackles_per90": 2.0, "assists_per90": 0.15},
    "LB": {"progressive_carries_per90": 3.0, "tackles_per90": 2.0, "assists_per90": 0.15},
    "GK": {"save_pct": 72.0, "clean_sheet_pct": 40.0},
}


def analyze_squad_depth(squad: list[Player]) -> list[dict]:
    """Analyze squad depth at each position and identify gaps."""
    available = [p for p in squad if p.status in ("available",)]
    results = []

    for pos, req in IDEAL_DEPTH.items():
        players_in_pos = [p for p in available if p.position == pos]
        starters = [p for p in players_in_pos if p.role_in_squad == "starter"]
        quality_players = [p for p in players_in_pos
                          if p.stats.squawka_score >= req["quality_threshold"]]

        total_count = len(players_in_pos)
        starter_count = len(starters)
        quality_count = len(quality_players)
        depth_score = min(100, int((total_count / req["total"]) * 50 +
                                   (quality_count / max(1, req["total"])) * 50))

        status = "adequate"
        if total_count < req["total"]:
            status = "thin"
        if starter_count < req["starters"]:
            status = "critical"
        if total_count >= req["total"] and quality_count >= req["total"]:
            status = "strong"

        results.append({
            "position": pos,
            "required_total": req["total"],
            "current_total": total_count,
            "starters": starter_count,
            "quality_players": quality_count,
            "depth_score": depth_score,
            "status": status,
            "players": [{"name": p.name, "role": p.role_in_squad,
                        "squawka": p.stats.squawka_score,
                        "age": p.age} for p in players_in_pos],
        })

    return results


def analyze_performance_gaps(squad: list[Player]) -> list[dict]:
    """Identify individual and positional performance gaps using advanced metrics."""
    available = [p for p in squad if p.status == "available" and p.stats.minutes > 400]
    gaps = []

    for player in available:
        per90_minutes = player.stats.minutes / 90.0
        if per90_minutes < 3:
            continue

        issues = []
        pos = player.position

        # xG underperformance check (strikers/forwards)
        if pos in ("ST", "LW", "RW") and player.stats.xg > 0:
            xg_diff = player.stats.goals - player.stats.xg
            if xg_diff < -2.0:
                issues.append({
                    "metric": "xG Underperformance",
                    "detail": f"{player.stats.goals}G from {player.stats.xg:.1f}xG "
                              f"(delta: {xg_diff:+.1f})",
                    "severity": "high" if xg_diff < -3.0 else "medium",
                    "recommendation": "Finishing coaching or consider alternative"
                })

        # Shot accuracy check
        if pos == "ST" and player.stats.shot_accuracy_pct > 0:
            benchmark = ELITE_BENCHMARKS.get(pos, {}).get("shot_accuracy", 45.0)
            if player.stats.shot_accuracy_pct < benchmark:
                issues.append({
                    "metric": "Shot Accuracy",
                    "detail": f"{player.stats.shot_accuracy_pct:.1f}% "
                              f"(elite benchmark: {benchmark}%)",
                    "severity": "high" if player.stats.shot_accuracy_pct < 35 else "medium",
                    "recommendation": "Significant finishing improvement needed"
                })

        # Progressive action check (midfielders)
        if pos in ("CM", "DM", "AM"):
            prog_passes_per90 = player.stats.progressive_passes / per90_minutes
            benchmark = ELITE_BENCHMARKS.get(pos, {}).get("progressive_passes_per90", 4.0)
            if prog_passes_per90 < benchmark * 0.7:
                issues.append({
                    "metric": "Progressive Passing",
                    "detail": f"{prog_passes_per90:.1f}/90 "
                              f"(benchmark: {benchmark:.1f}/90)",
                    "severity": "medium",
                    "recommendation": "Below progressive passing threshold"
                })

        # Pass completion for deep midfielders
        if pos in ("DM", "CM") and player.stats.pass_completion_pct > 0:
            benchmark = ELITE_BENCHMARKS.get(pos, {}).get("pass_completion", 88.0)
            if player.stats.pass_completion_pct < benchmark:
                issues.append({
                    "metric": "Pass Completion",
                    "detail": f"{player.stats.pass_completion_pct:.1f}% "
                              f"(benchmark: {benchmark}%)",
                    "severity": "low",
                    "recommendation": "Below pass completion benchmark"
                })

        # Defensive contribution for defenders
        if pos in ("CB", "RB", "LB"):
            tackles_per90 = player.stats.tackles_won / per90_minutes
            benchmark = ELITE_BENCHMARKS.get(pos, {}).get("tackles_per90", 2.0)
            if tackles_per90 < benchmark * 0.6:
                issues.append({
                    "metric": "Defensive Actions",
                    "detail": f"{tackles_per90:.1f} tackles/90 "
                              f"(benchmark: {benchmark:.1f})",
                    "severity": "medium",
                    "recommendation": "Defensive engagement below benchmark"
                })

        if issues:
            gaps.append({
                "player": player.name,
                "position": pos,
                "minutes": player.stats.minutes,
                "issues": issues,
            })

    return gaps


def analyze_age_profile(squad: list[Player]) -> dict:
    """Analyze squad age distribution and sustainability."""
    available = [p for p in squad if p.status == "available"]

    age_groups = {
        "under_23": [],
        "prime_23_28": [],
        "experienced_29_31": [],
        "veteran_32_plus": [],
    }

    for p in available:
        if p.age < 23:
            age_groups["under_23"].append(p.name)
        elif p.age <= 28:
            age_groups["prime_23_28"].append(p.name)
        elif p.age <= 31:
            age_groups["experienced_29_31"].append(p.name)
        else:
            age_groups["veteran_32_plus"].append(p.name)

    avg_age = sum(p.age for p in available) / len(available) if available else 0

    return {
        "average_age": round(avg_age, 1),
        "age_groups": {k: {"count": len(v), "players": v} for k, v in age_groups.items()},
        "assessment": (
            "Well-balanced" if 24.5 <= avg_age <= 27.0
            else "Skewing young - may lack experience" if avg_age < 24.5
            else "Aging - need to invest in youth"
        ),
        "sustainability_score": min(100, int(
            (len(age_groups["prime_23_28"]) * 4 +
             len(age_groups["under_23"]) * 3 +
             len(age_groups["experienced_29_31"]) * 2 +
             len(age_groups["veteran_32_plus"]) * 1) /
            max(1, len(available)) * 10
        )),
    }


def analyze_contract_risk(squad: list[Player]) -> list[dict]:
    """Identify players with contract risk (expiring or sell-before-free scenarios)."""
    risks = []
    for p in squad:
        if not p.contract_expiry:
            continue
        expiry_year = int(p.contract_expiry[:4])
        # High risk: expires 2026 (this summer)
        if expiry_year == 2026:
            risks.append({
                "player": p.name,
                "position": p.position,
                "contract_expiry": p.contract_expiry,
                "risk_level": "critical",
                "market_value_m": p.market_value_m,
                "wage_weekly_k": p.wage_weekly_k,
                "recommendation": "Renew or let leave for free. Decision needed immediately."
            })
        # Medium risk: expires 2027 (sell now or risk free departure)
        elif expiry_year == 2027:
            risks.append({
                "player": p.name,
                "position": p.position,
                "contract_expiry": p.contract_expiry,
                "risk_level": "high",
                "market_value_m": p.market_value_m,
                "wage_weekly_k": p.wage_weekly_k,
                "recommendation": "Sell this summer or renew. Last chance to get a fee."
            })
        # Low risk: expires 2028
        elif expiry_year == 2028:
            risks.append({
                "player": p.name,
                "position": p.position,
                "contract_expiry": p.contract_expiry,
                "risk_level": "medium",
                "market_value_m": p.market_value_m,
                "wage_weekly_k": p.wage_weekly_k,
                "recommendation": "Monitor. Consider extension talks if key player."
            })

    risks.sort(key=lambda x: {"critical": 0, "high": 1, "medium": 2}.get(x["risk_level"], 3))
    return risks


def analyze_set_piece_vulnerability(squad: list[Player]) -> dict:
    """Analyze set-piece defending capability based on squad aerial/physical profiles."""
    available = [p for p in squad if p.status == "available" and p.stats.minutes > 400]
    defenders_mids = [p for p in available if p.position in ("CB", "DM", "CM")]

    aerial_avg = 0
    if defenders_mids:
        per90_aerials = []
        for p in defenders_mids:
            per90 = p.stats.minutes / 90.0
            if per90 > 0:
                per90_aerials.append(p.stats.aerials_won / per90)
        aerial_avg = sum(per90_aerials) / len(per90_aerials) if per90_aerials else 0

    return {
        "aerial_average_per90": round(aerial_avg, 2),
        "assessment": (
            "Adequate" if aerial_avg >= 2.0
            else "Below average - set-piece vulnerability confirmed"
        ),
        "key_aerial_players": [
            {"name": p.name, "aerials_won": p.stats.aerials_won}
            for p in sorted(defenders_mids, key=lambda x: x.stats.aerials_won, reverse=True)[:5]
        ],
        "recommendation": (
            "Arsenal's set-piece defensive record has been poor. Consider adding a "
            "physically dominant CB (e.g., Marc Guehi) and improving coaching methodology. "
            "Gabriel Magalhaes (52 aerials won) is the primary aerial threat but the team "
            "needs more presence around him."
        ),
    }


def generate_squad_report(squad: list[Player]) -> dict:
    """Generate a comprehensive squad analysis report."""
    depth = analyze_squad_depth(squad)
    perf_gaps = analyze_performance_gaps(squad)
    age_profile = analyze_age_profile(squad)
    contract_risks = analyze_contract_risk(squad)
    set_pieces = analyze_set_piece_vulnerability(squad)

    # Overall squad rating
    depth_avg = sum(d["depth_score"] for d in depth) / len(depth)
    critical_positions = [d for d in depth if d["status"] == "critical"]
    thin_positions = [d for d in depth if d["status"] == "thin"]

    overall_rating = max(0, min(100, int(
        depth_avg * 0.35 +
        age_profile["sustainability_score"] * 0.20 +
        (100 - len(perf_gaps) * 8) * 0.25 +
        (100 - len([r for r in contract_risks if r["risk_level"] == "critical"]) * 15) * 0.20
    )))

    return {
        "overall_rating": overall_rating,
        "depth_analysis": depth,
        "performance_gaps": perf_gaps,
        "age_profile": age_profile,
        "contract_risks": contract_risks,
        "set_piece_analysis": set_pieces,
        "critical_positions": [d["position"] for d in critical_positions],
        "thin_positions": [d["position"] for d in thin_positions],
        "headline_findings": _generate_headlines(depth, perf_gaps, contract_risks, set_pieces),
    }


def _generate_headlines(depth, perf_gaps, contract_risks, set_pieces) -> list[str]:
    """Generate human-readable headline findings."""
    headlines = []

    critical = [d for d in depth if d["status"] == "critical"]
    if critical:
        positions = ", ".join(d["position"] for d in critical)
        headlines.append(f"CRITICAL: Squad depth is critically thin at: {positions}")

    thin = [d for d in depth if d["status"] == "thin"]
    if thin:
        positions = ", ".join(d["position"] for d in thin)
        headlines.append(f"WARNING: Depth concerns at: {positions}")

    # xG underperformers
    xg_issues = [g for g in perf_gaps
                 if any(i["metric"] == "xG Underperformance" for i in g["issues"])]
    if xg_issues:
        names = ", ".join(g["player"] for g in xg_issues)
        headlines.append(f"PERFORMANCE: xG underperformance detected for: {names}")

    # Expiring contracts
    expiring = [r for r in contract_risks if r["risk_level"] == "critical"]
    if expiring:
        names = ", ".join(r["player"] for r in expiring)
        headlines.append(f"CONTRACT: Contracts expiring THIS summer: {names}")

    high_risk = [r for r in contract_risks if r["risk_level"] == "high"]
    if high_risk:
        names = ", ".join(r["player"] for r in high_risk)
        headlines.append(f"CONTRACT: Last chance to sell before free (2027 expiry): {names}")

    headlines.append(f"SET PIECES: {set_pieces['assessment']}")

    return headlines
