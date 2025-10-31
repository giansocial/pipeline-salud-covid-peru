import pytest
import pandas as pd
from src.load.warehouse import init_db, load_to_db


@pytest.fixture
def db(tmp_path):
    conn = init_db(tmp_path / "test.db")
    yield conn
    conn.close()


def _df():
    return pd.DataFrame({
        "location": ["Peru", "Peru"],
        "date": pd.to_datetime(["2020-03-06", "2020-03-07"]),
        "anio": [2020, 2020],
        "mes": [3, 3],
        "new_cases": [1, 0],
        "new_deaths": [0, 0],
        "total_cases": [1, 1],
        "total_deaths": [0, 0],
    })


def test_init_table(db):
    cur = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {r[0] for r in cur.fetchall()}
    assert "covid_diario" in tables


def test_load_inserts(db):
    assert load_to_db(_df(), db) == 2


def test_load_upsert(db):
    load_to_db(_df(), db)
    load_to_db(_df(), db)
    cur = db.execute("SELECT COUNT(*) FROM covid_diario")
    assert cur.fetchone()[0] == 2
