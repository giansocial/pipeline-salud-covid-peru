import pandas as pd
from src.transform.cleaner import clean_covid_data, fill_missing_daily


def _raw():
    return pd.DataFrame({
        "location": ["Peru"] * 3,
        "date": ["2020-03-06", "2020-03-07", "2020-03-08"],
        "new_cases": [1, 0, 2],
        "new_deaths": [0, 0, 0],
        "total_cases": [1, 1, 3],
        "total_deaths": [0, 0, 0],
    })


def test_clean_adds_temporal():
    df = clean_covid_data(_raw())
    assert "anio" in df.columns
    assert "mes" in df.columns
    assert df["anio"].iloc[0] == 2020


def test_clean_drops_dupes():
    df = _raw()
    df = pd.concat([df, df.iloc[:1]], ignore_index=True)
    cleaned = clean_covid_data(df)
    assert len(cleaned) == 3


def test_fill_missing():
    raw = pd.DataFrame({
        "location": ["Peru", "Peru"],
        "date": pd.to_datetime(["2020-03-06", "2020-03-09"]),
        "new_cases": [1, 5],
        "total_cases": [1, 10],
        "anio": [2020, 2020],
        "mes": [3, 3],
        "semana": [10, 11],
    })
    filled = fill_missing_daily(raw, "Peru")
    assert len(filled) == 4
    assert filled["total_cases"].iloc[1] == 1


def test_fill_missing_empty():
    raw = pd.DataFrame({
        "location": ["Peru"],
        "date": pd.to_datetime(["2020-03-06"]),
        "total_cases": [1],
        "anio": [2020], "mes": [3], "semana": [10],
    })
    filled = fill_missing_daily(raw, "Brazil")
    assert filled.empty
