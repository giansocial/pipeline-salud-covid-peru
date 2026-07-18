import pandas as pd
from src.quality.validators import check_completeness, check_temporal_gaps, run_quality_report


def _df():
    return pd.DataFrame({
        "location": ["Peru", "Peru", "Peru"],
        "date": pd.to_datetime(["2020-03-06", "2020-03-07", "2020-03-08"]),
        "new_cases": [1, 0, 2],
        "new_deaths": [0, 0, 0],
        "total_cases": [1, 1, 3],
    })


def test_completeness():
    result = check_completeness(_df(), ["location", "new_cases"])
    assert result["score"] == 100.0


def test_temporal_no_gaps():
    result = check_temporal_gaps(_df())
    assert result["gaps"] == 0


def test_temporal_with_gap():
    df = pd.DataFrame({
        "location": ["Peru", "Peru"],
        "date": pd.to_datetime(["2020-03-06", "2020-03-10"]),
    })
    result = check_temporal_gaps(df)
    assert result["gaps"] == 1
    assert result["max_gap_days"] == 4


def test_quality_report():
    report = run_quality_report(_df())
    assert report["score_total"] > 0
    assert report["filas"] == 3
