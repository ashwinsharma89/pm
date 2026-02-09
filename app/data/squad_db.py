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
    why_works: list = field(default_factory=list)
    why_wont_work: list = field(default_factory=list)


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
        role_in_squad="starter",
        why_works=[
            "The perfect Timber complement. While Timber inverts brilliantly into midfield, "
            "Livramento offers something different — explosive overlapping runs that stretch "
            "defences. When teams double up on Saka, the overlapping RB creates the 2v1 that "
            "unlocks the right side. That's 5+ extra chances per game Arsenal currently leave on the table.",
            "Already PL-proven at Newcastle in a system demanding defensive discipline AND attacking "
            "output. No adaptation period. His 65 progressive carries are outstanding — he can be the "
            "right-side outlet when Arsenal need to break the low blocks they face in 70% of games.",
            "Same agency as Arteta = faster deal completion, easier personal terms. At 23, he's about "
            "to enter his prime. Fills the Ben White-shaped hole with a genuine upgrade in dynamism.",
            "English and homegrown — crucial for squad registration. Newcastle's contract talks have "
            "stalled, giving Arsenal a genuine window to prise him away."
        ],
        why_wont_work=[
            "55m+ for a RB when Timber is already your starter and scored 78 Squawka is a LOT of "
            "capital for what could end up being squad depth. If Timber stays fit and dominant, "
            "Livramento might be unhappy as rotation — that's an expensive ego problem.",
            "Newcastle will play hardball. They don't need to sell, and the asking price could balloon "
            "to 70m in a negotiation war. At that price, the opportunity cost is brutal — you could "
            "get a starting CB AND a CM rotation option for the same money.",
            "His defensive discipline is still developing. At Newcastle, Trippier and the system cover "
            "for him. In Arteta's high defensive line, one positional error against elite wingers "
            "(Son, Diaz, Grealish) means a 1v1 with Raya. PL fine margins don't forgive that.",
            "The 84.5% pass completion is below what Arteta demands from his fullbacks in possession. "
            "Timber is at 88.4% — that gap matters in Arteta's build-up."
        ],
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
        role_in_squad="rotation",
        why_works=[
            "Generational talent. At 18, starting every game for Lille in Ligue 1 AND Champions "
            "League — that's absurd maturity. His 55 progressive passes and 42 progressive carries "
            "mean he can do BOTH sides of the Arteta midfield game: progress AND carry.",
            "The perfect succession plan. Odegaard is 27 with ankle issues, Merino is turning 30. "
            "Bouaddi can learn behind them for a season, then gradually take over the #8 role. "
            "His trajectory mirrors Saliba's path — France youth captain to senior, develop at Arsenal, "
            "become world-class by 22. Arsenal KNOW this French market pathway.",
            "His defensive intelligence at 18 (28 tackles, 20 interceptions) is remarkable — Arteta's "
            "midfield demands defensive contribution and Bouaddi already has it instinctively. "
            "At 45m, if he becomes what the data projects, this is a 150m+ asset in 4 years.",
            "88.5% pass completion at 18 — already close to Arsenal's midfield standards. His decision-making "
            "under pressure is beyond his years."
        ],
        why_wont_work=[
            "He's 18. In the PREMIER LEAGUE. The midfield physicality of Rice, Rodri, Bruno, Caicedo — "
            "these are grown men in their physical prime. Bouaddi is 5'11 and still developing. The risk "
            "of a Gavi-type burnout (played too much too young, ACL at 19) is genuinely frightening.",
            "45m for a teenager is an enormous gamble when Arsenal are trying to win the league NOW, not "
            "in 3 years. If Bouaddi needs a year to adapt (highly likely), that's 45m of budget sitting "
            "on the bench while other positions go unaddressed.",
            "Ligue 1 to PL is historically the hardest jump for midfielders. Ndombele, Lo Celso, "
            "Sangare — the list of French midfield stars who flopped in England is long. The intensity, "
            "the physicality, the speed of play — it's a different sport.",
            "Competition from Real Madrid and Man Utd could price Arsenal out or mean he simply doesn't "
            "choose London. If he picks Madrid, we've wasted months of negotiation capital."
        ],
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
        role_in_squad="rotation",
        why_works=[
            "The most technically gifted AM option. That left foot is special — Real Madrid signed "
            "him at 18 because they saw the next Mesut Ozil. His 4 goals in just 900 minutes (one "
            "every 225 min) is elite. He can play RW behind Saka or as #10 backup to Odegaard — "
            "tactical flexibility Arteta craves.",
            "A loan with option to buy completely de-risks the deal. Arsenal get a full season to "
            "evaluate him in the PL before committing 40m. Real Madrid's failure to give him minutes "
            "means he's desperate to play — motivated players adapt faster.",
            "His shooting technique is outstanding for an AM — Arteta's system creates half-spaces "
            "for the #10 to shoot from. Odegaard thrives there; Guler's left foot in those pockets "
            "would be equally dangerous. He'd give Arsenal a genuine creative threat from the right "
            "when Saka is rested.",
            "At 21, the ceiling is enormous. If he even becomes 80% of what Madrid thought he'd be, "
            "Arsenal have a generational creative player at a fraction of open-market value."
        ],
        why_wont_work=[
            "900 minutes in a full season at 21 tells you something troubling. Ancelotti (and whoever "
            "followed) didn't trust him enough to play regularly. The suspicion: his off-the-ball work "
            "and physical output aren't PL-grade. Arteta's press demands EVERYONE works — Ozil was "
            "the cautionary tale. Guler has that exact same risk profile.",
            "Physical development is genuinely concerning for the PL. At 1.80m, he's not small, but "
            "his body hasn't filled out yet. The Caicedos, Bissoumas, and Ndidis of the PL would "
            "physically overwhelm him in midfield. This isn't La Liga where referees protect technical players.",
            "Real Madrid may not sell permanently — just a loan. That leaves Arsenal without a permanent "
            "asset and another summer negotiation headache. Limited competitive minutes means he hasn't "
            "been tested in must-win, high-pressure situations. The PL doesn't give you time to find your feet.",
            "His 85% pass completion is below Odegaard's from the same position. If the backup #10 "
            "loses the ball more than the starter, the drop-off when Odegaard rests becomes a problem."
        ],
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
        role_in_squad="starter",
        why_works=[
            "World Cup winner. Champions League winner. You're getting a player who has WON at the "
            "absolute highest level. His versatility (anywhere across the front line) gives Arteta "
            "options he's never had — Alvarez behind Gyokeres, as a false 9, dropping deep as a "
            "link-up man. Mid-game tactical shifts without substitutions.",
            "His work rate is exceptional — he presses like a midfielder, which Arteta's system demands. "
            "Under Simeone's defensive structure at Atletico, he's had to work harder off the ball than "
            "at City. Imagine what he'd do with Saka, Odegaard, and Rice creating for him.",
            "He'd make Gyokeres better through competition. Arsenal's striker position has no genuine "
            "internal competition (Jesus is injured, done). Alvarez arriving would push Gyokeres to "
            "sharpen his finishing — that xG underperformance disappears when your spot isn't guaranteed.",
            "His big-game mentality is PROVEN under the most intense pressure — World Cup final, "
            "CL knockout rounds, Atletico derbies. Arsenal need players who step UP in April/May."
        ],
        why_wont_work=[
            "80m+ is INSANE money for a player who may not start. If Gyokeres hits form (the quality "
            "IS there — 8.5 xG doesn't lie), where does Alvarez play? You don't pay 80m for rotation. "
            "This deal would eat OVER HALF the transfer budget on ONE player when Arsenal need 4-5 signings.",
            "Atletico are under zero pressure to sell. Simeone loves him, the fans love him, he's their "
            "talisman. Arsenal would need to trigger astronomical release clauses or overpay. "
            "Meanwhile, that 80m buys you two impact signings elsewhere (e.g. Adeyemi + Koulierakis).",
            "His Atletico output (10 goals in 25 games) is good but not elite 20-goal-a-season level. "
            "For 80m, you need a player who transforms your attack. Alvarez improves it; he doesn't "
            "transform it. The pragmatic move is to trust Gyokeres and spend the money across the squad.",
            "Potential dressing room politics. Two 80m+ strikers (Gyokeres cost 65.8m) fighting for one "
            "shirt creates tension. The player who doesn't play makes headlines, agents get involved, "
            "morale suffers. Arsenal's harmony is a competitive advantage — this could disrupt it."
        ],
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
        role_in_squad="rotation",
        why_works=[
            "LEFT-FOOTED. Cannot overstate this. Arteta's build-up needs a left-footed LCB to open "
            "natural passing angles — diagonal balls to the LW, switches to Saka, progressive passes "
            "into Zubimendi's feet. Gabriel does this with his right foot; a natural lefty does it 0.3 "
            "seconds faster. At PL level, that's the difference between beating the press and getting caught.",
            "His aerial dominance (42 aerials won) directly replaces Gabriel's set-piece threat — Arsenal's "
            "set-piece edge is a 10+ goal advantage per season. 1.88m with excellent timing means he "
            "slots into the near-post routine immediately.",
            "Recovery pace means he can play Arteta's HIGH defensive line. When Rice and Timber push "
            "forward, the CBs are exposed in transition. Koulierakis has the legs to recover — that's "
            "non-negotiable against Salah, Haaland, and Isak.",
            "Wolfsburg are a selling club — 35-40m is realistic, leaving budget for LW and CM. "
            "At 22, he grows alongside Saliba for 8+ years as a partnership. The value proposition "
            "is outstanding."
        ],
        why_wont_work=[
            "Bundesliga to PL is the hardest jump for centre-backs. The tactical demand, physical "
            "intensity, and speed of transitions are completely different. His 85.5% pass completion "
            "is OK for Wolfsburg but Arsenal's CBs need 90%+ (Saliba: 92.1%, Gabriel: 89.5%). "
            "Under PL pressing, that gap could widen alarmingly.",
            "His ball progression UNDER HIGH PRESS is the specific concern. When Liverpool or City "
            "press high and aggressive, can he play through it? Wolfsburg face that kind of press "
            "maybe 3-4 times a season. At Arsenal it's every other week.",
            "Interest from Liverpool, Spurs, Inter, and Juve means a bidding war could push the price "
            "to 45-50m, eroding the value advantage. If it goes to auction, the selling club leverage disappears.",
            "Not CL-proven at the highest level. Wolfsburg's European experience is Europa Conference — "
            "a completely different intensity to CL knockout rounds against Real Madrid or Bayern."
        ],
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
        role_in_squad="starter",
        why_works=[
            "The most ARTETA-FRIENDLY CB profile on the market. At 1.94m with elite ball-playing, "
            "he's what Arteta dreamed of — a CB who steps into midfield in possession and dominates "
            "the box out of it. His ability to carry the ball out of defence AND play line-breaking "
            "passes is vanishingly rare. He'd transform Arsenal's build-up from the left.",
            "Gasperini's Atalanta system drills man-marking and defensive aggression — that's directly "
            "transferable to Arteta's high press. Scalvini already knows how to press a striker, "
            "step into midfield, and recover his position. Europa League winner = big-game mentality.",
            "CB/DM versatility is gold. If Zubimendi gets injured, Scalvini can cover the #6 role "
            "without buying a separate backup. That's squad depth worth 30m you don't have to spend. "
            "Full Italian international at 22 — the pedigree is undeniable.",
            "When fit, he's a 70m+ player available for 45-55m because of injury discount. That's "
            "the kind of market inefficiency elite clubs exploit. If Arsenal's medical team clears him, "
            "this is the best pure CB signing available in Europe."
        ],
        why_wont_work=[
            "The ACL tear in June 2024 is a RED FLAG. Arsenal have been burned by injury-prone signings "
            "before. You CANNOT build a title challenge around a player with a compromised knee. "
            "His muscle injuries in 2025 suggest the body is compensating — that's a cascading injury risk.",
            "At 50m+ with medical risk, the ROI could be catastrophic if he breaks down again. A player "
            "who misses 15+ games defeats the purpose of signing a CB for depth and competition. "
            "Arsenal need availability above all else — 60 games across all competitions demand durability.",
            "Atalanta's man-marking system is FUNDAMENTALLY different from Arteta's zonal/positional "
            "setup. The tactical re-grooving takes time — he's used to following a man, not holding a line. "
            "That transition period could cost Arsenal in the early season title race.",
            "Newcastle and Man Utd are also interested. If it goes to auction, Arsenal could overpay for "
            "a player whose medical could fail. The scouting time and negotiation capital wasted on a "
            "deal that collapses is a hidden cost clubs underestimate."
        ],
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
        role_in_squad="starter",
        why_works=[
            "HE WANTS TO COME. In transfers, player willingness is 50% of the battle. When a player "
            "desperately wants to play for your club, the adaptation, the commitment, the extra yard — "
            "it all follows. Adeyemi told Dortmund he prefers London over Manchester. His reps prefer Arsenal.",
            "Against deep blocks — Arsenal's biggest tactical challenge — having someone who can beat a man "
            "1v1 and create chaos is priceless. Martinelli has plateaued; Adeyemi is the direct upgrade. "
            "His 28 dribbles completed in just 16 games is elite. 5G + 5A while missing games to injury "
            "projects to 12G + 12A over a full season.",
            "Arteta's left side demands the LW to cut inside while Calafiori overlaps — Adeyemi's pace "
            "and directness driving at the centre-back creates the space for Calafiori's overlaps AND "
            "opens the switch to Saka isolated 1v1 on the right. The system unlocks.",
            "Dortmund's 2027 contract means they MUST sell or lose him cheap next year. The 60-65m "
            "price is fair market, not inflated. His versatility (LW/RW/CF) also covers Saka injury risk."
        ],
        why_wont_work=[
            "Injury history at Dortmund is genuinely concerning — he's missed significant chunks of "
            "EVERY season. Arsenal play 60 games/season across 4 competitions. If the LW plays 25, "
            "you've spent 65m on half a season. Martinelli's availability (19 apps so far) was already "
            "a problem — replacing one unavailable LW with another is madness.",
            "PL physicality is VERY different to Bundesliga. Van Dijk, Saliba, Dias — these defenders "
            "deal with pace differently. They don't dive in; they show you wide and use their body. "
            "Adeyemi's Bundesliga success is partly because defenders commit — PL defenders don't.",
            "65m on a LW when you also need a CB, CM, and RB means this signing could starve other "
            "positions of budget. Arsenal's squad has 4-5 gaps; filling one at the expense of others "
            "is how you end up with one world-class flank and a paper-thin bench elsewhere.",
            "His decision-making in the final third needs improvement. At Dortmund, he's given freedom "
            "to try and fail. In Arteta's structured system, that freedom vanishes — every possession "
            "must be purposeful. Can he adapt from instinct to structure?"
        ],
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
        role_in_squad="youth",
        why_works=[
            "Pure upside play at 12m. Arsenal's academy model works — Saka, Lewis-Skelly, Nwaneri prove "
            "that investing in young talent and developing them in-house creates both squad value and "
            "culture. Bartesaghi has the athletic profile Arteta's system demands from a modern fullback.",
            "Milan are worried about losing him — that internal concern tells you how highly they rate "
            "him. Italian football develops tactically disciplined defenders — his positional education "
            "under Pioli and Fonseca's systems is elite for his age.",
            "At 12m, even if he takes 2 years to develop, the value proposition is enormous. He could "
            "be the long-term Calafiori competition/successor. If he becomes a starter, Arsenal have "
            "a 60m+ asset for 12m invested. Risk-reward is heavily skewed."
        ],
        why_wont_work=[
            "Way too raw for a title challenge. Arsenal aren't building for 2029 — they need to win NOW. "
            "16 Serie A appearances and zero European experience is nowhere near the quality needed "
            "to compete for PL, CL, and FA Cup simultaneously.",
            "Lewis-Skelly (18) already fills the 'young LB development project' slot. Adding another "
            "creates a positional traffic jam: Calafiori (starter), Hincapie (rotation), MLS (youth), "
            "and now Bartesaghi? That's 4 LBs and none of the newcomers improve the first XI.",
            "The PL is unforgiving for young fullbacks. Could easily be a Tavares situation — the talent "
            "is there but the PL's intensity, physicality, and speed chews him up before he's ready. "
            "At 19, he's a project, not a solution."
        ],
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
        role_in_squad="starter",
        why_works=[
            "The most progressive passer of all three CB options — top 5% among Bundesliga CBs. "
            "Left-footed, which Arsenal NEED. His 90.5% pass completion is ALREADY at Arsenal-level "
            "(Saliba: 92.1%). He'd slot into the build-up immediately without any technical adaptation.",
            "Played under Rose at Leipzig in a pressing, high-line system that mirrors what Arteta "
            "demands. The tactical transition would be minimal compared to Koulierakis (Wolfsburg) "
            "or Scalvini (Atalanta's man-marking). He already understands positional play.",
            "France international pedigree means he handles pressure and big stages. Quick for a CB — "
            "perfect for Arsenal's high defensive line. More technically polished than Koulierakis right now, "
            "which means fewer build-up errors in the crucial early-season period.",
            "His reading of the game compensates for any aerial limitations. He intercepts rather than "
            "challenges — 20 interceptions shows elite anticipation. In Arteta's system, intelligence "
            "matters more than raw physicality."
        ],
        why_wont_work=[
            "Not the most physical CB — against PL strikers like Haaland, Watkins, Isak, aerial "
            "dominance matters MORE than in the Bundesliga. 32 aerials won is decent but not dominant. "
            "Arsenal's set-piece advantage needs an aerial weapon at CB — Lukeba may not provide that.",
            "Leipzig's defensive system protects CBs with a deep DM shield. At Arsenal, the defensive "
            "line is more exposed because fullbacks push incredibly high. When Timber inverts and "
            "Calafiori overlaps, the CBs are the last line — Lukeba hasn't been tested in that isolation.",
            "Competition from Bayern and Barcelona means Arsenal might get into a bidding war that "
            "pushes the price to 55-60m. At that point, the value proposition weakens significantly "
            "compared to Koulierakis at 35-40m.",
            "He hasn't been tested in the PL's unique physicality + pace blend. Bundesliga is fast "
            "but not as physical; La Liga is technical but not as quick. The PL combines ALL of it, "
            "and many excellent Bundesliga CBs have struggled (Upamecano-style errors)."
        ],
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
        role_in_squad="rotation",
        why_works=[
            "The ULTIMATE Arteta fullback. Can play RB, CB, AND DM — this is literally what Arteta's "
            "system demands. The inverting fullback role that Timber plays? Geertruida does it naturally "
            "from his Feyenoord days under Slot (now at Liverpool). The tactical adaptation is zero.",
            "At 32m, he's nearly HALF the price of Livramento with arguably better tactical fit. "
            "His positional intelligence is his superpower — he always knows where to be. In a 60-game "
            "season, having a player who can cover 3 positions without drop-off is worth 30m in depth "
            "you don't have to buy separately.",
            "Dutch international alongside Timber means national team chemistry already exists on the "
            "right side. His 87% pass completion and 32 progressive passes from RB are strong for "
            "a defender — he'd maintain Arsenal's build-up quality from the right.",
            "Feyenoord under Slot played a system VERY similar to Arteta's — positional play, high press, "
            "build from the back. Geertruida was the best player in that system. Direct translation."
        ],
        why_wont_work=[
            "He's NOT a pace merchant. Against Luis Diaz, Son, Grealish — rapid wingers who run in "
            "behind — Geertruida could get exposed in transition. Arsenal's high line DEMANDS recovery "
            "pace. This is his one clear and potentially fatal limitation at PL level.",
            "His attacking output (3 goals, 4 assists) is solid but not game-changing. He won't create "
            "moments of individual magic the way Livramento or Vanderson might. Against deep blocks, "
            "Arsenal need fullbacks who can produce from open play — Geertruida is more functional "
            "than spectacular.",
            "Leipzig's Bundesliga system is slower-paced than the PL. The intensity jump, the physical "
            "battles in wide areas, the speed of counter-attacks — all significantly higher in England. "
            "Smart positioning compensates for some of that, but not all.",
            "If Timber stays fit (which he has this season — 23 apps), Geertruida might never start "
            "in the PL. Spending 32m on a player who's primarily your cup/rotation RB is a lot when "
            "Ben White is still at the club doing exactly that role."
        ],
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
        role_in_squad="rotation",
        why_works=[
            "Pure chaos on the right flank. When Arsenal face deep blocks (70% of their games), they "
            "need someone who can dribble past players and create something from nothing. 26 dribbles "
            "completed and 55 progressive carries make him an elite ball-progressor from fullback.",
            "At 28m from a selling club, the financial risk is minimal. He's only 23 — massive "
            "development runway. His 6 assists show end product, not just empty dribbles. His attacking "
            "profile gives Arteta a tactical option he currently lacks: a fullback who STAYS WIDE and "
            "overlaps rather than inverts. Against certain opponents, that width is devastating.",
            "Different profile to Timber — when opposition prepare for the inverting fullback all week "
            "and Arsenal switch to Vanderson's overlapping runs, it's a tactical curveball. Arteta "
            "loves having multiple systems available."
        ],
        why_wont_work=[
            "Ligue 1 to PL is a HUGE jump for a defender. The defensive intensity, physicality, and "
            "speed of transition in the PL would be a culture shock. His defensive positioning is still "
            "raw — at Monaco, he gets away with it in a lower-quality league. Against Salah, Palmer, "
            "Saka-level wingers, his 1v1 defending would be brutally exposed.",
            "82% pass completion is BELOW Arsenal's standards for a fullback in possession. Arteta's "
            "build-up demands precision — when the RB receives under pressure, every pass must find "
            "its target. Vanderson's technique is attack-first, defend/pass-second. That's backwards "
            "for Arteta.",
            "Could be a liability in big games where defensive solidity matters more than attacking "
            "flair. Imagine Arsenal 1-0 up at Anfield with 10 minutes left — do you trust Vanderson "
            "to defend that lead? That's the question Arteta would ask."
        ],
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
        role_in_squad="starter",
        why_works=[
            "ALREADY PL-PROVEN. This cannot be overstated — he knows what it takes to defend against "
            "Salah, Palmer, Saka EVERY WEEK. Zero adaptation period. His transition play is exactly what "
            "Arteta wants from a LB when Arsenal counter — explosive forward runs that turn defence into "
            "attack in 3 seconds.",
            "The anti-Zinchenko. Where Zinchenko was silky on the ball but a liability defending, "
            "Kerkez is reliable at the back AND dynamic going forward. 32 tackles won shows he relishes "
            "the physical battle. He'd give Calafiori genuine competition AND cover his injury niggles.",
            "The Calafiori-Kerkez rotation gives Arsenal two different LB profiles — one for possession "
            "dominance (Calafiori: technically superior, inverts), one for transitions and defensive "
            "solidity (Kerkez: pace, aggression, direct). That tactical flexibility is worth 35m alone.",
            "At 35m from Bournemouth, this is a clean, realistic deal with no bidding war drama. "
            "Bournemouth sell to big clubs regularly — the pathway is smooth."
        ],
        why_wont_work=[
            "His technical ceiling worries you. Arteta's LB needs to play intricate combinations in "
            "tight spaces — Kerkez is more of a 'get it and drive' player. His crossing accuracy is "
            "inconsistent, which matters when Arsenal's left-side overloads demand precise final balls.",
            "At Bournemouth he has freedom to bomb forward. At Arsenal, the LB role is more structured "
            "and positionally complex — when to overlap, when to invert, when to hold the half-space. "
            "Can he handle Arteta's tactical demands? Bournemouth's system asks him to run; "
            "Arsenal's system asks him to THINK and run.",
            "Multiple PL clubs interested means the price could inflate to 40-45m, where the value "
            "proposition weakens. At 35m he's a great deal; at 45m you start questioning whether "
            "you're overpaying for a player who isn't a clear upgrade on Calafiori.",
            "His 82.5% pass completion is the lowest of any LB Arsenal would consider. In Arteta's "
            "build-up, the LB is critical to ball progression — if Kerkez misplaces passes under "
            "press, it disrupts the entire left-side structure."
        ],
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
        role_in_squad="starter",
        why_works=[
            "La Masia pedigree means the technical ability is INNATE. He's been drilled in Barcelona's "
            "positional play since childhood — and Arteta's system IS positional play, descended from "
            "the Cruyff/Guardiola/Barca tree. Balde already understands half-spaces, third-man "
            "combinations, positional rotations. The tactical language is shared.",
            "His pace is elite (one of the fastest LBs in Europe) — perfect for Arsenal's high-line "
            "recovery. Spain international at 22 means he handles the biggest stages. If Barcelona "
            "NEED to sell for FFP, Arsenal could get a 55m+ player for 38m — the kind of market "
            "inefficiency smart sporting directors exploit.",
            "CL knockout experience at 22 for Barcelona — he's played in the cauldron. Arsenal's "
            "ambition is to WIN the Champions League. You need players who've been there before.",
            "His combination of pace + technique is extremely rare at LB. He can overlap at speed AND "
            "play intricate combinations when he arrives in the final third. That's both dimensions "
            "of Arteta's LB role covered in one player."
        ],
        why_wont_work=[
            "ACL in 2024. Full stop. Arsenal already have Calafiori and Timber who've had injury issues. "
            "Building a squad on players with serious injury histories at 22 is reckless. The medical "
            "risk alone should give the recruitment team sleepless nights.",
            "His defensive positioning is genuinely POOR. At Barcelona, the fullbacks are protected by "
            "the midfield structure. At Arsenal, when Rice carries forward, the LB is often the last "
            "line of defence. Balde gets beaten too easily in 1v1 defensive situations — the PL's "
            "elite wingers would feast on that.",
            "Barcelona might NOT sell. They might find FFP workarounds, leaving Arsenal having wasted "
            "an entire summer in negotiations while Kerkez signs for Liverpool. The opportunity cost "
            "of a collapsed deal is months of lost time and missed alternatives.",
            "38m for a player with an ACL history and defensive positioning issues is a gamble. Kerkez "
            "at 35m with PL-proven defensive solidity and no injury concerns is objectively safer."
        ],
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
        role_in_squad="rotation",
        why_works=[
            "The most underrated midfielder in England. 91% pass completion from a deep-lying role — "
            "that's ZUBIMENDI territory. PL proven, English (homegrown quota), and he ALREADY understands "
            "the intensity of English football. Zero adaptation risk. Zero settling-in period.",
            "His metronomic passing would give Arsenal a different midfield option — when Zubimendi is "
            "rested, Wharton steps in and the system doesn't lose tempo. Palace under Glasner play a "
            "system that demands their #6 to be press-resistant — that's directly transferable to Arteta.",
            "At 42m, he's cheaper than Bouaddi with significantly less risk. The homegrown advantage "
            "shouldn't be underestimated — Arsenal need to balance their foreign player quota for CL "
            "and PL registration. An English CM solves a regulatory problem AND a football problem.",
            "At 22, his development arc is still steep. He's not the finished article — but he's already "
            "playing at a level that would be immediately useful. The gap between his current level "
            "and Arsenal's requirement is small enough to close within one season."
        ],
        why_wont_work=[
            "ZERO goal threat. 1 goal in 22 games. Arteta's midfielders are expected to arrive in "
            "the box — Rice has 4 goals, Zubimendi has 4, Merino has 4. Against deep blocks, you need "
            "midfielders who crash the box as an extra body. Wharton doesn't have that in his game.",
            "His physicality is a concern at the very top level. The Caicedos, Rices, and Bissoumas "
            "of the PL would physically bully him in duels. The step up from Palace-level midfield "
            "battles to Arsenal-level (where you face City's and Liverpool's press) is enormous.",
            "Palace is not Arsenal — the step up in expectation, pressure, tactical complexity, and "
            "scrutiny is massive. He's never played in Europe. And 42m is a lot for a backup who "
            "doesn't start over Zubimendi, Rice, or Odegaard on current form.",
            "His progressive carrying (20) is limited compared to what Arsenal demand. Rice carries "
            "the ball 145 times — Wharton's game is pass-first. In the PL, sometimes you need to "
            "carry through the press, not just pass through it."
        ],
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
        role_in_squad="starter",
        why_works=[
            "The most 'ready-made' CM option. At 26, peak age, zero development needed. His ball-winning "
            "(42 tackles, 28 interceptions) is ELITE. In games where Arsenal need to be combative — "
            "NLD, away at Anfield, CL knockout legs — Ederson adds a physical dimension the midfield "
            "sometimes lacks. Think of the Rice-Ederson double pivot for big away games.",
            "He's basically a Declan Rice clone. Arteta could deploy a Rice-Ederson double pivot in "
            "tough away games while pushing Odegaard higher as a free #10. That tactical flexibility "
            "— to go from 4-3-3 to a 4-2-3-1 mid-game — is something Arsenal currently can't do "
            "without losing midfield quality.",
            "Europa League winner with Atalanta. Gasperini's system demands insane physical output "
            "from every midfielder — 12km+ per game. He's built for the PL's physical demands. "
            "His 4 goals from CM shows he's not just a destroyer — he arrives in the box.",
            "At 26, he's immediately impactful. No waiting, no development, no risk of PL shock. "
            "Arsenal buy him in June, he starts in August. That certainty has value."
        ],
        why_wont_work=[
            "50m for a 26-year-old CM with limited resale value is fiscally irresponsible when you "
            "could spend that on Bouaddi (who has 10x the resale potential at 18). Arsenal's model "
            "should be buying assets that appreciate, not peak-age players who depreciate from day one.",
            "His passing (87% completion) ISN'T at the level Arsenal demand from their midfielders. "
            "Zubimendi is 91.5%, Wharton is 91%. In Arteta's possession system, every midfielder must "
            "be press-resistant and technically precise — Ederson is more 'win it and give it simple'. "
            "That works at Atalanta; it might not at Arsenal.",
            "He DUPLICATES what Arsenal already have in Rice. Do you really need TWO ball-carrying "
            "physical CMs? The system needs creativity and tempo control more than combativeness. "
            "Buying another Rice is solving a problem Arsenal don't have.",
            "Serie A to PL adaptation is unpredictable. The speed of play, the intensity of pressing, "
            "the aerial challenge in midfield — all significantly higher in England. Many excellent "
            "Serie A midfielders have taken 6-12 months to adjust. Arsenal can't afford that in a title race."
        ],
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
        role_in_squad="rotation",
        why_works=[
            "The most versatile of the AM options — AM, LW, RW. Arteta craves multi-positional players "
            "because it allows mid-game tactical shifts WITHOUT substitutions. Need to rest Saka on "
            "the right? Doue covers. Odegaard cramps at 70min? Doue drops into the #10. That flexibility "
            "across a 60-game season is invaluable.",
            "His dribbling in tight spaces is reminiscent of a young Bernardo Silva — and Arteta knows "
            "EXACTLY what Bernardo brings from his City days. Against packed defences, players who can "
            "receive, turn, and create in 2 square metres are golden. Doue has that.",
            "Olympic gold medalist at 20 shows mentality and big-game nerve. At PSG, he's learning "
            "from Dembele, one of the best dribblers in the world. If PSG don't give him minutes, "
            "a loan with option is possible — low-risk, high-reward structure.",
            "French market pathway that Arsenal know well. Their scouting network in France (Saliba, "
            "Bouaddi links) means they have detailed intelligence on Doue's character, training habits, "
            "and adaptability. No blind spots."
        ],
        why_wont_work=[
            "End product. 3 goals and 4 assists in 22 games is NOT enough for a creative player at "
            "Arsenal's level. Eze has similar numbers and he's been inconsistent. In the PL, you need "
            "decisive moments in tight games — Doue hasn't shown he can produce them yet.",
            "Physical development for the PL is a genuine concern. Ligue 1 and PL are different planets "
            "physically. The midfield combat zone in England — where tackles fly in, shirts are pulled, "
            "and referees let it go — would be a shock to a player who's been protected in France.",
            "PSG may not sell permanently, and a loan doesn't build squad equity. At 38m as a permanent "
            "deal, the risk-reward is worse than Guler (more talented, loan option) and Kubo (more "
            "proven output, cheaper). Doue falls in an awkward middle ground.",
            "Could easily be another Pepe — technically skilled French winger who can't adapt to PL "
            "intensity. Arsenal paid 72m for that lesson. The parallels are uncomfortable."
        ],
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
        role_in_squad="rotation",
        why_works=[
            "The most PROVEN of the three AM options. 6 goals, 5 assists in 24 games at Real Sociedad — "
            "he's performing NOW, not in potential. His 32 dribbles completed and 30 key passes are the "
            "BEST of any AM target by a distance. This isn't projection — it's output.",
            "At 35m, he's the cheapest AM option while arguably being the most productive. Arsenal scouted "
            "him extensively in 2025 — they know exactly what he brings. Former Barca/Real Madrid youth "
            "means he understands elite environments and handles pressure.",
            "His work rate has improved significantly at Sociedad under Imanol's pressing system — "
            "this directly addresses the 'defensive contribution' concern. He's not the lazy luxury "
            "player people assume. The pressing data backs it up.",
            "Can play RW or AM, giving backup to both Saka and Odegaard — the two most important "
            "attacking players in the squad. When Saka needs rest (he's played too many minutes), "
            "Kubo on the right maintains creativity. That insurance is worth 35m."
        ],
        why_wont_work=[
            "At 1.73m, the PL physicality is a genuine concern. Centre-backs in England are bigger, "
            "faster, and more aggressive than in La Liga. Santi Cazorla made it work, but he's the "
            "exception not the rule. The physical mismatch in aerial duels, shoulder challenges, and "
            "50-50s could nullify his technical advantage.",
            "La Liga to PL is a significant adaptation — the speed of play, the aerial challenge, the "
            "refereeing style (less protection for technical players). Many La Liga creators have "
            "struggled: Coutinho, Hazard post-Chelsea, etc. The transition is not guaranteed.",
            "His defensive contribution IS limited despite improvements. Can Arteta trust him in a "
            "system where EVERY player must press? When Arsenal are 1-0 up and defending a lead, "
            "can Kubo do the dirty work? That question mark lingers.",
            "At 24, his development curve is flattening — what you see is what you get. Is a 35m "
            "squad player who might not start really worth it when Arsenal already have Eze and "
            "Nwaneri for AM backup? The positional overlap could create a selection headache."
        ],
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
        role_in_squad="starter",
        why_works=[
            "The most physically impressive striker target. 1.95m with GENUINE PACE — that combination "
            "is almost impossible to find in world football. 14 goals in 24 games shows consistent "
            "finishing. Arsenal were very close in 2024 — the relationship and trust already exist.",
            "His release clause (65m) means NO protracted negotiations — pay it and he's yours by "
            "July 1st. In big games, having a Plan B of 'launch it to the 6'5 striker who runs a "
            "4.7s 40-yard dash' is incredibly valuable. Deep-defending teams who pack the box against "
            "Arsenal's patient build-up would HATE facing Sesko's directness.",
            "The Haaland comparison isn't unfair — similar body type, similar trajectory. At 23, his "
            "development runway is massive. If Gyokeres struggles to adapt (the xG gap is alarming), "
            "Sesko becomes the starter AND Arsenal have a 100m+ asset.",
            "His pressing numbers are strong for a big man — he covers ground and wins the ball high. "
            "Arteta demands front-press triggers; Sesko has the engine and aggression to execute them."
        ],
        why_wont_work=[
            "Link-up play STILL developing. Arteta's system demands the #9 to be involved in build-up — "
            "dropping deep, combining with Odegaard, playing one-twos in the final third. Sesko's game "
            "is more direct: run in behind, win the aerial, finish. That's valuable but it's NOT what "
            "Arsenal's primary system needs. His 10 key passes in 24 games is very low.",
            "65m on a SECOND striker when Gyokeres is already there on 200k/week is enormous. The risk "
            "of creating an unhappy dressing room — two expensive #9s fighting for one shirt — is real. "
            "Managing egos costs more than managing budgets. Ask Guardiola about Aguero/Dzeko dynamics.",
            "Leipzig's system FLATTERS strikers — open, transition-heavy, counter-attacking football "
            "with lots of space in behind. The PL defending Sesko would face is completely different: "
            "compact, organised, physical. His conversion rate in tight spaces is untested.",
            "Big-club pressure is different. At Leipzig, there's no expectation to win the league. "
            "At Arsenal, every game matters. Young strikers can freeze — Gyokeres' own early struggles "
            "prove that PL pressure affects finishing. Sesko at 65m facing that same pressure is a risk."
        ],
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
        role_in_squad="rotation",
        why_works=[
            "FREE. TRANSFER. In a market where mediocre players cost 50m, getting a proven 15-goal-a-season "
            "striker for ZERO transfer fee is the best value proposition in football. That 50-65m saved "
            "can fund a CB AND a LW. Arsenal's budget stretches to cover all squad gaps.",
            "David's movement is intelligent — he finds space between defenders in a way that's eerily "
            "similar to Thierry Henry's (smaller scale). His pressing from the front is excellent — "
            "Lille's system demands it. He's scored 15+ goals for 5 CONSECUTIVE seasons — this isn't "
            "a one-season wonder, it's a proven elite-level output machine.",
            "Even as the #2 striker behind Gyokeres, his goal record means he'd contribute 10-15 goals "
            "from rotation, cups, and substitute appearances. That's the difference between winning "
            "the league by 2 points or losing it.",
            "At 26, he's entering his prime. Clinical finishing is the one quality Arsenal's attack "
            "lacks (Gyokeres: 33% shot accuracy vs David's 50%). David off the bench at 70min against "
            "a tired defence is a devastatingly effective plan."
        ],
        why_wont_work=[
            "The competition for him is ENORMOUS — Barcelona, Man Utd, Juventus all want him. As a "
            "free agent, the player holds ALL the cards. David might choose Barca for prestige, Juve "
            "for lifestyle, or Utd for wages. Arsenal may simply lose the personal terms battle.",
            "Free agent wage demands are astronomical — agents demand 300k+ signing bonuses, image "
            "rights packages, and inflated weekly wages. The 'free transfer' label is misleading: "
            "total cost with signing bonus, agent fees, and 140k/week wages over 4 years is still "
            "50m+. It's free upfront, not free overall.",
            "He's not the most physically imposing at 5'11 — in the PL, against Saliba-types, he'd "
            "struggle in aerial duels. Arteta's system often uses the #9 as a target for crosses and "
            "set-pieces. David doesn't give you that aerial dimension.",
            "Is he actually BETTER than Gyokeres? If not, you're paying 140k/week for a backup who "
            "might not be happy on the bench. Ligue 1 records don't always translate — many Ligue 1 "
            "strikers have flopped in the PL (Lacazette's decline, Remy, Batshuayi)."
        ],
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
        role_in_squad="starter",
        why_works=[
            "The COMPLETE LW package. Goals (7), assists (8), dribbling (36 completed), pace, "
            "physicality — he does EVERYTHING. Euro 2024 star alongside Yamal means he thrives on "
            "the absolute biggest stages. When Martinelli has 3G+2A all season and Williams has "
            "7G+8A, the upgrade is massive and immediate.",
            "In Arteta's system, the LW cuts inside while the LB overlaps — Williams does exactly "
            "this at Athletic Bilbao, and he does it at the highest level in La Liga AND "
            "international football. The tactical fit is perfect. His physical profile "
            "(pace + strength) suits the PL — he wouldn't be pushed off the ball like smaller wingers.",
            "Release clause (58m) is set — no negotiation theatre, no bidding war, no protracted "
            "summer saga. Arsenal pay 58m and it's done by June. Barcelona tried and FAILED in 2024, "
            "proving the clause CAN be triggered. He'd immediately become the best LW Arsenal have "
            "had since peak Alexis Sanchez.",
            "At 24, he's entering his prime with 8+ years of elite football ahead. His 74 Squawka "
            "and 7.5 FotMob ratings are the highest of ANY transfer target on the list."
        ],
        why_wont_work=[
            "His emotional attachment to Athletic Bilbao is REAL — he grew up there, his brother Inaki "
            "is a club legend, the Basque identity runs deep. He turned down Barcelona. Arsenal may "
            "simply not be able to convince him to leave San Mames for the Emirates. You can trigger "
            "the clause, but you can't force him to sign.",
            "58m release clause + 150k/week wages + agent fees = 90m+ total investment on a position "
            "where Arteta could find a cheaper solution (Adeyemi at 65m WANTS to come; Bakayoko at "
            "42m is an exciting alternative). The opportunity cost of overspending on LW is starving "
            "the CB or CM budget.",
            "Williams is at his BEST driving at defenders in open space — transition football suits "
            "him. Against deep blocks, where Arsenal spend 70% of their time, is his game as effective? "
            "Athletic Bilbao play more direct football. Arsenal's patient, positional build-up is a "
            "very different tactical environment.",
            "High wage demands could disrupt the wage structure. If Williams arrives on 150k+/week, "
            "Saka's camp will use it as leverage for a raise. The ripple effect of one marquee "
            "signing's wages through the squad is the hidden cost boards underestimate."
        ],
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
        role_in_squad="rotation",
        why_works=[
            "The analytics darling. 8 goals and 6 assists in 22 Eredivisie games at 22 — the trajectory "
            "is steep and accelerating. Right-footed on the left, he naturally cuts inside to shoot — "
            "EXACTLY what Arteta wants from his LW (create overloads left, cut inside, shoot or "
            "combine with the #10). The Martinelli replacement profile is perfect.",
            "Contract leverage (2027) gives PSV selling pressure — 40-45m is realistic. At that price, "
            "Arsenal get a high-ceiling winger AND preserve budget for CB, RB, and CM. That's the "
            "financial smartness that separates good windows from great ones.",
            "Belgium international at 22 means he's played on big stages. His 30 dribbles completed "
            "and 45 progressive carries show he can beat players and progress the ball into the final "
            "third. His 6.5 xG is the highest of ANY LW target — the goal threat is real, not just "
            "Eredivisie inflation.",
            "At 22, the resale value is enormous. If he hits (think Salah at Roma → Liverpool), Arsenal "
            "have a 100m+ asset. If he's good-not-great, they recoup the 42m easily. The financial "
            "downside is capped; the upside is uncapped."
        ],
        why_wont_work=[
            "Eredivisie to PL is historically the HARDEST jump for attackers. Depay, Bergwijn, Janssen, "
            "Ziyech — the list of Eredivisie stars who flopped in England is longer than the successes. "
            "PSV's system gives attackers space, time, and weaker opposition. The PL gives you none of those.",
            "His defensive work rate is inconsistent — in Arteta's system, that's NON-NEGOTIABLE. When "
            "Arsenal lose the ball, the LW must become the first line of press on the opposition RB. "
            "If Bakayoko can't or won't do that consistently, he can't play for Arteta. Period.",
            "Decision-making is still maturing — at Arsenal, you get ONE chance in the final third, not "
            "three. The Eredivisie forgives bad decisions because you get the ball back quickly against "
            "weaker teams. In the PL, one wrong pass and you're defending a counter-attack.",
            "The 42m could be better spent on a proven PL attacker or a cheaper development option. "
            "Bakayoko sits in the awkward middle — too expensive for a gamble, not proven enough "
            "for certainty. For the same money, Arsenal could get a PL-proven player at another position."
        ],
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
