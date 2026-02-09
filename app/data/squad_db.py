"""
Arsenal Transfer Planner - Squad Database
==========================================
Complete squad data for Arsenal FC 2025-26 season.
All stats sourced from FBref, ESPN, Squawka, Transfermarkt, Capology as of Feb 2026.

Data includes: appearances, goals, assists, minutes, xG, xA, progressive actions,
defensive actions, wages, market value, contract expiry, and scouting notes.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PlayerStats:
    appearances: int = 0
    goals: int = 0
    assists: int = 0
    minutes: int = 0
    # Advanced metrics (per 90 or season totals)
    xg: float = 0.0
    xa: float = 0.0
    progressive_passes: int = 0
    progressive_carries: int = 0
    key_passes: int = 0
    tackles_won: int = 0
    interceptions: int = 0
    aerials_won: int = 0
    dribbles_completed: int = 0
    shot_accuracy_pct: float = 0.0
    pass_completion_pct: float = 0.0
    clean_sheets: int = 0  # GK / defenders
    saves: int = 0  # GK
    # Squawka / scout rating (0-100)
    squawka_score: float = 0.0
    fotmob_rating: float = 0.0


@dataclass
class Player:
    name: str
    age: int
    position: str  # GK, CB, LB, RB, DM, CM, AM, LW, RW, ST
    nationality: str
    squad_number: Optional[int] = None
    market_value_m: float = 0.0  # in millions EUR
    wage_weekly_k: float = 0.0  # in thousands GBP
    contract_expiry: str = ""  # YYYY-MM-DD
    stats: PlayerStats = field(default_factory=PlayerStats)
    status: str = "available"  # available, injured, loaned_out, transfer_listed
    loan_club: str = ""
    eye_test_notes: str = ""
    strengths: list = field(default_factory=list)
    weaknesses: list = field(default_factory=list)
    role_in_squad: str = ""  # starter, rotation, backup, youth


def build_arsenal_squad() -> list[Player]:
    """Build the complete Arsenal 2025-26 squad with real stats and scouting data."""

    squad = []

    # ==================== GOALKEEPERS ====================

    squad.append(Player(
        name="David Raya",
        age=29,
        position="GK",
        nationality="Spain",
        squad_number=1,
        market_value_m=35.0,
        wage_weekly_k=150.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=24, goals=0, assists=0, minutes=2160,
            clean_sheets=11, saves=62,
            pass_completion_pct=87.5,
            squawka_score=60.0, fotmob_rating=7.1
        ),
        status="available",
        eye_test_notes="Elite distribution, sweeper-keeper style. Occasionally shaky on crosses. "
                       "Commands area well. Shot-stopping above average but not world-class.",
        strengths=["Distribution", "Sweeper-keeper", "Penalty saves", "Playing out from back"],
        weaknesses=["Aerial command in crowded box", "Occasional lapses on crosses"],
        role_in_squad="starter"
    ))

    squad.append(Player(
        name="Kepa Arrizabalaga",
        age=31,
        position="GK",
        nationality="Spain",
        squad_number=22,
        market_value_m=8.0,
        wage_weekly_k=80.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=8, goals=0, assists=0, minutes=720,
            clean_sheets=4, saves=22,
            pass_completion_pct=84.0,
            squawka_score=52.0, fotmob_rating=6.8
        ),
        status="available",
        eye_test_notes="Solid backup GK. Good with feet. Reliable cup keeper. "
                       "Not elite shot-stopper but adequate depth.",
        strengths=["Ball-playing", "Experience", "Cup competition specialist"],
        weaknesses=["Shot-stopping ceiling lower than elite", "High wages for backup"],
        role_in_squad="rotation"
    ))

    # ==================== CENTRE-BACKS ====================

    squad.append(Player(
        name="William Saliba",
        age=24,
        position="CB",
        nationality="France",
        squad_number=2,
        market_value_m=90.0,
        wage_weekly_k=200.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=23, goals=1, assists=1, minutes=2070,
            progressive_passes=48, progressive_carries=22,
            tackles_won=32, interceptions=28, aerials_won=45,
            pass_completion_pct=92.1,
            squawka_score=74.0, fotmob_rating=7.4
        ),
        status="available",
        eye_test_notes="World-class centre-back. Exceptional reading of the game, "
                       "elite recovery pace. Ball-playing ability top-tier. "
                       "France international and long-term pillar.",
        strengths=["Recovery pace", "Ball progression", "Aerial dominance", "1v1 defending", "Reading the game"],
        weaknesses=["Occasionally over-commits in high press"],
        role_in_squad="starter"
    ))

    squad.append(Player(
        name="Gabriel Magalhaes",
        age=28,
        position="CB",
        nationality="Brazil",
        squad_number=6,
        market_value_m=70.0,
        wage_weekly_k=190.0,
        contract_expiry="2030-06-30",
        stats=PlayerStats(
            appearances=18, goals=3, assists=0, minutes=1620,
            progressive_passes=32, progressive_carries=12,
            tackles_won=24, interceptions=22, aerials_won=52,
            pass_completion_pct=89.5,
            squawka_score=70.0, fotmob_rating=7.2
        ),
        status="available",
        eye_test_notes="Physical monster. Set-piece threat with 3 goals from headers. "
                       "Excellent aerial duel winner. Occasionally ball-watches "
                       "during transitions. Strong leader.",
        strengths=["Aerial dominance", "Set-piece threat", "Physical presence", "Leadership"],
        weaknesses=["Ball-watching in transitions", "Progressive passing under pressure", "Pace against quick forwards"],
        role_in_squad="starter"
    ))

    squad.append(Player(
        name="Cristhian Mosquera",
        age=20,
        position="CB",
        nationality="Spain",
        squad_number=25,
        market_value_m=25.0,
        wage_weekly_k=60.0,
        contract_expiry="2030-06-30",
        stats=PlayerStats(
            appearances=12, goals=0, assists=0, minutes=780,
            progressive_passes=18, progressive_carries=8,
            tackles_won=16, interceptions=14, aerials_won=18,
            pass_completion_pct=90.2,
            squawka_score=62.0, fotmob_rating=6.9
        ),
        status="available",
        eye_test_notes="Young, composed centre-back signed from Valencia. Excellent ball-playing "
                       "for his age. Needs physical development but reads the game well. "
                       "Long-term Saliba partner prospect.",
        strengths=["Ball progression", "Composure", "Youth and ceiling", "Tactical intelligence"],
        weaknesses=["Physical development needed", "Limited PL experience", "Aerial duels vs strong strikers"],
        role_in_squad="rotation"
    ))

    # ==================== FULL-BACKS ====================

    squad.append(Player(
        name="Jurrien Timber",
        age=24,
        position="RB",
        nationality="Netherlands",
        squad_number=12,
        market_value_m=55.0,
        wage_weekly_k=140.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=23, goals=2, assists=3, minutes=1980,
            progressive_passes=42, progressive_carries=55,
            key_passes=18, tackles_won=30, interceptions=20,
            dribbles_completed=22,
            pass_completion_pct=88.4,
            squawka_score=78.0, fotmob_rating=7.5
        ),
        status="available",
        eye_test_notes="Highest Squawka score for any full-back this season. "
                       "Exceptional inverting full-back who transitions into midfield. "
                       "Tactically elite. Strong going forward. First-choice RB.",
        strengths=["Tactical versatility", "Ball progression", "Inverting into midfield",
                   "1v1 defending", "Goal contributions"],
        weaknesses=["Can be caught high up against quick counters"],
        role_in_squad="starter"
    ))

    squad.append(Player(
        name="Ben White",
        age=28,
        position="RB",
        nationality="England",
        squad_number=4,
        market_value_m=30.0,
        wage_weekly_k=120.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=12, goals=0, assists=1, minutes=840,
            progressive_passes=22, progressive_carries=15,
            tackles_won=14, interceptions=10,
            pass_completion_pct=89.8,
            squawka_score=55.0, fotmob_rating=6.7
        ),
        status="available",
        eye_test_notes="Frustrated with lack of minutes behind Timber. Only 12 apps this season. "
                       "Still a quality defender with good passing range. Can play CB. "
                       "Reports suggest unhappy and open to exit.",
        strengths=["Passing range", "Tactical intelligence", "Can play CB/RB", "Composure"],
        weaknesses=["Diminished minutes", "Morale concerns", "Not as dynamic as Timber going forward"],
        role_in_squad="rotation"
    ))

    squad.append(Player(
        name="Riccardo Calafiori",
        age=23,
        position="LB",
        nationality="Italy",
        squad_number=33,
        market_value_m=55.0,
        wage_weekly_k=130.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=20, goals=1, assists=2, minutes=1540,
            progressive_passes=38, progressive_carries=48,
            key_passes=14, tackles_won=22, interceptions=18,
            dribbles_completed=16,
            pass_completion_pct=87.8,
            squawka_score=66.0, fotmob_rating=7.1
        ),
        status="available",
        eye_test_notes="Aggressive overlapping full-back with excellent ball-carrying. "
                       "Italy international. Strong in build-up. Can also play CB. "
                       "First-choice LB when fit.",
        strengths=["Ball-carrying", "Overlap/underlap runs", "Build-up play", "Versatility CB/LB"],
        weaknesses=["Defensive positioning when caught high", "Injury niggles"],
        role_in_squad="starter"
    ))

    squad.append(Player(
        name="Piero Hincapie",
        age=23,
        position="LB",
        nationality="Ecuador",
        squad_number=15,
        market_value_m=35.0,
        wage_weekly_k=80.0,
        contract_expiry="2026-06-30",  # loan expires
        stats=PlayerStats(
            appearances=16, goals=0, assists=1, minutes=1080,
            progressive_passes=28, progressive_carries=20,
            tackles_won=18, interceptions=14, aerials_won=16,
            pass_completion_pct=89.0,
            squawka_score=58.0, fotmob_rating=6.8
        ),
        status="available",
        loan_club="Bayer Leverkusen (loan)",
        eye_test_notes="Leverkusen loanee. Solid defensive full-back/CB hybrid. "
                       "Good in a back-three. Less dynamic going forward than Calafiori. "
                       "Option to buy reportedly £30m.",
        strengths=["Defensive solidity", "Versatility LB/CB", "Left-footed", "Physical"],
        weaknesses=["Limited attacking output", "Not permanent yet - loan decision needed"],
        role_in_squad="rotation"
    ))

    squad.append(Player(
        name="Myles Lewis-Skelly",
        age=18,
        position="LB",
        nationality="England",
        squad_number=49,
        market_value_m=15.0,
        wage_weekly_k=30.0,
        contract_expiry="2030-06-30",
        stats=PlayerStats(
            appearances=14, goals=0, assists=2, minutes=780,
            progressive_passes=22, progressive_carries=30,
            key_passes=8, tackles_won=10, interceptions=8,
            dribbles_completed=14,
            pass_completion_pct=85.5,
            squawka_score=60.0, fotmob_rating=6.9
        ),
        status="available",
        eye_test_notes="Exceptional academy talent. Originally a midfielder, now deployed at LB. "
                       "Arteta plans to transition him back to midfield long-term. "
                       "Outstanding ball-carrier. Needs defensive refinement.",
        strengths=["Ball-carrying", "Progressive actions", "Youth potential", "Versatility"],
        weaknesses=["Defensive positioning", "Physical development", "Decision-making under pressure"],
        role_in_squad="rotation"
    ))

    # ==================== MIDFIELDERS ====================

    squad.append(Player(
        name="Martin Odegaard",
        age=27,
        position="AM",
        nationality="Norway",
        squad_number=8,
        market_value_m=100.0,
        wage_weekly_k=250.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=18, goals=2, assists=4, minutes=1440,
            xg=3.2, xa=5.8,
            progressive_passes=68, progressive_carries=35,
            key_passes=42,
            dribbles_completed=18,
            pass_completion_pct=87.2,
            squawka_score=72.0, fotmob_rating=7.4
        ),
        status="available",
        eye_test_notes="Captain and creative heartbeat. 8 through balls in early season. "
                       "Slightly injury-disrupted (missed 5 games). When fit, arguably "
                       "best #10 in the PL. Drives tempo and final-third creativity.",
        strengths=["Creativity", "Through balls", "Press resistance", "Leadership",
                   "Final third passing"],
        weaknesses=["Injury concerns (ankle)", "Defensive contribution in deep block situations"],
        role_in_squad="starter"
    ))

    squad.append(Player(
        name="Declan Rice",
        age=27,
        position="CM",
        nationality="England",
        squad_number=41,
        market_value_m=110.0,
        wage_weekly_k=250.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=23, goals=4, assists=3, minutes=2070,
            xg=3.0, xa=2.5,
            progressive_passes=55, progressive_carries=145,
            key_passes=22,
            tackles_won=38, interceptions=26,
            dribbles_completed=28,
            pass_completion_pct=89.0,
            squawka_score=75.0, fotmob_rating=7.5
        ),
        status="available",
        eye_test_notes="Engine of the team. League-leading ball carrier with 145 carries, "
                       "65 progressive. Wins possession 36+ times. Box-to-box machine. "
                       "4 goals and 3 assists show his evolution. Indispensable.",
        strengths=["Ball-carrying", "Press resistance", "Goal contributions from midfield",
                   "Winning possession", "Engine/fitness"],
        weaknesses=["Occasional over-ambitious forward runs leaving gaps"],
        role_in_squad="starter"
    ))

    squad.append(Player(
        name="Martin Zubimendi",
        age=27,
        position="DM",
        nationality="Spain",
        squad_number=36,
        market_value_m=65.0,
        wage_weekly_k=180.0,
        contract_expiry="2030-06-30",
        stats=PlayerStats(
            appearances=24, goals=4, assists=2, minutes=2000,
            xg=2.5, xa=2.0,
            progressive_passes=72, progressive_carries=40,
            key_passes=28,
            tackles_won=34, interceptions=32,
            pass_completion_pct=91.5,
            squawka_score=73.0, fotmob_rating=7.3
        ),
        status="available",
        eye_test_notes="The deep-lying controller Arsenal desperately needed. Elite tempo setter. "
                       "91.5% pass completion from the #6 role. Reads the game exceptionally. "
                       "Surprise goal contributions (4 goals). Transformative signing.",
        strengths=["Tempo control", "Progressive passing", "Positional intelligence",
                   "Interceptions", "Press resistance"],
        weaknesses=["Not the most physical in duels", "Pace in recovery"],
        role_in_squad="starter"
    ))

    squad.append(Player(
        name="Mikel Merino",
        age=29,
        position="CM",
        nationality="Spain",
        squad_number=23,
        market_value_m=40.0,
        wage_weekly_k=140.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=21, goals=4, assists=3, minutes=1560,
            xg=2.8, xa=2.5,
            progressive_passes=48, progressive_carries=32,
            key_passes=20,
            tackles_won=22, interceptions=18, aerials_won=28,
            pass_completion_pct=86.5,
            squawka_score=68.0, fotmob_rating=7.2
        ),
        status="available",
        eye_test_notes="Excellent box-to-box option. 8 through balls early season alongside Odegaard. "
                       "Physical presence and aerial ability add a different dimension. "
                       "Smart rotation option but not guaranteed starter.",
        strengths=["Aerial ability", "Late runs into box", "Through balls",
                   "Physical presence", "Versatility"],
        weaknesses=["Not as press-resistant as Odegaard/Zubimendi", "Turning 30"],
        role_in_squad="rotation"
    ))

    squad.append(Player(
        name="Eberechi Eze",
        age=27,
        position="AM",
        nationality="England",
        squad_number=20,
        market_value_m=55.0,
        wage_weekly_k=150.0,
        contract_expiry="2030-06-30",
        stats=PlayerStats(
            appearances=19, goals=4, assists=2, minutes=1200,
            xg=3.5, xa=2.0,
            progressive_passes=30, progressive_carries=45,
            key_passes=22,
            dribbles_completed=28,
            pass_completion_pct=84.0,
            squawka_score=65.0, fotmob_rating=7.0
        ),
        status="available",
        eye_test_notes="Signed from Crystal Palace. Silky dribbler with flair. "
                       "Can play AM/LW. Excellent in tight spaces. "
                       "Not yet fully integrated but flashes of brilliance.",
        strengths=["Dribbling", "Ball-carrying", "Flair in tight spaces",
                   "Set-piece delivery", "Versatility AM/LW"],
        weaknesses=["Consistency in big matches", "Defensive work rate", "Decision-making final third"],
        role_in_squad="rotation"
    ))

    squad.append(Player(
        name="Ethan Nwaneri",
        age=18,
        position="AM",
        nationality="England",
        squad_number=53,
        market_value_m=20.0,
        wage_weekly_k=35.0,
        contract_expiry="2030-06-30",
        stats=PlayerStats(
            appearances=14, goals=2, assists=2, minutes=640,
            xg=1.8, xa=1.5,
            progressive_passes=18, progressive_carries=20,
            key_passes=12,
            dribbles_completed=10,
            pass_completion_pct=82.0,
            squawka_score=58.0, fotmob_rating=6.8
        ),
        status="available",
        eye_test_notes="Generational English talent. Record-breaking youngest PL player. "
                       "Outstanding creativity and shooting for his age. "
                       "Needs more PL minutes but ceiling is immense.",
        strengths=["Creativity", "Shooting technique", "Youth ceiling", "Intelligence"],
        weaknesses=["Physical development", "Senior experience", "Defensive intensity"],
        role_in_squad="youth"
    ))

    squad.append(Player(
        name="Christian Norgaard",
        age=31,
        position="DM",
        nationality="Denmark",
        squad_number=16,
        market_value_m=8.0,
        wage_weekly_k=60.0,
        contract_expiry="2027-06-30",
        stats=PlayerStats(
            appearances=10, goals=0, assists=0, minutes=520,
            progressive_passes=12, progressive_carries=8,
            tackles_won=14, interceptions=12, aerials_won=16,
            pass_completion_pct=85.0,
            squawka_score=48.0, fotmob_rating=6.4
        ),
        status="available",
        eye_test_notes="Experienced DM signed as Jorginho leadership replacement. "
                       "Physical presence and set-piece defending. "
                       "Not a long-term solution but adds squad depth and dressing room value.",
        strengths=["Leadership", "Aerial ability", "Experience", "Set-piece defending"],
        weaknesses=["Limited on the ball", "Aging", "Not CL-quality starter"],
        role_in_squad="backup"
    ))

    # ==================== WINGERS / FORWARDS ====================

    squad.append(Player(
        name="Bukayo Saka",
        age=24,
        position="RW",
        nationality="England",
        squad_number=7,
        market_value_m=130.0,
        wage_weekly_k=300.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=22, goals=4, assists=3, minutes=1549,
            xg=5.0, xa=4.5,
            progressive_passes=45, progressive_carries=60,
            key_passes=35,
            dribbles_completed=10,
            pass_completion_pct=82.0,
            squawka_score=72.0, fotmob_rating=7.54
        ),
        status="available",
        eye_test_notes="Franchise player. 24 dribble attempts, highest at the club. "
                       "Highest FotMob rating 7.54. Creates and scores consistently. "
                       "Best 1v1 player in the squad. Indispensable.",
        strengths=["1v1 dribbling", "Creativity", "Goal contributions", "Big-game player",
                   "Work rate", "Versatility RW/LW"],
        weaknesses=["Occasional over-reliance on left foot", "Workload management needed"],
        role_in_squad="starter"
    ))

    squad.append(Player(
        name="Noni Madueke",
        age=23,
        position="RW",
        nationality="England",
        squad_number=11,
        market_value_m=50.0,
        wage_weekly_k=120.0,
        contract_expiry="2030-06-30",
        stats=PlayerStats(
            appearances=20, goals=3, assists=2, minutes=1100,
            xg=3.2, xa=2.0,
            progressive_passes=18, progressive_carries=35,
            key_passes=14,
            dribbles_completed=20,
            pass_completion_pct=79.5,
            squawka_score=62.0, fotmob_rating=6.9
        ),
        status="available",
        eye_test_notes="Pacy, direct winger signed from Chelsea. Good depth for Saka. "
                       "Can play both wings. Strong dribbler. Needs to improve end product "
                       "consistency. Good rotation option in a packed schedule.",
        strengths=["Pace", "Directness", "Dribbling", "Can play both flanks"],
        weaknesses=["End product consistency", "Decision-making in final third", "Defensive contribution"],
        role_in_squad="rotation"
    ))

    squad.append(Player(
        name="Gabriel Martinelli",
        age=24,
        position="LW",
        nationality="Brazil",
        squad_number=10,
        market_value_m=50.0,
        wage_weekly_k=130.0,
        contract_expiry="2027-06-30",
        stats=PlayerStats(
            appearances=19, goals=3, assists=2, minutes=1080,
            xg=4.0, xa=1.8,
            progressive_passes=12, progressive_carries=32,
            key_passes=10,
            dribbles_completed=14,
            pass_completion_pct=78.0,
            squawka_score=56.0, fotmob_rating=6.7
        ),
        status="available",
        eye_test_notes="Has plateaued since his 15-goal 2022/23 season. Inconsistent end product. "
                       "High energy and pressing are assets, but final-third quality lacking. "
                       "Reports suggest Arsenal are open to selling for ~50m to fund an upgrade.",
        strengths=["High pressing intensity", "Pace", "Energy", "Direct running"],
        weaknesses=["End product regression", "Decision-making", "Has hit ceiling",
                   "Inconsistent against deep blocks"],
        role_in_squad="rotation"
    ))

    squad.append(Player(
        name="Leandro Trossard",
        age=31,
        position="LW",
        nationality="Belgium",
        squad_number=19,
        market_value_m=20.0,
        wage_weekly_k=120.0,
        contract_expiry="2026-06-30",
        stats=PlayerStats(
            appearances=20, goals=5, assists=4, minutes=1200,
            xg=4.2, xa=3.5,
            progressive_passes=22, progressive_carries=25,
            key_passes=18,
            dribbles_completed=8,
            pass_completion_pct=83.0,
            squawka_score=64.0, fotmob_rating=7.0
        ),
        status="available",
        eye_test_notes="Belgium veteran. Leads goal involvements (5G+4A). Clutch performer. "
                       "Contract expires June 2026 - will leave for free unless renewed. "
                       "31 years old, Saudi interest reported. Excellent squad player "
                       "but not the upgrade needed for title/CL push.",
        strengths=["Clutch goals", "Versatility LW/RW/AM", "Experience", "Finishing"],
        weaknesses=["Contract expiring", "Age 31", "Pace declining", "Not a starter-level upgrade"],
        role_in_squad="rotation"
    ))

    # ==================== STRIKERS ====================

    squad.append(Player(
        name="Viktor Gyokeres",
        age=27,
        position="ST",
        nationality="Sweden",
        squad_number=14,
        market_value_m=80.0,
        wage_weekly_k=200.0,
        contract_expiry="2030-06-30",
        stats=PlayerStats(
            appearances=22, goals=6, assists=2, minutes=1760,
            xg=8.5, xa=1.8,
            progressive_passes=12, progressive_carries=25,
            key_passes=8,
            dribbles_completed=12,
            shot_accuracy_pct=33.3,
            aerials_won=32,
            squawka_score=58.0, fotmob_rating=6.9
        ),
        status="available",
        eye_test_notes="Headline signing from Sporting (65.8m). Only 6 PL goals from 8.5 xG - "
                       "significant underperformance. Shot accuracy 33% is concerning. "
                       "Missing 0.45 big chances per 90. Physical presence is excellent "
                       "but adaptation to PL defending has been slow. "
                       "Still trust he'll come good but xG gap is alarming.",
        strengths=["Physical presence", "Hold-up play", "Aerial ability",
                   "Pressing", "xG generation"],
        weaknesses=["Shot accuracy (33%)", "xG underperformance", "PL adaptation",
                   "Big chance conversion", "Touches in tight spaces"],
        role_in_squad="starter"
    ))

    squad.append(Player(
        name="Gabriel Jesus",
        age=28,
        position="ST",
        nationality="Brazil",
        squad_number=9,
        market_value_m=20.0,
        wage_weekly_k=165.0,
        contract_expiry="2027-06-30",
        stats=PlayerStats(
            appearances=9, goals=2, assists=1, minutes=420,
            xg=1.5, xa=0.8,
            progressive_passes=6, progressive_carries=10,
            key_passes=4,
            dribbles_completed=6,
            squawka_score=50.0, fotmob_rating=6.5
        ),
        status="available",
        eye_test_notes="Injury-ravaged season. Only 9 appearances. When fit, brings "
                       "excellent link-up and pressing but conversion has always been an issue. "
                       "High wages for a backup. Potential sell candidate to recoup fees.",
        strengths=["Link-up play", "Pressing", "Experience", "Work rate"],
        weaknesses=["Injury prone", "Conversion rate", "High wages for role", "Confidence issues"],
        role_in_squad="backup"
    ))

    # ==================== LOANED OUT PLAYERS ====================

    squad.append(Player(
        name="Oleksandr Zinchenko",
        age=29,
        position="LB",
        nationality="Ukraine",
        squad_number=None,
        market_value_m=15.0,
        wage_weekly_k=200.0,
        contract_expiry="2026-06-30",
        stats=PlayerStats(),
        status="loaned_out",
        loan_club="Nottingham Forest -> sold to Ajax",
        eye_test_notes="Was loaned to Forest, now sold to Ajax. 200k/week wages freed up. "
                       "Fell behind MLS/Calafiori in pecking order. Departure confirmed.",
        strengths=["Technical ability", "Inverted full-back play"],
        weaknesses=["Defensive liability", "Pace", "Wages"],
        role_in_squad="backup"
    ))

    squad.append(Player(
        name="Jakub Kiwior",
        age=25,
        position="CB",
        nationality="Poland",
        squad_number=None,
        market_value_m=15.0,
        wage_weekly_k=70.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(),
        status="loaned_out",
        loan_club="FC Porto",
        eye_test_notes="On loan at Porto. Decent left-footed CB. Not good enough "
                       "to start for Arsenal. Likely to be sold permanently in summer.",
        strengths=["Left-footed CB", "Ball-playing"],
        weaknesses=["Not PL starting quality", "Aerial duels", "Pace"],
        role_in_squad="backup"
    ))

    squad.append(Player(
        name="Reiss Nelson",
        age=26,
        position="RW",
        nationality="England",
        squad_number=None,
        market_value_m=8.0,
        wage_weekly_k=60.0,
        contract_expiry="2027-06-30",
        stats=PlayerStats(),
        status="loaned_out",
        loan_club="Brentford",
        eye_test_notes="On loan at Brentford. Not Arsenal quality. Should be sold permanently.",
        strengths=["Dribbling", "Academy product"],
        weaknesses=["Not PL top-6 level", "Injuries", "End product"],
        role_in_squad="backup"
    ))

    squad.append(Player(
        name="Fabio Vieira",
        age=25,
        position="AM",
        nationality="Portugal",
        squad_number=None,
        market_value_m=10.0,
        wage_weekly_k=65.0,
        contract_expiry="2027-06-30",
        stats=PlayerStats(),
        status="loaned_out",
        loan_club="Hamburg",
        eye_test_notes="Creative talent but too lightweight for PL. On loan at Hamburg. "
                       "Should be sold permanently to recoup some of original fee.",
        strengths=["Creativity", "Set-piece delivery", "Technical ability"],
        weaknesses=["Physical weakness", "Not PL level", "Injuries"],
        role_in_squad="backup"
    ))

    squad.append(Player(
        name="Karl Hein",
        age=23,
        position="GK",
        nationality="Estonia",
        squad_number=None,
        market_value_m=2.0,
        wage_weekly_k=15.0,
        contract_expiry="2026-06-30",
        stats=PlayerStats(),
        status="loaned_out",
        loan_club="Werder Bremen",
        eye_test_notes="On loan at Bremen. Third-choice GK. Contract expiring. "
                       "Unlikely to have a future at Arsenal.",
        strengths=["Shot-stopping"],
        weaknesses=["Not top-6 level", "No PL experience"],
        role_in_squad="backup"
    ))

    return squad


def build_rival_squads() -> dict:
    """Key rival squad data for context - who they might sell/who they're targeting."""
    return {
        "Manchester City": {
            "strengths": ["Depth", "Haaland", "Foden", "Rodri"],
            "weaknesses": ["Aging squad", "Manager uncertainty post-Guardiola era",
                          "Stuttering form this season"],
            "likely_targets": ["Marc Guehi (reportedly won race)", "Florian Wirtz"],
            "sellable_assets": [],
            "pl_position": "Top 4 but behind Arsenal",
        },
        "Liverpool": {
            "strengths": ["Defending champions", "Slot system embedded", "Salah/Van Dijk"],
            "weaknesses": ["Salah age", "Squad transition ongoing"],
            "likely_targets": ["Rodrygo", "Marc Guehi", "Bouaddi"],
            "sellable_assets": [],
            "pl_position": "Top 4 contender",
        },
        "Chelsea": {
            "strengths": ["Young squad", "Massive investment", "Palmer"],
            "weaknesses": ["Managerial instability (Maresca sacked Jan 2026)",
                          "Bloated squad", "Inconsistency"],
            "likely_targets": ["Various - big spenders"],
            "sellable_assets": [],
            "pl_position": "5th-ish, underperforming",
        },
        "Manchester United": {
            "strengths": ["Individual talent", "Investment"],
            "weaknesses": ["Amorim sacked Jan 2026", "Recruitment disputes",
                          "Underperforming significantly"],
            "likely_targets": ["Rebuilding mode"],
            "sellable_assets": [],
            "pl_position": "Mid-table crisis",
        },
        "Real Madrid": {
            "strengths": ["Mbappe", "Vinicius", "Bellingham"],
            "weaknesses": ["Rodrygo unhappy", "Squad management issues"],
            "likely_targets": [],
            "sellable_assets": ["Rodrygo (wants out)", "Arda Guler (limited minutes)"],
            "pl_position": "N/A - La Liga",
        },
    }


def build_transfer_targets() -> list[Player]:
    """Build database of realistic summer 2026 transfer targets with stats and scouting."""

    targets = []

    # ==================== PRIMARY TARGETS ====================

    # NOTE: Rodrygo (PRICED OUT by Real Madrid), Marc Guehi (SIGNED by Man City),
    # and Jeremy Jacquet (SIGNED by Liverpool) have been removed per intel updates.

    targets.append(Player(
        name="Tino Livramento",
        age=23,
        position="RB",
        nationality="England",
        market_value_m=55.0,
        wage_weekly_k=100.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=24, goals=2, assists=5, minutes=2100,
            progressive_passes=35, progressive_carries=65,
            key_passes=22,
            tackles_won=36, interceptions=24,
            dribbles_completed=20,
            pass_completion_pct=84.5,
            squawka_score=70.0, fotmob_rating=7.3
        ),
        eye_test_notes="Arsenal's TOP target at RB. Arteta and Berta both personally keen. "
                       "Same agency as Arteta (easier personal terms). "
                       "Timber-like profile but more dynamic in attack. "
                       "Newcastle will demand 60m+ EUR. Contract talks stalled. "
                       "Would replace Ben White and provide competition for Timber.",
        strengths=["Pace", "Attacking output", "Versatility (can play LB)",
                   "Ball-carrying", "Young and improving"],
        weaknesses=["Newcastle won't sell cheap", "High fee for RB position",
                   "Defensive discipline needs work"],
        role_in_squad="starter"
    ))

    targets.append(Player(
        name="Ayyoub Bouaddi",
        age=18,
        position="CM",
        nationality="France",
        market_value_m=45.0,
        wage_weekly_k=60.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=28, goals=3, assists=4, minutes=2200,
            progressive_passes=55, progressive_carries=42,
            key_passes=22,
            tackles_won=28, interceptions=20,
            pass_completion_pct=88.5,
            squawka_score=72.0, fotmob_rating=7.3
        ),
        eye_test_notes="18-year-old Lille midfielder. Complete CM with massive potential. "
                       "Valued ~43m GBP. Arsenal are in the chase. "
                       "Would be a long-term Merino successor and Odegaard backup. "
                       "Outstanding for his age - started nearly every Lille game.",
        strengths=["Complete midfielder", "Youth and ceiling", "Progressive passing",
                   "Defensive intelligence for age", "French market knowledge"],
        weaknesses=["High fee for 18-year-old", "PL adaptation risk",
                   "Competition from Man Utd, Real Madrid"],
        role_in_squad="rotation"
    ))

    targets.append(Player(
        name="Arda Guler",
        age=21,
        position="AM",
        nationality="Turkey",
        market_value_m=40.0,
        wage_weekly_k=80.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=18, goals=4, assists=3, minutes=900,
            xg=3.5, xa=2.5,
            progressive_passes=22, progressive_carries=18,
            key_passes=16,
            dribbles_completed=14,
            pass_completion_pct=85.0,
            squawka_score=66.0, fotmob_rating=7.1
        ),
        eye_test_notes="Real Madrid prodigy with limited minutes. Exceptional left foot. "
                       "Can play RW/AM. Summer interest more likely than January. "
                       "Would add elite creativity. Loan with option to buy possible.",
        strengths=["Left foot quality", "Creativity", "Shooting", "Youth potential"],
        weaknesses=["Limited senior minutes", "Physical development",
                   "Real Madrid may not sell permanently"],
        role_in_squad="rotation"
    ))

    targets.append(Player(
        name="Julian Alvarez",
        age=26,
        position="ST",
        nationality="Argentina",
        market_value_m=80.0,
        wage_weekly_k=180.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=25, goals=10, assists=5, minutes=2000,
            xg=9.0, xa=4.0,
            progressive_passes=20, progressive_carries=35,
            key_passes=18,
            dribbles_completed=16,
            shot_accuracy_pct=48.0,
            squawka_score=72.0, fotmob_rating=7.4
        ),
        eye_test_notes="World Cup winner. Atletico Madrid forward who can play anywhere "
                       "across the front line. Arsenal exploring possibility. "
                       "Would give Gyokeres elite competition or allow tactical flexibility. "
                       "Fee would be massive (80m+).",
        strengths=["Versatility across front 3", "Big-game mentality", "Work rate",
                   "Link-up play", "World Cup winner"],
        weaknesses=["Atletico unlikely to sell", "Very expensive",
                   "Would need to displace Gyokeres or adjust system"],
        role_in_squad="starter"
    ))

    # ==================== REPLACEMENT TARGETS (Feb 2026 Intel Update) ====================

    targets.append(Player(
        name="Konstantinos Koulierakis",
        age=22,
        position="CB",
        nationality="Greece",
        market_value_m=35.0,
        wage_weekly_k=70.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=17, goals=0, assists=0, minutes=1485,
            progressive_passes=28, progressive_carries=15,
            tackles_won=32, interceptions=26, aerials_won=42,
            pass_completion_pct=85.5,
            squawka_score=67.0, fotmob_rating=7.1
        ),
        eye_test_notes="22-year-old Wolfsburg CB. LEFT-FOOTED — ideal to partner Saliba. "
                       "Signed from PAOK for just 12m in 2024. Nominated for Bundesliga "
                       "Rookie of the Month 3 times. Physically imposing (1.88m) with "
                       "excellent recovery pace. Strong in the air and technically solid "
                       "in build-up. Wolfsburg are a selling club — 35-40m realistic. "
                       "Top replacement for Guehi (City) and Jacquet (Liverpool).",
        strengths=["Left-footed CB", "Aerial dominance", "Recovery pace",
                   "Ball-playing ability", "Affordable", "Selling club"],
        weaknesses=["Ball progression under high press needs work",
                   "Interest from Liverpool, Spurs, Inter, Juve",
                   "Bundesliga to PL adaptation"],
        role_in_squad="rotation"
    ))

    targets.append(Player(
        name="Giorgio Scalvini",
        age=22,
        position="CB",
        nationality="Italy",
        market_value_m=50.0,
        wage_weekly_k=90.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=14, goals=2, assists=0, minutes=733,
            progressive_passes=22, progressive_carries=20,
            tackles_won=18, interceptions=14, aerials_won=30,
            pass_completion_pct=87.0,
            squawka_score=69.0, fotmob_rating=7.3
        ),
        eye_test_notes="Atalanta's CB/DM hybrid. Europa League winner at 20. Full Italian "
                       "international. The 'dream modern CB' — 1.94m, elite on the ball, "
                       "progressive carries, line-breaking passes. Can step into midfield. "
                       "ACL tear (June 2024) and muscle injuries keep price at 45-55m — "
                       "when fit, he's a 70m+ player. Medical assessment critical. "
                       "Newcastle have scouted for 2+ years. Higher ceiling than Koulierakis.",
        strengths=["Ball-playing ability (elite)", "CB/DM versatility", "Aerial dominance (1.94m)",
                   "CL experience", "Progressive carrying", "Full international"],
        weaknesses=["ACL tear history (June 2024)", "Muscle injuries in 2025",
                   "Medical risk premium", "Newcastle and Man Utd also interested"],
        role_in_squad="starter"
    ))

    targets.append(Player(
        name="Karim Adeyemi",
        age=24,
        position="LW",
        nationality="Germany",
        market_value_m=65.0,
        wage_weekly_k=130.0,
        contract_expiry="2027-06-30",
        stats=PlayerStats(
            appearances=16, goals=5, assists=5, minutes=1200,
            xg=4.2, xa=4.0,
            progressive_passes=18, progressive_carries=48,
            key_passes=20,
            dribbles_completed=28,
            pass_completion_pct=80.0,
            squawka_score=71.0, fotmob_rating=7.3
        ),
        eye_test_notes="Dortmund's explosive attacker. WANTS ARSENAL — told BVB he prefers "
                       "London over Manchester. Same reports say 'his reps prefer Arsenal.' "
                       "Elite pace, direct, versatile (LW/RW/CF). Contract expires 2027 "
                       "so Dortmund under pressure to sell. Extension talks stalled — "
                       "Adeyemi only extends with release clause (BVB refused). "
                       "Asking price 60-70m EUR. Player preference gives Arsenal huge leverage. "
                       "Replaces Rodrygo's intended role — pace, directness, creativity.",
        strengths=["Elite pace (one of fastest in Bundesliga)", "Player wants Arsenal",
                   "1v1 dribbling", "Versatility across front line",
                   "Contract leverage (2027)", "Goal threat and creation"],
        weaknesses=["Fee still 60-70m", "Man Utd, Chelsea, Liverpool also interested",
                   "Injury history at Dortmund", "PL physicality adaptation"],
        role_in_squad="starter"
    ))

    targets.append(Player(
        name="Davide Bartesaghi",
        age=19,
        position="LB",
        nationality="Italy",
        market_value_m=12.0,
        wage_weekly_k=25.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=16, goals=0, assists=2, minutes=1100,
            progressive_passes=18, progressive_carries=28,
            tackles_won=16, interceptions=10,
            pass_completion_pct=84.0,
            squawka_score=58.0, fotmob_rating=6.7
        ),
        eye_test_notes="AC Milan LB prospect Arsenal are monitoring. Athletic, "
                       "modern full-back profile. Would be a long-term LB option. "
                       "Milan concerned about Arsenal interest.",
        strengths=["Athletic profile", "Youth", "Modern full-back attributes"],
        weaknesses=["Very raw", "Limited Serie A experience", "Unknown PL fit"],
        role_in_squad="youth"
    ))

    # ==================== ADDITIONAL OPTIONS (3 per position) ====================

    # --- CB Option 3 ---
    targets.append(Player(
        name="Castello Lukeba",
        age=22,
        position="CB",
        nationality="France",
        market_value_m=48.0,
        wage_weekly_k=85.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=20, goals=1, assists=1, minutes=1750,
            progressive_passes=38, progressive_carries=22,
            tackles_won=26, interceptions=20, aerials_won=32,
            pass_completion_pct=90.5,
            squawka_score=70.0, fotmob_rating=7.2
        ),
        eye_test_notes="RB Leipzig's French CB. LEFT-FOOTED, elite passer from the back. "
                       "Former Lyon academy product, France U21 captain turned senior call-up. "
                       "One of the best ball-playing CBs in Bundesliga — top 5% progressive "
                       "passes among CBs. Quick for his size, reads the game superbly. "
                       "Leipzig will sell at the right price (50m range). "
                       "More polished on the ball than Koulierakis, slightly less physical.",
        strengths=["Left-footed", "Elite passing range", "Pace for a CB",
                   "France international pedigree", "Reading of the game"],
        weaknesses=["Leipzig will want 50m+", "Not the most dominant aerially",
                   "Competition from Bayern, Barcelona"],
        role_in_squad="starter"
    ))

    # --- RB Option 2 ---
    targets.append(Player(
        name="Lutsharel Geertruida",
        age=24,
        position="RB",
        nationality="Netherlands",
        market_value_m=32.0,
        wage_weekly_k=75.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=22, goals=3, assists=4, minutes=1900,
            progressive_passes=32, progressive_carries=40,
            key_passes=18,
            tackles_won=30, interceptions=22,
            dribbles_completed=12,
            pass_completion_pct=87.0,
            squawka_score=68.0, fotmob_rating=7.1
        ),
        eye_test_notes="RB Leipzig's versatile Dutch defender. Can play RB, CB, and DM — "
                       "Arteta would love his positional flexibility (inverting fullback). "
                       "Former Feyenoord star, Eredivisie champion. Strong in build-up, "
                       "composed under pressure. More defensive than Livramento but smarter "
                       "positionally. Cheaper option at 30-35m.",
        strengths=["Positional versatility (RB/CB/DM)", "Tactical intelligence",
                   "Build-up play", "Affordable", "Dutch international"],
        weaknesses=["Not as dynamic going forward as Livramento",
                   "Limited top-level CL experience",
                   "Not a pace merchant"],
        role_in_squad="rotation"
    ))

    # --- RB Option 3 ---
    targets.append(Player(
        name="Vanderson",
        age=23,
        position="RB",
        nationality="Brazil",
        market_value_m=28.0,
        wage_weekly_k=65.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=23, goals=1, assists=6, minutes=1950,
            progressive_passes=28, progressive_carries=55,
            key_passes=20,
            tackles_won=24, interceptions=16,
            dribbles_completed=26,
            pass_completion_pct=82.0,
            squawka_score=67.0, fotmob_rating=7.0
        ),
        eye_test_notes="Monaco's Brazilian RB. Electric going forward — among top RBs in "
                       "Ligue 1 for dribbles and progressive carries. Reminiscent of Dani Alves "
                       "in his attacking instincts. Defensive work has improved under Huetter. "
                       "Monaco are a selling club and 25-30m is realistic. "
                       "Would provide a completely different profile to Timber — pure attack.",
        strengths=["Explosive attacking runs", "Dribbling", "Crossing quality",
                   "Youth", "Selling club = cheaper"],
        weaknesses=["Defensive positioning still developing",
                   "Ligue 1 to PL jump is significant",
                   "Not PL proven"],
        role_in_squad="rotation"
    ))

    # --- LB Option 2 ---
    targets.append(Player(
        name="Milos Kerkez",
        age=22,
        position="LB",
        nationality="Hungary",
        market_value_m=35.0,
        wage_weekly_k=70.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=24, goals=1, assists=4, minutes=2100,
            progressive_passes=30, progressive_carries=52,
            key_passes=16,
            tackles_won=32, interceptions=18,
            dribbles_completed=18,
            pass_completion_pct=82.5,
            squawka_score=69.0, fotmob_rating=7.1
        ),
        eye_test_notes="Bournemouth's Hungarian LB. ALREADY PL-PROVEN — huge advantage. "
                       "Athletic, aggressive, brilliant in transition. Arsenal have been "
                       "linked repeatedly. Fills the Zinchenko hole with a completely "
                       "different profile — more dynamic and defensively solid. "
                       "Bournemouth will sell for 35m. Best value LB on the market.",
        strengths=["PL proven", "Athleticism and pace", "Defensive solidity",
                   "Transition play", "Reasonable price"],
        weaknesses=["Technical ceiling not as high as elite LBs",
                   "Crossing accuracy inconsistent",
                   "Multiple PL clubs interested"],
        role_in_squad="starter"
    ))

    # --- LB Option 3 ---
    targets.append(Player(
        name="Alejandro Balde",
        age=22,
        position="LB",
        nationality="Spain",
        market_value_m=38.0,
        wage_weekly_k=80.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=20, goals=0, assists=3, minutes=1600,
            progressive_passes=25, progressive_carries=48,
            key_passes=14,
            tackles_won=20, interceptions=12,
            dribbles_completed=22,
            pass_completion_pct=86.0,
            squawka_score=66.0, fotmob_rating=7.0
        ),
        eye_test_notes="Barcelona's Spanish LB. Barca may need to sell for FFP compliance. "
                       "Extremely quick, technically excellent, La Masia product. "
                       "Has played in CL knockouts for Barca. Spain international. "
                       "Recovered well from ACL injury in 2024. If Barcelona need cash, "
                       "35-40m could be enough. High ceiling if he stays fit.",
        strengths=["Elite pace", "Technical ability (La Masia)", "Spain international",
                   "CL experience", "Only 22"],
        weaknesses=["ACL injury history (2024)", "Barcelona may not sell",
                   "Defensive positioning needs improvement"],
        role_in_squad="starter"
    ))

    # --- CM Option 2 ---
    targets.append(Player(
        name="Adam Wharton",
        age=22,
        position="CM",
        nationality="England",
        market_value_m=42.0,
        wage_weekly_k=75.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=22, goals=1, assists=3, minutes=1800,
            progressive_passes=48, progressive_carries=20,
            key_passes=24,
            tackles_won=22, interceptions=18,
            pass_completion_pct=91.0,
            squawka_score=70.0, fotmob_rating=7.2
        ),
        eye_test_notes="Crystal Palace's English CM. Deep-lying playmaker with absurd "
                       "passing accuracy (91%+). England international at 21. PL PROVEN. "
                       "Controls tempo like a young Jorginho but with more mobility. "
                       "Would be the ideal Zubimendi partner — one progresses, one dictates. "
                       "Palace will demand 40-50m. Homegrown quota advantage.",
        strengths=["PL proven", "Elite passing accuracy", "England international",
                   "Homegrown", "Tempo control", "Young"],
        weaknesses=["Palace will demand premium", "Not a goal threat",
                   "Needs to add physicality for top level"],
        role_in_squad="rotation"
    ))

    # --- CM Option 3 ---
    targets.append(Player(
        name="Ederson",
        age=26,
        position="CM",
        nationality="Brazil",
        market_value_m=50.0,
        wage_weekly_k=100.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=24, goals=4, assists=3, minutes=2000,
            progressive_passes=40, progressive_carries=38,
            key_passes=16,
            tackles_won=42, interceptions=28,
            aerials_won=18,
            pass_completion_pct=87.0,
            squawka_score=71.0, fotmob_rating=7.3
        ),
        eye_test_notes="Atalanta's Brazilian B2B midfielder. Europa League winner. "
                       "Dominant ball-winner who also carries forward — a Declan Rice "
                       "comparison is fair. Physical, tireless, CL-proven. "
                       "26 is peak age for a CM signing. Atalanta will sell at 50m. "
                       "More mature and ready-made than Bouaddi. Less ceiling, more floor.",
        strengths=["Ball-winning ability (elite)", "Box-to-box engine", "CL proven",
                   "Physical presence", "Goals from midfield"],
        weaknesses=["Atalanta will want 50m+", "Already 26 (limited resale)",
                   "Serie A to PL adaptation"],
        role_in_squad="starter"
    ))

    # --- AM Option 2 ---
    targets.append(Player(
        name="Desire Doue",
        age=21,
        position="AM",
        nationality="France",
        market_value_m=38.0,
        wage_weekly_k=70.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=22, goals=3, assists=4, minutes=1400,
            xg=2.8, xa=3.5,
            progressive_passes=20, progressive_carries=35,
            key_passes=22,
            dribbles_completed=24,
            pass_completion_pct=83.0,
            squawka_score=66.0, fotmob_rating=7.0
        ),
        eye_test_notes="PSG's young French attacker. Versatile — plays AM, LW, RW. "
                       "Olympic gold medalist with France at Paris 2024. Silky dribbler, "
                       "creative passer, can unlock defences in tight spaces. "
                       "May struggle for minutes at PSG behind Dembele/Barcola. "
                       "A loan with option to buy could be possible. "
                       "High ceiling — reminiscent of a young Bernardo Silva.",
        strengths=["Versatility (AM/LW/RW)", "Dribbling in tight spaces",
                   "France international", "Olympic gold medalist", "Creative vision"],
        weaknesses=["PSG may not sell permanently", "Needs more end product",
                   "Physical development for PL"],
        role_in_squad="rotation"
    ))

    # --- AM Option 3 ---
    targets.append(Player(
        name="Takefusa Kubo",
        age=24,
        position="AM",
        nationality="Japan",
        market_value_m=35.0,
        wage_weekly_k=75.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=24, goals=6, assists=5, minutes=1900,
            xg=5.0, xa=4.5,
            progressive_passes=28, progressive_carries=42,
            key_passes=30,
            dribbles_completed=32,
            pass_completion_pct=82.0,
            squawka_score=70.0, fotmob_rating=7.2
        ),
        eye_test_notes="Real Sociedad's Japanese creator. Former Barca/Real Madrid youth. "
                       "Outstanding dribbler and chance creator — La Liga's hidden gem. "
                       "Can play RW or AM. Release clause around 60m but Sociedad would "
                       "likely accept 35-40m. Arsenal scouted extensively in 2025. "
                       "Would add flair and unpredictability. Excellent in 1v1 situations.",
        strengths=["1v1 dribbling (elite)", "Chance creation", "La Liga proven",
                   "Release clause available", "Versatile attacker"],
        weaknesses=["Physical stature (1.73m)", "PL intensity is different",
                   "Defensive contribution limited"],
        role_in_squad="rotation"
    ))

    # --- ST Option 2 ---
    targets.append(Player(
        name="Benjamin Sesko",
        age=23,
        position="ST",
        nationality="Slovenia",
        market_value_m=65.0,
        wage_weekly_k=120.0,
        contract_expiry="2029-06-30",
        stats=PlayerStats(
            appearances=24, goals=14, assists=3, minutes=2000,
            xg=12.0, xa=2.5,
            progressive_passes=15, progressive_carries=30,
            key_passes=10,
            dribbles_completed=14,
            shot_accuracy_pct=52.0, aerials_won=28,
            squawka_score=73.0, fotmob_rating=7.4
        ),
        eye_test_notes="RB Leipzig's Slovenian striker. 1.95m powerhouse with genuine pace — "
                       "a rare combination. 14 goals in 24 apps this season. Arsenal were "
                       "very close to signing him in 2024 before he renewed. Release clause "
                       "reportedly 65m. Different profile to Gyokeres — more physical, "
                       "better in the air. Could form a devastating partnership or rotation.",
        strengths=["Pace + power combination (rare)", "Aerial threat (1.95m)",
                   "Release clause available", "Young with huge ceiling",
                   "Arsenal already have relationship"],
        weaknesses=["Release clause is 65m", "Link-up play still developing",
                   "Big club move might affect form"],
        role_in_squad="starter"
    ))

    # --- ST Option 3 ---
    targets.append(Player(
        name="Jonathan David",
        age=26,
        position="ST",
        nationality="Canada",
        market_value_m=0.0,  # FREE AGENT
        wage_weekly_k=140.0,
        contract_expiry="2026-06-30",
        stats=PlayerStats(
            appearances=26, goals=15, assists=4, minutes=2200,
            xg=13.5, xa=3.0,
            progressive_passes=18, progressive_carries=22,
            key_passes=14,
            dribbles_completed=12,
            shot_accuracy_pct=50.0,
            squawka_score=72.0, fotmob_rating=7.3
        ),
        eye_test_notes="LOSC Lille's Canadian striker. AVAILABLE ON FREE TRANSFER — "
                       "contract expires June 2026. Prolific scorer — 15+ goals per season "
                       "for 5 consecutive years. Smart movement, clinical finisher, "
                       "works hard pressing from the front. At zero fee, this is incredible "
                       "value even as a rotation striker. Links to Barcelona and Man Utd.",
        strengths=["FREE TRANSFER", "Proven prolific scorer", "Clinical finishing",
                   "Smart movement", "High pressing work rate"],
        weaknesses=["Massive wage demands (free agent premium)",
                   "Competition from Barca, Man Utd, Juventus",
                   "Not the most physically imposing"],
        role_in_squad="rotation"
    ))

    # --- LW Option 2 ---
    targets.append(Player(
        name="Nico Williams",
        age=24,
        position="LW",
        nationality="Spain",
        market_value_m=58.0,
        wage_weekly_k=120.0,
        contract_expiry="2028-06-30",
        stats=PlayerStats(
            appearances=24, goals=7, assists=8, minutes=2000,
            xg=5.5, xa=6.0,
            progressive_passes=22, progressive_carries=55,
            key_passes=26,
            dribbles_completed=36,
            pass_completion_pct=79.0,
            squawka_score=74.0, fotmob_rating=7.5
        ),
        eye_test_notes="Athletic Bilbao's Spanish winger. Euro 2024 star alongside Yamal. "
                       "Explosive, direct, brilliant in 1v1. Release clause around 58m. "
                       "Barcelona tried and failed in 2024. The most complete winger option — "
                       "can score, create, and beat any defender. PL physicality would "
                       "suit him. The dream LW signing if Adeyemi falls through.",
        strengths=["Elite pace and directness", "Spain international (Euro 2024 star)",
                   "Release clause available (58m)", "Goal and assist threat",
                   "1v1 ability among best in Europe"],
        weaknesses=["Release clause is firm — no negotiation",
                   "Athletic Bilbao emotional attachment",
                   "High wage demands"],
        role_in_squad="starter"
    ))

    # --- LW Option 3 ---
    targets.append(Player(
        name="Johan Bakayoko",
        age=22,
        position="LW",
        nationality="Belgium",
        market_value_m=42.0,
        wage_weekly_k=70.0,
        contract_expiry="2027-06-30",
        stats=PlayerStats(
            appearances=22, goals=8, assists=6, minutes=1800,
            xg=6.5, xa=5.0,
            progressive_passes=20, progressive_carries=45,
            key_passes=24,
            dribbles_completed=30,
            pass_completion_pct=81.0,
            squawka_score=71.0, fotmob_rating=7.3
        ),
        eye_test_notes="PSV Eindhoven's Belgian winger. Breakout star of the Eredivisie. "
                       "Right-footed playing on the left — loves to cut inside and shoot. "
                       "8 goals and 6 assists in 22 games. Belgium international. "
                       "Contract runs to 2027 so PSV under pressure to sell. "
                       "Cheaper alternative to Adeyemi/Williams at 40-45m. "
                       "Raw but incredibly exciting — huge ceiling.",
        strengths=["Goal threat from LW (cuts inside)", "Exciting dribbler",
                   "Contract leverage (2027)", "Young with high ceiling",
                   "Most affordable LW option"],
        weaknesses=["Eredivisie to PL is a big jump",
                   "Defensive effort inconsistent",
                   "Decision-making still maturing"],
        role_in_squad="rotation"
    ))

    return targets


# Contracts expiring in summer 2026
EXPIRING_CONTRACTS_2026 = [
    "Leandro Trossard",  # Will leave for free or renewed
    "Karl Hein",  # Will leave
]

# Players likely to be sold
SELL_CANDIDATES = [
    "Gabriel Martinelli",    # ~50m, plateaued
    "Ben White",             # ~25m, unhappy with minutes
    "Gabriel Jesus",         # ~20m, injury-prone, high wages
    "Jakub Kiwior",          # ~15m, not good enough
    "Reiss Nelson",          # ~8m, not Arsenal level
    "Fabio Vieira",          # ~10m, not PL level
]

# Revenue projections from sales
PROJECTED_SALE_REVENUE = {
    "Gabriel Martinelli": 50.0,
    "Ben White": 25.0,
    "Gabriel Jesus": 20.0,
    "Jakub Kiwior": 15.0,
    "Reiss Nelson": 8.0,
    "Fabio Vieira": 10.0,
    "Leandro Trossard": 0.0,  # free agent departure
    "Karl Hein": 0.0,  # free agent departure
}
