# Arsenal FC - Transfer War Room 2026

Enterprise-grade transfer planning application for Arsenal FC's 2026 summer transfer window.

## Overview

A full-stack web application that combines squad analysis, transfer recommendations, financial modeling, and rival intelligence into a unified sporting director console. All data is sourced from FBref, Squawka, FotMob, Transfermarkt, and scout reports as of February 2026.

## Features

- **Squad Analysis Engine** - Position-by-position depth scoring, performance gap detection (xG underperformance, progressive actions), age profile sustainability, contract risk matrix, set-piece vulnerability assessment
- **Transfer Recommendation Engine** - Weighted scoring system for buy/sell decisions factoring squad need, player quality, financial value, age profile, and deal feasibility
- **Financial Modeling** - Budget tracking, wage bill impact analysis, transfer amortization scheduling, Premier League PSR compliance checking, deal structure optimization
- **Rival Intelligence** - Competitor squad analysis, overlapping target identification, market positioning
- **Interactive Dashboard** - 7-tab enterprise UI with KPI cards, positional heatmap, player modals, score breakdowns, and strategy timeline

## Architecture

```
app/
├── data/
│   └── squad_db.py          # Squad database with 25+ players and 8 transfer targets
├── engine/
│   ├── squad_analyzer.py    # Deficiency detection and squad rating
│   ├── transfer_recommender.py  # Buy/sell recommendation engine
│   └── financial_model.py   # Budget, wages, amortization, PSR
├── static/
│   ├── css/style.css        # Arsenal-themed dark mode dashboard
│   └── js/app.js            # Frontend rendering and interactivity
├── templates/
│   └── index.html           # Dashboard HTML
└── main.py                  # Flask application and API routes
```

## Quick Start

```bash
pip install -r requirements.txt
python app/main.py
```

Then open `http://localhost:5000` in your browser.

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Dashboard UI |
| `GET /api/plan?budget=150` | Full transfer plan (adjustable budget in EUR millions) |
| `GET /api/squad` | Current Arsenal squad data |
| `GET /api/targets` | Transfer target database |
| `GET /api/squad-report` | Squad analysis report |
| `GET /api/financial?budget=150` | Financial model report |
| `GET /api/rivals` | Rival intelligence |
| `GET /api/deal-check?player=X&fee=Y&wage=Z` | Deal feasibility checker |

## Data Sources

- [FBref](https://fbref.com/en/squads/18bb7c10/Arsenal-Stats) - Advanced statistics
- [Squawka](https://www.squawka.com/en/stats/clubs/arsenal/) - Performance ratings
- [FotMob](https://www.fotmob.com) - Match ratings
- [Transfermarkt](https://www.transfermarkt.us/fc-arsenal/transfers/verein/11) - Market values
- Transfer news from Fabrizio Romano, David Ornstein, Sky Sports, TeamTalk
