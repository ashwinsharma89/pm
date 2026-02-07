/**
 * Arsenal Transfer War Room - Frontend Application
 * ==================================================
 * Enterprise-grade transfer planning dashboard.
 * Fetches data from Flask API and renders all dashboard views.
 */

(function () {
    "use strict";

    let DATA = null;
    const $ = (s) => document.querySelector(s);
    const $$ = (s) => document.querySelectorAll(s);

    // ---- BUDGET SLIDER ----
    const slider = $("#budgetSlider");
    const display = $("#budgetDisplay");
    slider.addEventListener("input", () => {
        display.textContent = `\u20AC${slider.value}m`;
    });
    $("#refreshBtn").addEventListener("click", () => loadData(Number(slider.value)));

    // ---- TABS ----
    $$(".tab").forEach((tab) => {
        tab.addEventListener("click", () => {
            $$(".tab").forEach((t) => t.classList.remove("active"));
            $$(".tab-content").forEach((tc) => tc.classList.remove("active"));
            tab.classList.add("active");
            const target = tab.dataset.tab;
            $(`#tab-${target}`).classList.add("active");
        });
    });

    // ---- MODAL ----
    $("#modalClose").addEventListener("click", closeModal);
    $("#playerModal").addEventListener("click", (e) => {
        if (e.target === $("#playerModal")) closeModal();
    });
    function closeModal() {
        $("#playerModal").classList.remove("show");
    }
    function openModal(html) {
        $("#modalBody").innerHTML = html;
        $("#playerModal").classList.add("show");
    }

    // ---- LOAD DATA ----
    // Store the original baseline data for client-side recalculations
    let BASELINE = null;

    async function loadData(budget) {
        const loader = $("#loadingIndicator");
        loader.classList.remove("hidden");

        // First load: use embedded data
        if (!DATA && window.__INITIAL_DATA__) {
            DATA = window.__INITIAL_DATA__;
            BASELINE = JSON.parse(JSON.stringify(DATA)); // deep clone
            render();
            return;
        }

        // Recalculate: try server first, fall back to client-side
        try {
            const res = await fetch(`/api/plan?budget=${budget || 150}`);
            if (!res.ok) throw new Error("Server unavailable");
            DATA = await res.json();
            render();
        } catch (err) {
            // Client-side recalculation (works in standalone mode)
            if (BASELINE) {
                DATA = recalcWithBudget(budget || 150);
                render();
            } else {
                loader.innerHTML = `<p style="color:var(--red)">Error loading data: ${err.message}</p>`;
            }
        }
    }

    // ---- CLIENT-SIDE BUDGET RECALCULATION ENGINE ----
    function recalcWithBudget(budget) {
        // Deep clone baseline so we don't mutate it
        const d = JSON.parse(JSON.stringify(BASELINE));
        const saleRevenue = d.transfer_plan.sell_recommendations.reduce((s, r) => s + r.projected_fee_m, 0);
        const totalAvailable = budget + saleRevenue;

        // Recalculate buy recommendation scores based on new budget
        for (const b of d.transfer_plan.buy_recommendations) {
            const fee = b.estimated_fee_m;
            // Financial value: lower fee relative to budget = better
            let valueScore;
            if (fee === 0) {
                valueScore = 100;
            } else {
                valueScore = Math.max(10, Math.min(100, Math.round(100 - (fee / budget) * 80)));
            }
            // Feasibility: can we afford it?
            let feasScore = 70;
            if (fee === 0) { feasScore = 95; }
            else {
                if (fee > budget * 0.6) feasScore -= 20;
                if (fee > budget) feasScore -= 30;
            }
            // Check risk keywords in risk_factors
            const riskKw = ["city", "liverpool", "real madrid", "already signed"];
            for (const rf of (b.risk_factors || [])) {
                if (riskKw.some(k => rf.toLowerCase().includes(k))) { feasScore -= 15; break; }
            }
            feasScore = Math.max(10, Math.min(100, feasScore));

            b.score_breakdown.financial_value = valueScore;
            b.score_breakdown.feasibility = feasScore;

            // Recalculate priority score with same weights
            const sb = b.score_breakdown;
            b.priority_score = Math.round(
                sb.squad_need * 0.25 +
                sb.player_quality * 0.20 +
                sb.financial_value * 0.20 +
                sb.age_profile * 0.15 +
                sb.feasibility * 0.20
            );

            // Update summary tier label
            const tier = b.priority_score >= 75 ? "PRIORITY 1" : b.priority_score >= 60 ? "PRIORITY 2" : "PRIORITY 3";
            b.recommendation_summary = `${tier}: Sign ${b.player} (${b.position}, ${b.age}). Estimated fee: \u20AC${fee}m. Recommendation score: ${b.priority_score}/100.`;
        }
        // Re-sort by new priority score
        d.transfer_plan.buy_recommendations.sort((a, b) => b.priority_score - a.priority_score);

        // Recalculate financial report
        const top4 = d.transfer_plan.buy_recommendations.slice(0, 4);
        const totalSpend = top4.reduce((s, b) => s + b.estimated_fee_m, 0);
        const newWagesAnnual = top4.reduce((s, b) => s + b.estimated_wages_k * 52 / 1000, 0);
        const wageSaved = d.transfer_plan.sell_recommendations.reduce((s, r) => s + r.wage_saving_annual_m, 0);
        const currentWageBill = 186.0;
        const annualRevenue = 480.0;
        const netWageChange = newWagesAnnual - wageSaved;
        const projectedWageBill = currentWageBill + netWageChange;
        const wageRatio = projectedWageBill / annualRevenue;
        const maxRatio = 0.55;
        const existingAmort = 80.0;
        const newAmort = top4.reduce((s, b) => s + b.estimated_fee_m / 5, 0);
        const amortRemoved = saleRevenue * 0.1;
        const totalAmort = existingAmort + newAmort - amortRemoved;
        const otherCosts = 60.0;
        const totalCosts = projectedWageBill + totalAmort + otherCosts;
        const annualProfit = annualRevenue - totalCosts;

        d.financial_report = {
            budget_overview: {
                base_budget_m: budget,
                sale_revenue_m: Math.round(saleRevenue * 10) / 10,
                total_available_m: Math.round(totalAvailable * 10) / 10,
                total_spend_m: Math.round(totalSpend * 10) / 10,
                remaining_m: Math.round((totalAvailable - totalSpend) * 10) / 10,
                net_spend_m: Math.round((totalSpend - saleRevenue) * 10) / 10,
            },
            wage_impact: {
                current_wage_bill_m: currentWageBill,
                new_wages_added_m: Math.round(newWagesAnnual * 100) / 100,
                wages_saved_m: Math.round(wageSaved * 100) / 100,
                net_wage_change_m: Math.round(netWageChange * 100) / 100,
                projected_wage_bill_m: Math.round(projectedWageBill * 100) / 100,
                current_wage_ratio: Math.round(currentWageBill / annualRevenue * 1000) / 10,
                projected_wage_ratio: Math.round(wageRatio * 1000) / 10,
                max_sustainable_ratio: Math.round(maxRatio * 1000) / 10,
                wage_headroom_m: Math.round((maxRatio * annualRevenue - projectedWageBill) * 100) / 100,
                status: wageRatio < 0.45 ? "healthy" : wageRatio < 0.55 ? "caution" : "danger",
            },
            amortization: {
                existing_annual_amortization_m: existingAmort,
                new_amortization_m: Math.round(newAmort * 100) / 100,
                amortization_removed_m: Math.round(amortRemoved * 100) / 100,
                total_projected_amortization_m: Math.round(totalAmort * 100) / 100,
                purchases_detail: top4.map(b => ({
                    player: b.player,
                    fee_m: b.estimated_fee_m,
                    years: 5,
                    annual_amort_m: Math.round(b.estimated_fee_m / 5 * 100) / 100,
                })),
            },
            psr_compliance: {
                estimated_annual_revenue_m: annualRevenue,
                estimated_annual_costs_m: Math.round(totalCosts * 100) / 100,
                estimated_annual_profit_m: Math.round(annualProfit * 100) / 100,
                psr_allowable_loss_m: 105.0,
                psr_headroom_m: Math.round((105.0 + annualProfit) * 100) / 100,
                status: annualProfit > -105 ? "compliant" : "at_risk",
                notes: annualProfit > -50
                    ? "Arsenal's strong commercial revenue and CL qualification provide significant PSR headroom. The proposed transfer plan is well within sustainable limits."
                    : "Caution: Proposed spending approaches PSR limits. Consider phasing purchases or increasing sales.",
            },
        };

        // Update financial summary in transfer_plan
        d.transfer_plan.financial_summary = {
            transfer_budget_m: budget,
            projected_sale_revenue_m: Math.round(saleRevenue * 10) / 10,
            total_available_m: Math.round(totalAvailable * 10) / 10,
            projected_purchase_cost_m: Math.round(totalSpend * 10) / 10,
            net_spend_m: Math.round((totalSpend - saleRevenue) * 10) / 10,
            wage_savings_annual_m: Math.round(wageSaved * 10) / 10,
            new_wages_annual_m: Math.round(newWagesAnnual * 10) / 10,
            net_wage_change_annual_m: Math.round(netWageChange * 10) / 10,
        };

        // Update strategy phases with re-sorted targets
        const pBuys = d.transfer_plan.buy_recommendations;
        const priority = pBuys.filter(b => b.priority_score >= 70);
        const secondary = pBuys.filter(b => b.priority_score >= 55 && b.priority_score < 70);
        const opp = pBuys.filter(b => b.priority_score < 55);
        const sells = d.transfer_plan.sell_recommendations;
        d.transfer_plan.transfer_window_strategy = {
            phase_1_early_summer: {
                description: "Secure priority targets before World Cup distraction",
                targets: priority.slice(0, 3).map(b => b.player),
                sales: sells.filter(s => s.urgency === "immediate").map(s => s.player),
            },
            phase_2_mid_summer: {
                description: "Complete secondary business after World Cup",
                targets: secondary.slice(0, 2).map(b => b.player),
                sales: sells.filter(s => s.urgency === "summer").map(s => s.player),
            },
            phase_3_late_window: {
                description: "Opportunistic deals and final squad trimming",
                targets: opp.slice(0, 2).map(b => b.player),
                sales: sells.filter(s => s.urgency === "optional").map(s => s.player),
            },
            total_priority_signings: priority.length,
            total_sales_planned: sells.length,
        };

        return d;
    }

    // ==================== INTEL STATE ====================
    let INTEL_UPDATES = {}; // keyed by player name
    let INTEL_LOG = [];

    function loadIntelFromStorage() {
        try {
            const saved = localStorage.getItem("arsenal_intel");
            if (saved) {
                const parsed = JSON.parse(saved);
                INTEL_UPDATES = parsed.updates || {};
                INTEL_LOG = parsed.log || [];
            }
        } catch (e) { /* ignore */ }
    }
    function saveIntelToStorage() {
        try {
            localStorage.setItem("arsenal_intel", JSON.stringify({
                updates: INTEL_UPDATES,
                log: INTEL_LOG,
            }));
        } catch (e) { /* ignore */ }
    }

    function applyIntelToBaseline() {
        // Start from a fresh clone of the original baseline
        const d = JSON.parse(JSON.stringify(BASELINE));

        // Remove or modify targets based on intel
        const removedNames = [];
        for (const [name, intel] of Object.entries(INTEL_UPDATES)) {
            if (intel.status === "signed_by_rival") {
                removedNames.push(name);
                // Remove from buy recommendations
                d.transfer_plan.buy_recommendations = d.transfer_plan.buy_recommendations.filter(b => b.player !== name);
                // Remove from targets
                d.targets = (d.targets || []).filter(t => t.name !== name);
            } else if (intel.status === "priced_out") {
                removedNames.push(name);
                d.transfer_plan.buy_recommendations = d.transfer_plan.buy_recommendations.filter(b => b.player !== name);
                d.targets = (d.targets || []).filter(t => t.name !== name);
            }
            // Fee adjustments
            if (intel.fee !== undefined && intel.fee !== null) {
                const buyRec = d.transfer_plan.buy_recommendations.find(b => b.player === name);
                if (buyRec) {
                    buyRec.estimated_fee_m = intel.fee;
                    if (buyRec.deal_structure) buyRec.deal_structure.total = intel.fee;
                }
                const target = (d.targets || []).find(t => t.name === name);
                if (target) target.market_value_m = intel.fee;
            }
            // Add rival info to risk factors
            if (intel.status === "signed_by_rival" && intel.rival) {
                const buyRec = d.transfer_plan.buy_recommendations.find(b => b.player === name);
                if (buyRec) {
                    buyRec.risk_factors = buyRec.risk_factors || [];
                    buyRec.risk_factors.push(`Already signed by ${intel.rival}`);
                }
            }
        }

        // Update BASELINE clone (this becomes the new working baseline for recalc)
        BASELINE = d;
        // Recalculate with current budget
        const budget = Number(slider.value) || 150;
        DATA = recalcWithBudget(budget);
        render();
    }

    function render() {
        if (!DATA) return;
        $("#loadingIndicator").classList.add("hidden");
        renderOverview();
        renderSquadTab();
        renderSellTab();
        renderBuyTab();
        renderFinancialTab();
        renderRivalsTab();
        renderStrategyTab();
        renderIntelTab();
    }

    // ==================== OVERVIEW ====================
    function renderOverview() {
        const sr = DATA.squad_report;
        const tp = DATA.transfer_plan;
        const fin = DATA.financial_report;

        // KPIs
        $("#kpiRow").innerHTML = `
            ${kpi(sr.overall_rating + "/100", "Squad Rating", ratingClass(sr.overall_rating))}
            ${kpi(sr.age_profile.average_age, "Average Age", "kpi-blue")}
            ${kpi("\u20AC" + fin.budget_overview.total_available_m + "m", "Total Budget", "kpi-green")}
            ${kpi(tp.sell_recommendations.length, "Players OUT", "kpi-red")}
            ${kpi(tp.buy_recommendations.filter(b => b.priority_score >= 60).length, "Priority Targets", "kpi-gold")}
            ${kpi(sr.critical_positions.length + sr.thin_positions.length, "Positions to Address", "kpi-yellow")}
        `;

        // Headlines
        const hl = sr.headline_findings || [];
        $("#headlinesList").innerHTML = hl
            .map((h) => {
                let cls = "headline-info";
                if (h.startsWith("CRITICAL")) cls = "headline-critical";
                else if (h.startsWith("WARNING") || h.startsWith("PERFORMANCE") || h.startsWith("CONTRACT"))
                    cls = "headline-warning";
                else if (h.startsWith("SET PIECES")) cls = "headline-warning";
                return `<li class="${cls}">${h}</li>`;
            })
            .join("");

        // Pitch grid
        renderPitchGrid(sr.depth_analysis);

        // Quick plan
        let sellHtml = tp.sell_recommendations
            .map(
                (s) =>
                    `<div class="quick-item"><span><span class="qi-name">${s.player}</span><span class="qi-pos">${s.position}</span></span><span class="qi-fee">${s.projected_fee_m > 0 ? "\u20AC" + s.projected_fee_m + "m" : "Free / Released"}</span></div>`
            )
            .join("");
        $("#quickSellList").innerHTML = sellHtml || "<p>No sales planned</p>";

        let buyHtml = tp.buy_recommendations
            .filter((b) => b.priority_score >= 55)
            .map(
                (b) =>
                    `<div class="quick-item"><span><span class="qi-name">${b.player}</span><span class="qi-pos">${b.position}</span></span><span class="qi-fee">\u20AC${b.estimated_fee_m}m (Score: ${b.priority_score})</span></div>`
            )
            .join("");
        $("#quickBuyList").innerHTML = buyHtml || "<p>No targets identified</p>";
    }

    function renderPitchGrid(depth) {
        // Map positions to a 5x4 grid (football pitch layout)
        const layout = [
            [null, null, "ST", null, null],
            ["LW", null, "AM", null, "RW"],
            [null, "CM", "DM", "CM", null],
            ["LB", "CB", "GK", "CB", "RB"],
        ];
        const depthMap = {};
        depth.forEach((d) => (depthMap[d.position] = d));

        // For CM we combine the single CM entry for both grid slots
        let html = "";
        const seen = new Set();
        for (const row of layout) {
            for (const pos of row) {
                if (!pos) {
                    html += `<div class="pitch-cell" style="visibility:hidden"></div>`;
                    continue;
                }
                const d = depthMap[pos];
                if (!d) {
                    html += `<div class="pitch-cell" style="visibility:hidden"></div>`;
                    continue;
                }
                if (pos === "CM" && seen.has("CM")) {
                    html += `<div class="pitch-cell" style="visibility:hidden"></div>`;
                    continue;
                }
                seen.add(pos);
                const cls = `depth-${d.status}`;
                html += `<div class="pitch-cell ${cls}" title="${pos}: ${d.current_total}/${d.required_total} players">
                    <span class="pos-label">${pos}</span>
                    <span class="pos-count">${d.current_total}/${d.required_total}</span>
                </div>`;
            }
        }
        $("#pitchGrid").innerHTML = html;
    }

    // ==================== SQUAD TAB ====================
    function renderSquadTab() {
        const sr = DATA.squad_report;
        const squad = DATA.squad;

        // Age profile
        const ap = sr.age_profile;
        const total = Object.values(ap.age_groups).reduce((s, g) => s + g.count, 0) || 1;
        const groups = [
            { key: "under_23", label: "Under 23", cls: "youth" },
            { key: "prime_23_28", label: "Prime (23-28)", cls: "prime" },
            { key: "experienced_29_31", label: "Experienced (29-31)", cls: "experienced" },
            { key: "veteran_32_plus", label: "Veteran (32+)", cls: "veteran" },
        ];
        let ageHtml = `<div class="age-bars">`;
        for (const g of groups) {
            const data = ap.age_groups[g.key] || { count: 0, players: [] };
            const pct = Math.round((data.count / total) * 100);
            ageHtml += `<div class="age-group">
                <span class="age-label">${g.label} (${data.count})</span>
                <div class="age-bar-track">
                    <div class="age-bar-fill ${g.cls}" style="width:${pct}%">${pct}%</div>
                </div>
            </div>`;
        }
        ageHtml += `</div>
            <p style="margin-top:12px;font-size:13px;color:var(--text-secondary)">
                Average Age: <strong>${ap.average_age}</strong> &mdash; ${ap.assessment}.
                Sustainability Score: <strong>${ap.sustainability_score}/100</strong>
            </p>`;
        $("#ageProfile").innerHTML = ageHtml;

        // Contract risks
        const cr = sr.contract_risks || [];
        let crHtml = cr
            .map(
                (r) => `<div class="risk-bar">
                <div class="risk-indicator risk-${r.risk_level}"></div>
                <span class="risk-name">${r.player}</span>
                <span class="risk-detail">${r.position} &middot; Expires ${r.contract_expiry} &middot; \u20AC${r.market_value_m}m &middot; ${r.wage_weekly_k}k/w</span>
                <span style="font-size:12px;color:var(--text-muted)">${r.recommendation}</span>
            </div>`
            )
            .join("");
        $("#contractRisks").innerHTML = crHtml || "<p>No contract risks detected</p>";

        // Performance gaps
        const pg = sr.performance_gaps || [];
        let pgHtml = pg
            .map((g) => {
                let issuesHtml = g.issues
                    .map(
                        (i) => `<div class="gap-issue">
                        <span class="severity-badge severity-${i.severity}">${i.severity}</span>
                        <span><strong>${i.metric}:</strong> ${i.detail}</span>
                    </div>`
                    )
                    .join("");
                return `<div class="gap-card"><h4>${g.player} (${g.position}, ${g.minutes} min)</h4>${issuesHtml}</div>`;
            })
            .join("");
        $("#perfGaps").innerHTML = pgHtml || "<p>No significant performance gaps detected</p>";

        // Set pieces
        const sp = sr.set_piece_analysis || {};
        let spHtml = `<p style="margin-bottom:12px;font-size:14px"><strong>Assessment:</strong> ${sp.assessment || "N/A"}</p>`;
        spHtml += `<p style="margin-bottom:12px;font-size:13px;color:var(--text-secondary)">${sp.recommendation || ""}</p>`;
        if (sp.key_aerial_players) {
            spHtml += `<div class="stats-grid">`;
            sp.key_aerial_players.forEach((p) => {
                spHtml += `<div class="stat-box"><div class="stat-val">${p.aerials_won}</div><div class="stat-label">${p.name}</div></div>`;
            });
            spHtml += `</div>`;
        }
        $("#setPieces").innerHTML = spHtml;

        // Squad table
        const avail = squad.filter((p) => p.status === "available");
        avail.sort((a, b) => posOrder(a.position) - posOrder(b.position));
        let tbHtml = avail
            .map(
                (p) => `<tr data-player='${encodeURIComponent(JSON.stringify(p))}'>
                <td>${p.squad_number || "-"}</td>
                <td>${p.name}</td>
                <td>${p.position}</td>
                <td>${p.age}</td>
                <td>${p.nationality}</td>
                <td>${p.stats.appearances}</td>
                <td>${p.stats.goals}</td>
                <td>${p.stats.assists}</td>
                <td>${p.stats.minutes}</td>
                <td>${p.stats.xg.toFixed(1)}</td>
                <td>${p.stats.squawka_score}</td>
                <td>${p.stats.fotmob_rating.toFixed(1)}</td>
                <td>\u20AC${p.market_value_m}m</td>
                <td>\u00A3${p.wage_weekly_k}k</td>
                <td>${p.contract_expiry.substring(0, 7)}</td>
                <td>${roleLabel(p.role_in_squad)}</td>
            </tr>`
            )
            .join("");
        $("#squadBody").innerHTML = tbHtml;

        // Click to open modal
        $$("#squadBody tr").forEach((tr) => {
            tr.addEventListener("click", () => {
                const p = JSON.parse(decodeURIComponent(tr.dataset.player));
                openPlayerModal(p);
            });
        });
    }

    function openPlayerModal(p) {
        let html = `
            <h2 style="margin-bottom:4px">${p.name}</h2>
            <p style="color:var(--text-secondary);margin-bottom:16px">${p.position} &middot; Age ${p.age} &middot; ${p.nationality} &middot; #${p.squad_number || "N/A"}</p>
            <div class="stats-grid" style="margin-bottom:16px">
                ${statBox(p.stats.appearances, "Apps")}
                ${statBox(p.stats.goals, "Goals")}
                ${statBox(p.stats.assists, "Assists")}
                ${statBox(p.stats.minutes, "Minutes")}
                ${statBox(p.stats.xg.toFixed(1), "xG")}
                ${statBox(p.stats.xa.toFixed(1), "xA")}
                ${statBox(p.stats.progressive_passes, "Prog Pass")}
                ${statBox(p.stats.progressive_carries, "Prog Carry")}
                ${statBox(p.stats.key_passes, "Key Pass")}
                ${statBox(p.stats.tackles_won, "Tackles")}
                ${statBox(p.stats.interceptions, "Intercept")}
                ${statBox(p.stats.squawka_score, "Squawka")}
            </div>
            <h4 style="font-size:12px;color:var(--text-secondary);text-transform:uppercase;margin-bottom:6px">Eye Test / Scout Notes</h4>
            <div class="eye-test-box" style="margin-bottom:14px">${p.eye_test_notes}</div>
            <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:14px">
                <div>
                    <h4 style="font-size:12px;color:var(--text-secondary);text-transform:uppercase;margin-bottom:6px">Strengths</h4>
                    <div class="risk-tags">${(p.strengths || []).map((s) => `<span class="strength-tag">${s}</span>`).join("")}</div>
                </div>
                <div>
                    <h4 style="font-size:12px;color:var(--text-secondary);text-transform:uppercase;margin-bottom:6px">Weaknesses</h4>
                    <div class="risk-tags">${(p.weaknesses || []).map((w) => `<span class="risk-tag">${w}</span>`).join("")}</div>
                </div>
            </div>
            <div style="display:flex;gap:16px;font-size:13px;color:var(--text-secondary)">
                <span>Value: <strong>\u20AC${p.market_value_m}m</strong></span>
                <span>Wage: <strong>\u00A3${p.wage_weekly_k}k/wk</strong></span>
                <span>Contract: <strong>${p.contract_expiry}</strong></span>
                <span>Role: <strong>${roleLabel(p.role_in_squad)}</strong></span>
            </div>
        `;
        openModal(html);
    }

    // ==================== SELL TAB ====================
    function renderSellTab() {
        const sells = DATA.transfer_plan.sell_recommendations || [];
        const totalRev = sells.reduce((s, r) => s + r.projected_fee_m, 0);
        const totalWage = sells.reduce((s, r) => s + r.wage_saving_annual_m, 0);

        $("#sellKpi").innerHTML = `
            ${kpi(sells.length, "Players to Sell/Release", "kpi-red")}
            ${kpi("\u20AC" + totalRev.toFixed(1) + "m", "Projected Revenue", "kpi-green")}
            ${kpi("\u00A3" + totalWage.toFixed(1) + "m/yr", "Wage Savings", "kpi-gold")}
        `;

        let html = "";
        for (const s of sells) {
            const scoreClass = s.priority_score >= 75 ? "score-high" : s.priority_score >= 50 ? "score-mid" : "score-low";
            html += `
            <div class="rec-card sell-card">
                <div class="rec-header">
                    <div class="rec-player-info">
                        <h3>${s.player}</h3>
                        <div class="rec-meta">
                            <span>${s.position}</span>
                            <span>Age ${s.age}</span>
                            <span>Role: ${s.current_role}</span>
                            <span>Contract: ${s.contract_expiry}</span>
                            <span>Wage: \u00A3${s.wage_saving_weekly_k}k/wk</span>
                        </div>
                    </div>
                    <div class="rec-score">
                        <span class="priority-badge ${s.urgency === "immediate" ? "priority-1" : s.urgency === "summer" ? "priority-2" : "priority-3"}">${s.urgency}</span>
                        <div class="score-ring ${scoreClass}">${s.priority_score}</div>
                    </div>
                </div>
                <div class="rec-body">
                    <div class="rec-section">
                        <h4>Projected Fee</h4>
                        <p style="font-size:20px;font-weight:700;color:var(--green)">${s.projected_fee_m > 0 ? "\u20AC" + s.projected_fee_m + "m" : "Free Agent / Release"}</p>
                        <p style="font-size:13px;color:var(--text-secondary);margin-top:4px">Annual wage saving: \u00A3${s.wage_saving_annual_m}m</p>
                    </div>
                    <div class="rec-section">
                        <h4>Reasons to Sell</h4>
                        ${s.reasons.map((r) => `<div class="rec-reason">${r}</div>`).join("")}
                    </div>
                    <div class="rec-section">
                        <h4>Scout / Eye Test Assessment</h4>
                        <div class="eye-test-box">${s.eye_test}</div>
                    </div>
                    <div class="rec-section">
                        <h4>Summary</h4>
                        <p style="font-size:14px;font-weight:500">${s.recommendation_summary}</p>
                    </div>
                </div>
            </div>`;
        }
        $("#sellCards").innerHTML = html;
    }

    // ==================== BUY TAB ====================
    function renderBuyTab() {
        const buys = DATA.transfer_plan.buy_recommendations || [];
        let html = "";

        for (const b of buys) {
            const scoreClass = b.priority_score >= 75 ? "score-high" : b.priority_score >= 55 ? "score-mid" : "score-low";
            const tier = b.priority_score >= 75 ? "priority-1" : b.priority_score >= 60 ? "priority-2" : "priority-3";
            const tierLabel = b.priority_score >= 75 ? "Priority 1" : b.priority_score >= 60 ? "Priority 2" : "Priority 3";

            const st = b.stats_summary || {};
            const sb = b.score_breakdown || {};
            const deal = b.deal_structure || {};

            html += `
            <div class="rec-card buy-card">
                <div class="rec-header">
                    <div class="rec-player-info">
                        <h3>${b.player}</h3>
                        <div class="rec-meta">
                            <span>${b.position}</span>
                            <span>Age ${b.age}</span>
                            <span>${b.nationality}</span>
                            <span>From: ${b.current_club}</span>
                            <span>Contract: ${b.contract_expiry}</span>
                        </div>
                    </div>
                    <div class="rec-score">
                        <span class="priority-badge ${tier}">${tierLabel}</span>
                        <div class="score-ring ${scoreClass}">${b.priority_score}</div>
                    </div>
                </div>
                <div class="rec-body">
                    <!-- SCORE BREAKDOWN -->
                    <div class="rec-section">
                        <h4>Score Breakdown</h4>
                        <div class="score-breakdown">
                            ${breakdownBar("Need", sb.squad_need)}
                            ${breakdownBar("Quality", sb.player_quality)}
                            ${breakdownBar("Value", sb.financial_value)}
                            ${breakdownBar("Age", sb.age_profile)}
                            ${breakdownBar("Feasibility", sb.feasibility)}
                        </div>
                    </div>

                    <!-- STATS -->
                    <div class="rec-section">
                        <h4>2025-26 Season Stats</h4>
                        <div class="stats-grid">
                            ${statBox(st.appearances, "Apps")}
                            ${statBox(st.goals, "Goals")}
                            ${statBox(st.assists, "Assists")}
                            ${statBox(st.minutes, "Min")}
                            ${statBox(st.goals_per90, "G/90")}
                            ${statBox(st.assists_per90, "A/90")}
                            ${statBox(st.xg ? st.xg.toFixed(1) : "-", "xG")}
                            ${statBox(st.progressive_passes, "Prog Pass")}
                            ${statBox(st.progressive_carries, "Prog Carry")}
                            ${statBox(st.key_passes, "Key Pass")}
                            ${statBox(st.squawka_score, "Squawka")}
                            ${statBox(st.fotmob_rating ? st.fotmob_rating.toFixed(1) : "-", "FotMob")}
                        </div>
                    </div>

                    <!-- REASONS -->
                    <div class="rec-section">
                        <h4>Why Sign This Player</h4>
                        ${b.reasons.map((r) => `<div class="rec-reason">${r}</div>`).join("")}
                    </div>

                    <!-- EYE TEST -->
                    <div class="rec-section">
                        <h4>Scout / Eye Test Assessment</h4>
                        <div class="eye-test-box">${b.eye_test}</div>
                    </div>

                    <!-- DEAL STRUCTURE -->
                    <div class="rec-section">
                        <h4>Proposed Deal Structure</h4>
                        <div class="deal-box">
                            <div class="deal-row"><span class="deal-label">Type</span><span class="deal-val">${deal.type || "N/A"}</span></div>
                            <div class="deal-row"><span class="deal-label">Upfront</span><span class="deal-val">\u20AC${deal.upfront || 0}m</span></div>
                            <div class="deal-row"><span class="deal-label">Installments</span><span class="deal-val">\u20AC${deal.installments || 0}m (${deal.installment_years || 0} yrs)</span></div>
                            <div class="deal-row"><span class="deal-label">Add-ons</span><span class="deal-val">\u20AC${deal.add_ons || 0}m</span></div>
                            <div class="deal-row" style="border-top:1px solid var(--border);margin-top:4px;padding-top:6px"><span class="deal-label"><strong>Total</strong></span><span class="deal-val" style="color:var(--green);font-size:16px"><strong>\u20AC${deal.total || 0}m</strong></span></div>
                            <p style="font-size:12px;color:var(--text-muted);margin-top:8px">${deal.notes || ""}</p>
                        </div>
                    </div>

                    <!-- COMPETING WITH -->
                    <div class="rec-section">
                        <h4>Competes With (Current Squad)</h4>
                        <div class="risk-tags">
                            ${(b.competing_with || []).map((c) => `<span class="strength-tag">${c}</span>`).join("") || "<span style='color:var(--text-muted)'>No direct competition</span>"}
                        </div>
                    </div>

                    <!-- RISK FACTORS -->
                    <div class="rec-section">
                        <h4>Risk Factors</h4>
                        <div class="risk-tags">
                            ${(b.risk_factors || []).map((r) => `<span class="risk-tag">${r}</span>`).join("")}
                        </div>
                    </div>

                    <!-- SUMMARY -->
                    <div class="rec-section">
                        <h4>Recommendation</h4>
                        <p style="font-size:14px;font-weight:600;color:var(--arsenal-gold)">${b.recommendation_summary}</p>
                    </div>
                </div>
            </div>`;
        }
        $("#buyCards").innerHTML = html;
    }

    // ==================== FINANCIAL TAB ====================
    function renderFinancialTab() {
        const fin = DATA.financial_report;
        const bo = fin.budget_overview;
        const wi = fin.wage_impact;
        const am = fin.amortization;
        const psr = fin.psr_compliance;

        // KPIs
        $("#finKpi").innerHTML = `
            ${kpi("\u20AC" + bo.base_budget_m + "m", "Base Budget", "kpi-blue")}
            ${kpi("\u20AC" + bo.sale_revenue_m + "m", "Sale Revenue", "kpi-green")}
            ${kpi("\u20AC" + bo.total_available_m + "m", "Total Available", "kpi-gold")}
            ${kpi("\u20AC" + bo.total_spend_m + "m", "Projected Spend", "kpi-red")}
            ${kpi("\u20AC" + bo.net_spend_m + "m", "Net Spend", bo.net_spend_m > 0 ? "kpi-red" : "kpi-green")}
            ${kpi("\u20AC" + bo.remaining_m + "m", "Remaining", bo.remaining_m > 0 ? "kpi-green" : "kpi-red")}
        `;

        // Wage impact
        let wiHtml = `
            <div class="deal-box">
                <div class="deal-row"><span class="deal-label">Current Wage Bill</span><span class="deal-val">\u00A3${wi.current_wage_bill_m}m/yr</span></div>
                <div class="deal-row"><span class="deal-label">New Wages Added</span><span class="deal-val" style="color:var(--red)">+\u00A3${wi.new_wages_added_m}m/yr</span></div>
                <div class="deal-row"><span class="deal-label">Wages Saved</span><span class="deal-val" style="color:var(--green)">-\u00A3${wi.wages_saved_m}m/yr</span></div>
                <div class="deal-row" style="border-top:1px solid var(--border);padding-top:6px;margin-top:4px">
                    <span class="deal-label"><strong>Projected Wage Bill</strong></span>
                    <span class="deal-val"><strong>\u00A3${wi.projected_wage_bill_m}m/yr</strong></span>
                </div>
                <div class="deal-row"><span class="deal-label">Wage-to-Revenue Ratio</span><span class="deal-val">${wi.projected_wage_ratio}% (max ${wi.max_sustainable_ratio}%)</span></div>
                <div class="deal-row"><span class="deal-label">Wage Headroom</span><span class="deal-val" style="color:var(--green)">\u00A3${wi.wage_headroom_m}m</span></div>
                <div class="deal-row"><span class="deal-label">Status</span><span class="deal-val" style="color:${wi.status === "healthy" ? "var(--green)" : wi.status === "caution" ? "var(--yellow)" : "var(--red)"}">${wi.status.toUpperCase()}</span></div>
            </div>
        `;
        $("#wageImpact").innerHTML = wiHtml;

        // Amortization
        let amHtml = `
            <div class="deal-box" style="margin-bottom:12px">
                <div class="deal-row"><span class="deal-label">Existing Annual Amortization</span><span class="deal-val">\u20AC${am.existing_annual_amortization_m}m</span></div>
                <div class="deal-row"><span class="deal-label">New Amortization</span><span class="deal-val" style="color:var(--red)">+\u20AC${am.new_amortization_m}m</span></div>
                <div class="deal-row"><span class="deal-label">Amortization Removed (Sales)</span><span class="deal-val" style="color:var(--green)">-\u20AC${am.amortization_removed_m}m</span></div>
                <div class="deal-row" style="border-top:1px solid var(--border);padding-top:6px;margin-top:4px">
                    <span class="deal-label"><strong>Total Annual Amortization</strong></span>
                    <span class="deal-val"><strong>\u20AC${am.total_projected_amortization_m}m</strong></span>
                </div>
            </div>
        `;
        if (am.purchases_detail && am.purchases_detail.length) {
            amHtml += `<table class="data-table"><thead><tr><th>Player</th><th>Fee</th><th>Contract</th><th>Annual Amort</th></tr></thead><tbody>`;
            am.purchases_detail.forEach((p) => {
                amHtml += `<tr><td>${p.player}</td><td>\u20AC${p.fee_m}m</td><td>${p.years} yrs</td><td>\u20AC${p.annual_amort_m}m</td></tr>`;
            });
            amHtml += `</tbody></table>`;
        }
        $("#amortization").innerHTML = amHtml;

        // PSR
        let psrHtml = `
            <div class="psr-status ${psr.status === "compliant" ? "psr-compliant" : "psr-atrisk"}">${psr.status.toUpperCase()}</div>
            <div class="deal-box" style="margin-top:12px">
                <div class="deal-row"><span class="deal-label">Annual Revenue</span><span class="deal-val">\u00A3${psr.estimated_annual_revenue_m}m</span></div>
                <div class="deal-row"><span class="deal-label">Annual Costs</span><span class="deal-val">\u00A3${psr.estimated_annual_costs_m}m</span></div>
                <div class="deal-row"><span class="deal-label">Estimated P&L</span><span class="deal-val" style="color:${psr.estimated_annual_profit_m >= 0 ? "var(--green)" : "var(--red)"}">\u00A3${psr.estimated_annual_profit_m}m</span></div>
                <div class="deal-row"><span class="deal-label">PSR Allowable Loss</span><span class="deal-val">\u00A3${psr.psr_allowable_loss_m}m</span></div>
                <div class="deal-row"><span class="deal-label">PSR Headroom</span><span class="deal-val" style="color:var(--green)">\u00A3${psr.psr_headroom_m}m</span></div>
            </div>
            <p style="margin-top:12px;font-size:13px;color:var(--text-secondary)">${psr.notes}</p>
        `;
        $("#psrCheck").innerHTML = psrHtml;
    }

    // ==================== RIVALS TAB ====================
    function renderRivalsTab() {
        const rivals = DATA.rivals || {};
        let html = "";
        for (const [name, info] of Object.entries(rivals)) {
            html += `
            <div class="rival-card">
                <h3>${name}</h3>
                <p style="font-size:12px;color:var(--text-secondary);margin-bottom:12px">PL Position: ${info.pl_position}</p>
                <div class="rival-grid">
                    <div class="rival-section">
                        <h4>Strengths</h4>
                        <ul class="rival-list">${(info.strengths || []).map((s) => `<li>${s}</li>`).join("")}</ul>
                    </div>
                    <div class="rival-section">
                        <h4>Weaknesses</h4>
                        <ul class="rival-list">${(info.weaknesses || []).map((w) => `<li>${w}</li>`).join("")}</ul>
                    </div>
                    <div class="rival-section">
                        <h4>Likely Targets</h4>
                        <ul class="rival-list">${(info.likely_targets || []).map((t) => `<li>${t}</li>`).join("")}</ul>
                    </div>
                    <div class="rival-section">
                        <h4>Sellable Assets</h4>
                        <ul class="rival-list">${(info.sellable_assets || []).map((s) => `<li>${s}</li>`).join("") || "<li>None identified</li>"}</ul>
                    </div>
                </div>
            </div>`;
        }
        $("#rivalCards").innerHTML = html;
    }

    // ==================== STRATEGY TAB ====================
    function renderStrategyTab() {
        const strat = DATA.transfer_plan.transfer_window_strategy || {};
        const phases = [
            { key: "phase_1_early_summer", title: "Phase 1: Early Summer (June)", color: "var(--red)" },
            { key: "phase_2_mid_summer", title: "Phase 2: Mid Summer (July)", color: "var(--yellow)" },
            { key: "phase_3_late_window", title: "Phase 3: Late Window (August)", color: "var(--blue)" },
        ];

        let html = `<div class="card"><h2>Transfer Window Strategy &amp; Timeline</h2><div class="timeline">`;
        for (const phase of phases) {
            const p = strat[phase.key] || {};
            html += `
            <div class="timeline-phase">
                <h3 style="color:${phase.color}">${phase.title}</h3>
                <p class="phase-desc">${p.description || ""}</p>
                <div class="phase-items">
                    ${(p.targets || []).map((t) => `<span class="phase-item item-in">IN: ${t}</span>`).join("")}
                    ${(p.sales || []).map((s) => `<span class="phase-item item-out">OUT: ${s}</span>`).join("")}
                </div>
            </div>`;
        }
        html += `</div>`;
        html += `<div style="margin-top:20px;padding:16px;background:rgba(255,255,255,0.03);border-radius:6px">
            <p style="font-size:14px"><strong>Total Priority Signings:</strong> ${strat.total_priority_signings || 0}</p>
            <p style="font-size:14px"><strong>Total Planned Departures:</strong> ${strat.total_sales_planned || 0}</p>
        </div></div>`;
        $("#strategyTimeline").innerHTML = html;
    }

    // ==================== INTEL TAB ====================
    function renderIntelTab() {
        // Get all targets from original BASELINE (before intel applied)
        let origBaseline;
        try {
            const raw = window.__INITIAL_DATA__;
            origBaseline = raw;
        } catch (e) {
            origBaseline = BASELINE;
        }
        const allTargets = (origBaseline && origBaseline.transfer_plan)
            ? origBaseline.transfer_plan.buy_recommendations || []
            : (BASELINE && BASELINE.transfer_plan ? BASELINE.transfer_plan.buy_recommendations : []);

        // Build target editor rows
        let html = "";
        for (const t of allTargets) {
            const intel = INTEL_UPDATES[t.player] || {};
            const status = intel.status || "available";
            const fee = intel.fee !== undefined ? intel.fee : t.estimated_fee_m;
            const rival = intel.rival || "";
            const notes = intel.notes || "";
            const unavailable = status === "signed_by_rival" || status === "priced_out";

            html += `
            <div class="intel-target-row ${unavailable ? "intel-unavailable" : ""}">
                <div class="intel-player-info">
                    <div class="intel-name">${t.player}${unavailable ? `<span class="intel-rival-badge">${status === "signed_by_rival" ? "SIGNED BY " + (rival || "RIVAL").toUpperCase() : "PRICED OUT"}</span>` : ""}</div>
                    <div class="intel-meta">${t.position} &middot; ${t.age} &middot; ${t.current_club || ""}</div>
                </div>
                <div class="intel-field">
                    <label>Status</label>
                    <select data-player="${t.player}" data-field="status">
                        <option value="available" ${status === "available" ? "selected" : ""}>Available</option>
                        <option value="signed_by_rival" ${status === "signed_by_rival" ? "selected" : ""}>Signed by Rival</option>
                        <option value="priced_out" ${status === "priced_out" ? "selected" : ""}>Priced Out</option>
                    </select>
                </div>
                <div class="intel-field">
                    <label>Rival Club</label>
                    <input type="text" data-player="${t.player}" data-field="rival" value="${rival}" placeholder="e.g. Man City">
                </div>
                <div class="intel-field">
                    <label>Fee (\u20ACm)</label>
                    <input type="number" data-player="${t.player}" data-field="fee" value="${fee}" min="0" max="500" step="1">
                </div>
                <div class="intel-field">
                    <label>Notes</label>
                    <input type="text" data-player="${t.player}" data-field="notes" value="${notes}" placeholder="Scouting note...">
                </div>
            </div>`;
        }
        if (!allTargets.length) html = `<p style="color:var(--text-muted)">No transfer targets loaded.</p>`;
        $("#intelTargetEditor").innerHTML = html;

        // Bind change handlers on all intel fields
        document.querySelectorAll("#intelTargetEditor select, #intelTargetEditor input").forEach(el => {
            el.addEventListener("change", () => {
                const player = el.dataset.player;
                const field = el.dataset.field;
                if (!INTEL_UPDATES[player]) INTEL_UPDATES[player] = {};
                INTEL_UPDATES[player][field] = field === "fee" ? Number(el.value) : el.value;
                saveIntelToStorage();
            });
            // Also save on input for text/number fields
            if (el.tagName === "INPUT") {
                el.addEventListener("input", () => {
                    const player = el.dataset.player;
                    const field = el.dataset.field;
                    if (!INTEL_UPDATES[player]) INTEL_UPDATES[player] = {};
                    INTEL_UPDATES[player][field] = field === "fee" ? Number(el.value) : el.value;
                    saveIntelToStorage();
                });
            }
        });

        // Render intel log
        renderIntelLog();
    }

    function renderIntelLog() {
        if (!INTEL_LOG.length) {
            $("#intelLog").innerHTML = `<p style="color:var(--text-muted);font-size:13px">No intel updates yet. Make changes above and click "Apply Changes".</p>`;
            return;
        }
        let html = "";
        for (const entry of INTEL_LOG.slice().reverse()) {
            const cls = entry.type === "removal" ? "log-removal" : entry.type === "fee" ? "log-fee" : "log-note";
            html += `<div class="intel-log-entry ${cls}">
                <span class="log-time">${entry.time}</span>
                <span class="log-msg">${entry.message}</span>
            </div>`;
        }
        $("#intelLog").innerHTML = html;
    }

    // ==================== HELPERS ====================
    function kpi(value, label, cls) {
        return `<div class="kpi-box ${cls}"><div class="kpi-value">${value}</div><div class="kpi-label">${label}</div></div>`;
    }
    function statBox(val, label) {
        return `<div class="stat-box"><div class="stat-val">${val !== undefined && val !== null ? val : "-"}</div><div class="stat-label">${label}</div></div>`;
    }
    function breakdownBar(label, val) {
        val = val || 0;
        return `<div class="breakdown-bar">
            <div class="bar-label">${label}</div>
            <div style="background:rgba(255,255,255,0.08);border-radius:2px;height:4px;margin:4px 0"><div class="bar-fill" style="width:${val}%;background:${val >= 70 ? "var(--green)" : val >= 40 ? "var(--yellow)" : "var(--red)"}"></div></div>
            <div class="bar-val">${val}</div>
        </div>`;
    }
    function roleLabel(role) {
        const map = { starter: "Starter", rotation: "Rotation", backup: "Backup", youth: "Youth" };
        return map[role] || role;
    }
    function ratingClass(r) {
        return r >= 70 ? "kpi-green" : r >= 50 ? "kpi-yellow" : "kpi-red";
    }
    function posOrder(pos) {
        const order = { GK: 0, CB: 1, RB: 2, LB: 3, DM: 4, CM: 5, AM: 6, LW: 7, RW: 8, ST: 9 };
        return order[pos] ?? 10;
    }

    // ==================== WEBSOCKET BRIDGE ====================
    let WS = null;
    let WS_RECONNECT_TIMER = null;
    const BRIDGE_URL = "ws://localhost:8765";

    function connectBridge() {
        if (WS && WS.readyState === WebSocket.OPEN) return;
        try {
            WS = new WebSocket(BRIDGE_URL);
        } catch (e) {
            updateBridgeStatus(false);
            return;
        }

        WS.onopen = () => {
            updateBridgeStatus(true);
            appendChat("system", "Connected to Claude Code bridge. You can now send messages directly.");
            if (WS_RECONNECT_TIMER) { clearInterval(WS_RECONNECT_TIMER); WS_RECONNECT_TIMER = null; }
        };

        WS.onclose = () => {
            updateBridgeStatus(false);
            if (!WS_RECONNECT_TIMER) {
                WS_RECONNECT_TIMER = setInterval(() => connectBridge(), 5000);
            }
        };

        WS.onerror = () => {
            updateBridgeStatus(false);
        };

        WS.onmessage = (event) => {
            try {
                const msg = JSON.parse(event.data);
                if (msg.type === "ack") {
                    appendChat("system", msg.message);
                } else if (msg.type === "response") {
                    appendChat("claude", msg.message);
                    if (msg.updated_data) {
                        window.__INITIAL_DATA__ = msg.updated_data;
                        BASELINE = JSON.parse(JSON.stringify(msg.updated_data));
                        const budget = Number(slider.value) || 150;
                        DATA = recalcWithBudget(budget);
                        render();
                        appendChat("system", "Dashboard updated with new data from Claude Code.");
                    }
                } else if (msg.type === "status") {
                    appendChat("system", msg.message);
                }
            } catch (e) {
                appendChat("claude", event.data);
            }
        };
    }

    function updateBridgeStatus(connected) {
        const el = document.getElementById("bridgeStatus");
        if (!el) return;
        if (connected) {
            el.textContent = "Connected";
            el.style.background = "rgba(63,185,80,0.15)";
            el.style.color = "var(--green)";
        } else {
            el.textContent = "Disconnected";
            el.style.background = "rgba(248,81,73,0.15)";
            el.style.color = "var(--red)";
        }
    }

    function sendToBridge(message) {
        const payload = {
            type: "intel_update",
            message: message,
            intel: INTEL_UPDATES,
            intel_log: INTEL_LOG,
            budget: Number(slider.value) || 150,
            timestamp: new Date().toISOString(),
            current_buy_recs: DATA ? (DATA.transfer_plan.buy_recommendations || []).map(b => ({
                player: b.player, position: b.position, score: b.priority_score, fee: b.estimated_fee_m,
            })) : [],
            current_sell_recs: DATA ? (DATA.transfer_plan.sell_recommendations || []).map(s => ({
                player: s.player, fee: s.projected_fee_m, urgency: s.urgency,
            })) : [],
        };

        if (WS && WS.readyState === WebSocket.OPEN) {
            WS.send(JSON.stringify(payload));
            appendChat("user", message);
        } else {
            appendChat("system", "Bridge not connected. Start the bridge server: python3 bridge.py");
            connectBridge();
        }
    }

    function appendChat(role, text) {
        const container = document.getElementById("chatMessages");
        if (!container) return;
        const div = document.createElement("div");
        div.style.marginBottom = "8px";
        div.style.padding = "6px 10px";
        div.style.borderRadius = "4px";

        if (role === "user") {
            div.style.background = "rgba(156,130,74,0.15)";
            div.style.borderLeft = "3px solid var(--arsenal-gold)";
            div.innerHTML = `<span style="font-size:10px;color:var(--arsenal-gold);text-transform:uppercase;font-weight:700">You</span><br>${escapeHtml(text)}`;
        } else if (role === "claude") {
            div.style.background = "rgba(63,185,80,0.1)";
            div.style.borderLeft = "3px solid var(--green)";
            div.innerHTML = `<span style="font-size:10px;color:var(--green);text-transform:uppercase;font-weight:700">Claude Code</span><br>${escapeHtml(text)}`;
        } else {
            div.style.background = "rgba(88,166,255,0.08)";
            div.style.color = "var(--text-muted)";
            div.style.fontStyle = "italic";
            div.style.fontSize = "12px";
            div.textContent = text;
        }

        container.appendChild(div);
        container.scrollTop = container.scrollHeight;

        try {
            const history = JSON.parse(localStorage.getItem("arsenal_chat") || "[]");
            history.push({ role, text, time: Date.now() });
            if (history.length > 50) history.splice(0, history.length - 50);
            localStorage.setItem("arsenal_chat", JSON.stringify(history));
        } catch (e) { /* ignore */ }
    }

    function loadChatHistory() {
        try {
            const history = JSON.parse(localStorage.getItem("arsenal_chat") || "[]");
            for (const entry of history) {
                appendChat(entry.role, entry.text);
            }
        } catch (e) { /* ignore */ }
    }

    function escapeHtml(str) {
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }

    // ---- COMMENTS PERSISTENCE ----
    function loadCommentsFromStorage() {
        try {
            const saved = localStorage.getItem("arsenal_comments");
            if (saved) {
                const el = document.getElementById("userComments");
                if (el) el.value = saved;
            }
        } catch (e) { /* ignore */ }
    }
    function saveCommentsToStorage() {
        try {
            const el = document.getElementById("userComments");
            if (el) localStorage.setItem("arsenal_comments", el.value);
        } catch (e) { /* ignore */ }
    }

    // ---- EXPORT GENERATOR ----
    function generateExport() {
        const lines = [];
        const ts = new Date().toLocaleString();
        lines.push("=== ARSENAL TRANSFER WAR ROOM - INTEL EXPORT ===");
        lines.push(`Generated: ${ts}`);
        lines.push(`Current Budget: \u20AC${slider.value}m`);
        lines.push("");

        // Intel updates
        const hasUpdates = Object.keys(INTEL_UPDATES).length > 0;
        if (hasUpdates) {
            lines.push("--- TARGET STATUS CHANGES ---");
            for (const [player, intel] of Object.entries(INTEL_UPDATES)) {
                const parts = [`  ${player}:`];
                if (intel.status && intel.status !== "available") {
                    if (intel.status === "signed_by_rival") {
                        parts.push(`SIGNED BY ${(intel.rival || "unknown rival").toUpperCase()}`);
                    } else if (intel.status === "priced_out") {
                        parts.push("PRICED OUT");
                    }
                }
                if (intel.fee !== undefined) parts.push(`Fee: \u20AC${intel.fee}m`);
                if (intel.notes) parts.push(`Note: "${intel.notes}"`);
                lines.push(parts.join(" | "));
            }
            lines.push("");
        }

        // Current plan snapshot after intel applied
        if (DATA && DATA.transfer_plan) {
            lines.push("--- CURRENT BUY RECOMMENDATIONS (after intel applied) ---");
            const buys = DATA.transfer_plan.buy_recommendations || [];
            if (buys.length) {
                buys.forEach((b, i) => {
                    lines.push(`  ${i + 1}. ${b.player} (${b.position}, ${b.age}) - Score: ${b.priority_score}/100 - Fee: \u20AC${b.estimated_fee_m}m`);
                });
            } else {
                lines.push("  (no remaining targets)");
            }
            lines.push("");

            lines.push("--- SELL RECOMMENDATIONS ---");
            const sells = DATA.transfer_plan.sell_recommendations || [];
            sells.forEach((s, i) => {
                lines.push(`  ${i + 1}. ${s.player} - Projected fee: \u20AC${s.projected_fee_m}m - Urgency: ${s.urgency}`);
            });
            lines.push("");
        }

        // Financial snapshot
        if (DATA && DATA.financial_report) {
            const bo = DATA.financial_report.budget_overview;
            lines.push("--- FINANCIAL SNAPSHOT ---");
            lines.push(`  Budget: \u20AC${bo.base_budget_m}m | Sales: \u20AC${bo.sale_revenue_m}m | Available: \u20AC${bo.total_available_m}m`);
            lines.push(`  Spend: \u20AC${bo.total_spend_m}m | Remaining: \u20AC${bo.remaining_m}m | Net: \u20AC${bo.net_spend_m}m`);
            lines.push("");
        }

        // User comments
        const comments = (document.getElementById("userComments") || {}).value || "";
        if (comments.trim()) {
            lines.push("--- MY COMMENTS / REQUESTS ---");
            lines.push(comments.trim());
            lines.push("");
        }

        lines.push("=== END EXPORT ===");
        lines.push("Paste this into your Claude Code session for processing.");
        return lines.join("\n");
    }

    // ---- INTEL BUTTONS ----
    document.addEventListener("DOMContentLoaded", () => {
        const applyBtn = document.getElementById("intelApplyBtn");
        const resetBtn = document.getElementById("intelResetBtn");
        const exportBtn = document.getElementById("exportBtn");
        const copyBtn = document.getElementById("copyExportBtn");
        const commentsBox = document.getElementById("userComments");

        if (applyBtn) {
            applyBtn.addEventListener("click", () => {
                // Log the changes
                const now = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
                for (const [player, intel] of Object.entries(INTEL_UPDATES)) {
                    if (intel.status === "signed_by_rival") {
                        INTEL_LOG.push({ time: now, type: "removal", message: `${player} marked as SIGNED BY ${(intel.rival || "rival").toUpperCase()} \u2014 removed from recommendations` });
                    } else if (intel.status === "priced_out") {
                        INTEL_LOG.push({ time: now, type: "removal", message: `${player} marked as PRICED OUT \u2014 removed from recommendations` });
                    }
                    if (intel.fee !== undefined) {
                        INTEL_LOG.push({ time: now, type: "fee", message: `${player} fee updated to \u20AC${intel.fee}m` });
                    }
                    if (intel.notes) {
                        INTEL_LOG.push({ time: now, type: "note", message: `${player}: "${intel.notes}"` });
                    }
                }
                saveIntelToStorage();

                // Reset BASELINE to original data and re-apply intel
                BASELINE = JSON.parse(JSON.stringify(window.__INITIAL_DATA__));
                applyIntelToBaseline();
            });
        }
        if (resetBtn) {
            resetBtn.addEventListener("click", () => {
                INTEL_UPDATES = {};
                INTEL_LOG = [];
                localStorage.removeItem("arsenal_intel");
                BASELINE = JSON.parse(JSON.stringify(window.__INITIAL_DATA__));
                const budget = Number(slider.value) || 150;
                DATA = recalcWithBudget(budget);
                render();
            });
        }

        // Export button
        if (exportBtn) {
            exportBtn.addEventListener("click", () => {
                const text = generateExport();
                const outputDiv = document.getElementById("exportOutput");
                const outputPre = document.getElementById("exportText");
                if (outputDiv && outputPre) {
                    outputPre.textContent = text;
                    outputDiv.style.display = "block";
                    outputDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
                }
            });
        }

        // Copy to clipboard button
        if (copyBtn) {
            copyBtn.addEventListener("click", () => {
                // Generate fresh export if not already displayed
                const outputPre = document.getElementById("exportText");
                let text = outputPre ? outputPre.textContent : "";
                if (!text) {
                    text = generateExport();
                    const outputDiv = document.getElementById("exportOutput");
                    if (outputDiv && outputPre) {
                        outputPre.textContent = text;
                        outputDiv.style.display = "block";
                    }
                }
                navigator.clipboard.writeText(text).then(() => {
                    const orig = copyBtn.textContent;
                    copyBtn.textContent = "Copied!";
                    copyBtn.style.background = "var(--green)";
                    setTimeout(() => {
                        copyBtn.textContent = orig;
                        copyBtn.style.background = "var(--blue)";
                    }, 2000);
                }).catch(() => {
                    // Fallback: select the pre text
                    const range = document.createRange();
                    range.selectNodeContents(outputPre);
                    const sel = window.getSelection();
                    sel.removeAllRanges();
                    sel.addRange(range);
                });
            });
        }

        // Auto-save comments on input
        if (commentsBox) {
            commentsBox.addEventListener("input", saveCommentsToStorage);
        }

        // Load saved comments
        loadCommentsFromStorage();

        // ---- CHAT / BRIDGE ----
        const chatSendBtn = document.getElementById("chatSendBtn");
        const chatInput = document.getElementById("chatInput");

        if (chatSendBtn && chatInput) {
            chatSendBtn.addEventListener("click", () => {
                const msg = chatInput.value.trim();
                if (!msg) return;
                sendToBridge(msg);
                chatInput.value = "";
            });
            chatInput.addEventListener("keydown", (e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    chatSendBtn.click();
                }
            });
        }

        // Quick message buttons
        document.querySelectorAll(".quick-msg-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const msg = btn.dataset.msg;
                if (msg) sendToBridge(msg);
            });
        });

        // Load chat history and connect to bridge
        loadChatHistory();
        connectBridge();
    });

    // ---- INIT ----
    loadIntelFromStorage();
    loadData(150);

    // After initial load, apply any saved intel
    setTimeout(() => {
        if (Object.keys(INTEL_UPDATES).length > 0 && BASELINE) {
            const origBaseline = JSON.parse(JSON.stringify(window.__INITIAL_DATA__ || BASELINE));
            BASELINE = origBaseline;
            applyIntelToBaseline();
        }
    }, 100);
})();
