"""
Financial Modeling Module
==========================
Models transfer budgets, amortization, wage bill impact, FFP compliance,
and deal feasibility for Arsenal's 2026 summer window.

Based on:
- Arsenal's reported 2024-25 revenue (~£450m)
- Estimated 2025-26 wage bill (~£186m gross)
- Reported summer 2025 spend of £248m
- KSE ownership model and investment patterns
"""


class FinancialModel:
    """Arsenal FC financial model for transfer planning."""

    # Arsenal financial parameters (estimated, Feb 2026)
    ANNUAL_REVENUE_M = 480.0  # GBP, including CL revenue boost
    CURRENT_WAGE_BILL_M = 186.0  # GBP gross annual
    WAGE_TO_REVENUE_RATIO = 0.39  # Current ratio
    MAX_WAGE_RATIO = 0.55  # Sustainable ceiling
    TRANSFER_AMORTIZATION_YEARS = 5  # Standard contract length for amortization
    PSR_ALLOWABLE_LOSS_M = 105.0  # Premier League PSR (3-year rolling)
    ESTIMATED_EXISTING_AMORTIZATION_M = 80.0  # From previous signings

    # Budget estimation
    ESTIMATED_SUMMER_BUDGET_M = 150.0  # EUR, reported/estimated

    def __init__(self, base_budget_m: float = 150.0):
        self.base_budget = base_budget_m  # EUR millions
        self.sale_revenue = 0.0
        self.purchases = []
        self.sales = []

    def add_sale(self, player_name: str, fee_m: float, wage_saving_weekly_k: float):
        """Register a player sale."""
        self.sales.append({
            "player": player_name,
            "fee_m": fee_m,
            "wage_saving_annual_m": round(wage_saving_weekly_k * 52 / 1000, 2),
        })
        self.sale_revenue += fee_m

    def add_purchase(self, player_name: str, fee_m: float, wage_weekly_k: float,
                     contract_years: int = 5):
        """Register a player purchase."""
        annual_amortization = fee_m / contract_years if contract_years > 0 else 0
        self.purchases.append({
            "player": player_name,
            "fee_m": fee_m,
            "wage_annual_m": round(wage_weekly_k * 52 / 1000, 2),
            "contract_years": contract_years,
            "annual_amortization_m": round(annual_amortization, 2),
        })

    @property
    def total_budget(self) -> float:
        """Total available budget including sales."""
        return self.base_budget + self.sale_revenue

    @property
    def total_spend(self) -> float:
        """Total spend on purchases."""
        return sum(p["fee_m"] for p in self.purchases)

    @property
    def remaining_budget(self) -> float:
        """Remaining transfer budget."""
        return self.total_budget - self.total_spend

    @property
    def net_spend(self) -> float:
        """Net spend (purchases - sales)."""
        return self.total_spend - self.sale_revenue

    def get_wage_impact(self) -> dict:
        """Calculate wage bill impact of all transactions."""
        new_wages = sum(p["wage_annual_m"] for p in self.purchases)
        saved_wages = sum(s["wage_saving_annual_m"] for s in self.sales)
        net_wage_change = new_wages - saved_wages

        new_wage_bill = self.CURRENT_WAGE_BILL_M + net_wage_change
        new_ratio = new_wage_bill / self.ANNUAL_REVENUE_M

        return {
            "current_wage_bill_m": self.CURRENT_WAGE_BILL_M,
            "new_wages_added_m": round(new_wages, 2),
            "wages_saved_m": round(saved_wages, 2),
            "net_wage_change_m": round(net_wage_change, 2),
            "projected_wage_bill_m": round(new_wage_bill, 2),
            "current_wage_ratio": round(self.WAGE_TO_REVENUE_RATIO * 100, 1),
            "projected_wage_ratio": round(new_ratio * 100, 1),
            "max_sustainable_ratio": round(self.MAX_WAGE_RATIO * 100, 1),
            "wage_headroom_m": round(
                (self.MAX_WAGE_RATIO * self.ANNUAL_REVENUE_M) - new_wage_bill, 2),
            "status": "healthy" if new_ratio < 0.45 else
                      "caution" if new_ratio < 0.55 else "danger",
        }

    def get_amortization_impact(self) -> dict:
        """Calculate amortization impact on accounts."""
        new_amortization = sum(p["annual_amortization_m"] for p in self.purchases)
        # Sales remove amortization (simplified - assume average 50% remaining)
        amort_removed = sum(s["fee_m"] * 0.1 for s in self.sales)  # Rough estimate

        total_amortization = (self.ESTIMATED_EXISTING_AMORTIZATION_M +
                             new_amortization - amort_removed)

        return {
            "existing_annual_amortization_m": self.ESTIMATED_EXISTING_AMORTIZATION_M,
            "new_amortization_m": round(new_amortization, 2),
            "amortization_removed_m": round(amort_removed, 2),
            "total_projected_amortization_m": round(total_amortization, 2),
            "purchases_detail": [
                {
                    "player": p["player"],
                    "fee_m": p["fee_m"],
                    "years": p["contract_years"],
                    "annual_amort_m": p["annual_amortization_m"],
                }
                for p in self.purchases
            ],
        }

    def get_psr_compliance(self) -> dict:
        """Assess Premier League Profit and Sustainability Rules compliance."""
        wage_impact = self.get_wage_impact()
        amort_impact = self.get_amortization_impact()

        # Simplified PSR calculation
        # Loss = Wages + Amortization - Revenue + Other costs
        estimated_other_costs = 60.0  # Stadium, staff, operations
        estimated_annual_cost = (
            wage_impact["projected_wage_bill_m"] +
            amort_impact["total_projected_amortization_m"] +
            estimated_other_costs
        )
        estimated_annual_profit = self.ANNUAL_REVENUE_M - estimated_annual_cost

        # PSR looks at 3-year rolling average
        # Assume previous 2 years were roughly break-even
        three_year_avg = estimated_annual_profit / 1  # Simplified

        return {
            "estimated_annual_revenue_m": self.ANNUAL_REVENUE_M,
            "estimated_annual_costs_m": round(estimated_annual_cost, 2),
            "estimated_annual_profit_m": round(estimated_annual_profit, 2),
            "psr_allowable_loss_m": self.PSR_ALLOWABLE_LOSS_M,
            "psr_headroom_m": round(self.PSR_ALLOWABLE_LOSS_M + estimated_annual_profit, 2),
            "status": (
                "compliant" if estimated_annual_profit > -self.PSR_ALLOWABLE_LOSS_M
                else "at_risk"
            ),
            "notes": (
                "Arsenal's strong commercial revenue and CL qualification provide "
                "significant PSR headroom. The proposed transfer plan is well within "
                "sustainable limits."
                if estimated_annual_profit > -50
                else "Caution: Proposed spending approaches PSR limits. Consider "
                     "phasing purchases or increasing sales."
            ),
        }

    def get_deal_feasibility(self, player_name: str, fee_m: float,
                              wage_weekly_k: float) -> dict:
        """Assess feasibility of a specific deal within current constraints."""
        can_afford_fee = fee_m <= self.remaining_budget
        wage_impact = self.get_wage_impact()
        wage_headroom = wage_impact["wage_headroom_m"]
        annual_wage = wage_weekly_k * 52 / 1000
        can_afford_wage = annual_wage < wage_headroom

        feasibility_score = 0
        if can_afford_fee:
            feasibility_score += 50
        else:
            feasibility_score += max(0, int(50 * (self.remaining_budget / fee_m)))

        if can_afford_wage:
            feasibility_score += 30
        else:
            feasibility_score += max(0, int(30 * (wage_headroom / annual_wage)))

        # Add 20 for PSR compliance
        psr = self.get_psr_compliance()
        if psr["status"] == "compliant":
            feasibility_score += 20

        return {
            "player": player_name,
            "fee_m": fee_m,
            "wage_weekly_k": wage_weekly_k,
            "remaining_budget_m": round(self.remaining_budget, 2),
            "can_afford_fee": can_afford_fee,
            "can_afford_wage": can_afford_wage,
            "feasibility_score": feasibility_score,
            "status": (
                "go" if feasibility_score >= 80
                else "negotiate" if feasibility_score >= 50
                else "stretch" if feasibility_score >= 30
                else "not_feasible"
            ),
            "recommended_max_fee_m": round(self.remaining_budget * 0.8, 1),
            "recommended_max_wage_k": round(wage_headroom / 52 * 1000 * 0.3, 0),
        }

    def get_complete_financial_report(self) -> dict:
        """Generate complete financial overview of the transfer window plan."""
        return {
            "budget_overview": {
                "base_budget_m": self.base_budget,
                "sale_revenue_m": round(self.sale_revenue, 2),
                "total_available_m": round(self.total_budget, 2),
                "total_spend_m": round(self.total_spend, 2),
                "remaining_m": round(self.remaining_budget, 2),
                "net_spend_m": round(self.net_spend, 2),
            },
            "transactions": {
                "purchases": self.purchases,
                "sales": self.sales,
            },
            "wage_impact": self.get_wage_impact(),
            "amortization": self.get_amortization_impact(),
            "psr_compliance": self.get_psr_compliance(),
        }
