"""Canonical team identity for the poll-of-polls.

Every source spells teams a little differently ("Cabo Verde"-style noise,
abbreviations, "Los Angeles Rams" vs "Rams", "Washington Commanders" vs
"Commanders"). Extraction therefore resolves each parsed string to a canonical
key from TEAMS, and any string that resolves to nothing is simply ignored.

The canonical keys are the full club names. `abbr` is the standard NFL
three-letter code, used for the compact widget in the blog post.
"""

from __future__ import annotations

# Canonical -> (abbr, conference, division)
TEAMS: dict[str, tuple[str, str, str]] = {
    "Arizona Cardinals": ("ARI", "NFC", "West"),
    "Atlanta Falcons": ("ATL", "NFC", "South"),
    "Baltimore Ravens": ("BAL", "AFC", "North"),
    "Buffalo Bills": ("BUF", "AFC", "East"),
    "Carolina Panthers": ("CAR", "NFC", "South"),
    "Chicago Bears": ("CHI", "NFC", "North"),
    "Cincinnati Bengals": ("CIN", "AFC", "North"),
    "Cleveland Browns": ("CLE", "AFC", "North"),
    "Dallas Cowboys": ("DAL", "NFC", "East"),
    "Denver Broncos": ("DEN", "AFC", "West"),
    "Detroit Lions": ("DET", "NFC", "North"),
    "Green Bay Packers": ("GB", "NFC", "North"),
    "Houston Texans": ("HOU", "AFC", "South"),
    "Indianapolis Colts": ("IND", "AFC", "South"),
    "Jacksonville Jaguars": ("JAX", "AFC", "South"),
    "Kansas City Chiefs": ("KC", "AFC", "West"),
    "Las Vegas Raiders": ("LV", "AFC", "West"),
    "Los Angeles Chargers": ("LAC", "AFC", "West"),
    "Los Angeles Rams": ("LAR", "NFC", "West"),
    "Miami Dolphins": ("MIA", "AFC", "East"),
    "Minnesota Vikings": ("MIN", "NFC", "North"),
    "New England Patriots": ("NE", "AFC", "East"),
    "New Orleans Saints": ("NO", "NFC", "South"),
    "New York Giants": ("NYG", "NFC", "East"),
    "New York Jets": ("NYJ", "AFC", "East"),
    "Philadelphia Eagles": ("PHI", "NFC", "East"),
    "Pittsburgh Steelers": ("PIT", "AFC", "North"),
    "San Francisco 49ers": ("SF", "NFC", "West"),
    "Seattle Seahawks": ("SEA", "NFC", "West"),
    "Tampa Bay Buccaneers": ("TB", "NFC", "South"),
    "Tennessee Titans": ("TEN", "AFC", "South"),
    "Washington Commanders": ("WAS", "NFC", "East"),
}

# Alternative spellings seen in the wild. Keys and values are upper-cased and
# stripped before lookup, so "L.A. Rams" and "la rams" collide as intended.
_ALIASES: dict[str, str] = {
    # Full-name variants
    "ARIZONA CARDINALS": "Arizona Cardinals",
    "ATLANTA FALCONS": "Atlanta Falcons",
    "BALTIMORE RAVENS": "Baltimore Ravens",
    "BUFFALO BILLS": "Buffalo Bills",
    "CAROLINA PANTHERS": "Carolina Panthers",
    "CHICAGO BEARS": "Chicago Bears",
    "CINCINNATI BENGALS": "Cincinnati Bengals",
    "CLEVELAND BROWNS": "Cleveland Browns",
    "DALLAS COWBOYS": "Dallas Cowboys",
    "DENVER BRONCOS": "Denver Broncos",
    "DETROIT LIONS": "Detroit Lions",
    "GREEN BAY PACKERS": "Green Bay Packers",
    "HOUSTON TEXANS": "Houston Texans",
    "INDIANAPOLIS COLTS": "Indianapolis Colts",
    "JACKSONVILLE JAGUARS": "Jacksonville Jaguars",
    "KANSAS CITY CHIEFS": "Kansas City Chiefs",
    "LAS VEGAS RAIDERS": "Las Vegas Raiders",
    "LOS ANGELES CHARGERS": "Los Angeles Chargers",
    "LOS ANGELES RAMS": "Los Angeles Rams",
    "MIAMI DOLPHINS": "Miami Dolphins",
    "MINNESOTA VIKINGS": "Minnesota Vikings",
    "NEW ENGLAND PATRIOTS": "New England Patriots",
    "NEW ORLEANS SAINTS": "New Orleans Saints",
    "NEW YORK GIANTS": "New York Giants",
    "NEW YORK JETS": "New York Jets",
    "PHILADELPHIA EAGLES": "Philadelphia Eagles",
    "PITTSBURGH STEELERS": "Pittsburgh Steelers",
    "SAN FRANCISCO 49ERS": "San Francisco 49ers",
    "SEATTLE SEAHAWKS": "Seattle Seahawks",
    "TAMPA BAY BUCCANEERS": "Tampa Bay Buccaneers",
    "TENNESSEE TITANS": "Tennessee Titans",
    "WASHINGTON COMMANDERS": "Washington Commanders",
    # City-only and nickname-only forms
    "ARIZONA": "Arizona Cardinals",
    "CARDINALS": "Arizona Cardinals",
    "ATLANTA": "Atlanta Falcons",
    "FALCONS": "Atlanta Falcons",
    "BALTIMORE": "Baltimore Ravens",
    "RAVENS": "Baltimore Ravens",
    "BUFFALO": "Buffalo Bills",
    "BILLS": "Buffalo Bills",
    "CAROLINA": "Carolina Panthers",
    "PANTHERS": "Carolina Panthers",
    "CHICAGO": "Chicago Bears",
    "BEARS": "Chicago Bears",
    "CINCINNATI": "Cincinnati Bengals",
    "BENGALS": "Cincinnati Bengals",
    "CLEVELAND": "Cleveland Browns",
    "BROWNS": "Cleveland Browns",
    "DALLAS": "Dallas Cowboys",
    "COWBOYS": "Dallas Cowboys",
    "DENVER": "Denver Broncos",
    "BRONCOS": "Denver Broncos",
    "DETROIT": "Detroit Lions",
    "LIONS": "Detroit Lions",
    "GREEN BAY": "Green Bay Packers",
    "PACKERS": "Green Bay Packers",
    "HOUSTON": "Houston Texans",
    "TEXANS": "Houston Texans",
    "INDIANAPOLIS": "Indianapolis Colts",
    "COLTS": "Indianapolis Colts",
    "JACKSONVILLE": "Jacksonville Jaguars",
    "JAGUARS": "Jacksonville Jaguars",
    "JAGS": "Jacksonville Jaguars",
    "KANSAS CITY": "Kansas City Chiefs",
    "CHIEFS": "Kansas City Chiefs",
    "LAS VEGAS": "Las Vegas Raiders",
    "RAIDERS": "Las Vegas Raiders",
    "LOS ANGELES CHARGERS": "Los Angeles Chargers",
    "LA CHARGERS": "Los Angeles Chargers",
    "L.A. CHARGERS": "Los Angeles Chargers",
    "CHARGERS": "Los Angeles Chargers",
    "LOS ANGELES RAMS": "Los Angeles Rams",
    "LA RAMS": "Los Angeles Rams",
    "L.A. RAMS": "Los Angeles Rams",
    "RAMS": "Los Angeles Rams",
    "MIAMI": "Miami Dolphins",
    "DOLPHINS": "Miami Dolphins",
    "MINNESOTA": "Minnesota Vikings",
    "VIKINGS": "Minnesota Vikings",
    "NEW ENGLAND": "New England Patriots",
    "PATRIOTS": "New England Patriots",
    "PATS": "New England Patriots",
    "NEW ORLEANS": "New Orleans Saints",
    "SAINTS": "New Orleans Saints",
    "NEW YORK GIANTS": "New York Giants",
    "NY GIANTS": "New York Giants",
    "GIANTS": "New York Giants",
    "NEW YORK JETS": "New York Jets",
    "NY JETS": "New York Jets",
    "JETS": "New York Jets",
    "PHILADELPHIA": "Philadelphia Eagles",
    "EAGLES": "Philadelphia Eagles",
    "PITTSBURGH": "Pittsburgh Steelers",
    "STEELERS": "Pittsburgh Steelers",
    "SAN FRANCISCO": "San Francisco 49ers",
    "49ERS": "San Francisco 49ers",
    "NINERS": "San Francisco 49ers",
    "SF 49ERS": "San Francisco 49ers",
    "SEATTLE": "Seattle Seahawks",
    "SEAHAWKS": "Seattle Seahawks",
    "TAMPA BAY": "Tampa Bay Buccaneers",
    "BUCCANEERS": "Tampa Bay Buccaneers",
    "BUCS": "Tampa Bay Buccaneers",
    "TENNESSEE": "Tennessee Titans",
    "TITANS": "Tennessee Titans",
    "WASHINGTON": "Washington Commanders",
    "COMMANDERS": "Washington Commanders",
    "WASHINGTON FOOTBALL TEAM": "Washington Commanders",
    # Abbreviations
    "ARI": "Arizona Cardinals",
    "ATL": "Atlanta Falcons",
    "BAL": "Baltimore Ravens",
    "BUF": "Buffalo Bills",
    "CAR": "Carolina Panthers",
    "CHI": "Chicago Bears",
    "CIN": "Cincinnati Bengals",
    "CLE": "Cleveland Browns",
    "DAL": "Dallas Cowboys",
    "DEN": "Denver Broncos",
    "DET": "Detroit Lions",
    "GB": "Green Bay Packers",
    "GNB": "Green Bay Packers",
    "HOU": "Houston Texans",
    "IND": "Indianapolis Colts",
    "JAX": "Jacksonville Jaguars",
    "JAC": "Jacksonville Jaguars",
    "KC": "Kansas City Chiefs",
    "KAN": "Kansas City Chiefs",
    "LV": "Las Vegas Raiders",
    "LVR": "Las Vegas Raiders",
    "LAC": "Los Angeles Chargers",
    "LAR": "Los Angeles Rams",
    "LA": "Los Angeles Rams",
    "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings",
    "NE": "New England Patriots",
    "NWE": "New England Patriots",
    "NO": "New Orleans Saints",
    "NOR": "New Orleans Saints",
    "NYG": "New York Giants",
    "NYJ": "New York Jets",
    "PHI": "Philadelphia Eagles",
    "PIT": "Pittsburgh Steelers",
    "SF": "San Francisco 49ers",
    "SEA": "Seattle Seahawks",
    "TB": "Tampa Bay Buccaneers",
    "TAM": "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans",
    "WAS": "Washington Commanders",
    "WSH": "Washington Commanders",
}

# Order matters when scanning prose: longest names first so "Los Angeles Rams"
# is not clipped to "Los Angeles".
_CANONICAL_BY_LENGTH: list[str] = sorted(TEAMS, key=len, reverse=True)


def normalize(raw: str) -> str | None:
    """Resolve one raw team string to a canonical name, or None."""
    if not raw:
        return None
    key = " ".join(raw.replace("\u00a0", " ").split()).strip(" .,:;|()[]").upper()
    if key in _ALIASES:
        return _ALIASES[key]
    if key in TEAMS:
        return key
    # Retry without a leading ordinal or trailing record, e.g. "1. Seahawks (1-0)"
    for canonical in _CANONICAL_BY_LENGTH:
        if canonical.upper() in key:
            return canonical
    return None


def abbr(canonical: str) -> str:
    return TEAMS[canonical][0]


def division(canonical: str) -> tuple[str, str]:
    _, conf, div = TEAMS[canonical]
    return conf, div
