import logging
import sqlite3
from pathlib import Path
import pandas as pd

from src.config.settings import DB_PATH

log = logging.getLogger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS covid_diario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,
    date TEXT NOT NULL,
    anio INTEGER,
    mes INTEGER,
    new_cases REAL,
    new_deaths REAL,
    total_cases REAL,
    total_deaths REAL,
    new_cases_smoothed REAL,
    total_cases_per_million REAL,
    total_deaths_per_million REAL,
    total_vaccinations REAL,
    people_vaccinated REAL,
    people_fully_vaccinated REAL,
    stringency_index REAL,
    reproduction_rate REAL,
    UNIQUE(location, date)
);

CREATE INDEX IF NOT EXISTS idx_covid_location ON covid_diario(location);
CREATE INDEX IF NOT EXISTS idx_covid_date ON covid_diario(date);
"""


def init_db(db_path: Path = None) -> sqlite3.Connection:
    db_path = db_path or DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def load_to_db(df: pd.DataFrame, conn: sqlite3.Connection) -> int:
    cols = [
        "location", "date", "anio", "mes", "new_cases", "new_deaths",
        "total_cases", "total_deaths", "new_cases_smoothed",
        "total_cases_per_million", "total_deaths_per_million",
        "total_vaccinations", "people_vaccinated", "people_fully_vaccinated",
        "stringency_index", "reproduction_rate",
    ]
    available = [c for c in cols if c in df.columns]
    placeholders = ",".join(["?"] * len(available))
    col_str = ",".join(available)

    loaded = 0
    for _, row in df.iterrows():
        values = []
        for c in available:
            v = row[c]
            if hasattr(v, "isoformat"):
                v = v.isoformat()
            elif pd.isna(v):
                v = None
            values.append(v)
        conn.execute(
            f"INSERT OR REPLACE INTO covid_diario ({col_str}) VALUES ({placeholders})",
            values,
        )
        loaded += 1

    conn.commit()
    log.info("cargados %d registros", loaded)
    return loaded
