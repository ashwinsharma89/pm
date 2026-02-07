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
    async function loadData(budget) {
        const loader = $("#loadingIndicator");
        loader.classList.remove("hidden");
        try {
            const res = await fetch(`/api/plan?budget=${budget || 150}`);
            DATA = await res.json();
            render();
        } catch (err) {
            loader.innerHTML = `<p style="color:var(--red)">Error loading data: ${err.message}</p>`;
        }
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

    // ---- INIT ----
    loadData(150);
})();
