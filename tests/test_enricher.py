import pandas as pd
import numpy as np
from src.transform.enricher import (
    weekly_summary, monthly_summary, case_fatality_rate,
    compare_latam, wave_detection,
)


def _peru_df():
    dates = pd.date_range("2020-03-01", periods=365, freq="D")
    np.random.seed(42)
    cases = np.random.poisson(5000, 365)
    deaths = np.random.poisson(100, 365)
    return pd.DataFrame({
        "location": "Peru",
        "date": dates,
        "anio": dates.year,
        "mes": dates.month,
        "semana": dates.isocalendar().week.astype(int),
        "new_cases": cases,
        "new_deaths": deaths,
        "total_cases": cases.cumsum(),
        "total_deaths": deaths.cumsum(),
        "new_cases_smoothed": pd.Series(cases).rolling(7).mean().fillna(0).values,
        "total_cases_per_million": cases.cumsum() / 33,
        "total_deaths_per_million": deaths.cumsum() / 33,
    })


def test_weekly_summary():
    df = _peru_df()
    weekly = weekly_summary(df)
    assert "casos_semana" in weekly.columns
    assert len(weekly) > 50


def test_monthly_summary():
    df = _peru_df()
    monthly = monthly_summary(df)
    assert "casos_mes" in monthly.columns
    assert len(monthly) == 12


def test_case_fatality_rate():
    df = _peru_df()
    cfr = case_fatality_rate(df)
    assert "tasa_letalidad" in cfr.columns


def test_compare_latam():
    df = pd.DataFrame({
        "location": ["Peru", "Brazil", "Chile"],
        "date": pd.to_datetime(["2023-01-01"] * 3),
        "total_cases_per_million": [135000, 160000, 120000],
        "total_deaths_per_million": [6675, 3200, 3100],
    })
    comp = compare_latam(df)
    assert len(comp) == 3
    assert comp["total_deaths_per_million"].iloc[0] >= comp["total_deaths_per_million"].iloc[-1]


def test_wave_detection():
    df = _peru_df()
    waves = wave_detection(df, "Peru", threshold=1.3)
    if not waves.empty:
        assert "ola" in waves.columns
        assert "pico_casos" in waves.columns


def test_wave_detection_empty():
    df = pd.DataFrame({
        "location": ["Peru"],
        "new_cases_smoothed": [100],
        "date": pd.to_datetime(["2020-03-01"]),
    })
    waves = wave_detection(df, "Peru")
    assert waves.empty
