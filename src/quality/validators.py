import pandas as pd


def check_completeness(df: pd.DataFrame, cols: list[str]) -> dict:
    total = len(df)
    if total == 0:
        return {"score": 0.0, "detalles": {}}
    det = {}
    for c in cols:
        if c in df.columns:
            det[c] = round((1 - df[c].isnull().sum() / total) * 100, 1)
        else:
            det[c] = 0.0
    return {"score": round(sum(det.values()) / len(det), 1), "detalles": det}


def check_temporal_gaps(df: pd.DataFrame, country: str = "Peru") -> dict:
    sub = df[df["location"] == country].sort_values("date")
    if len(sub) < 2:
        return {"gaps": 0, "max_gap_days": 0}
    diffs = sub["date"].diff().dt.days
    gaps = (diffs > 1).sum()
    max_gap = int(diffs.max()) if not diffs.empty else 0
    return {"gaps": int(gaps), "max_gap_days": max_gap}


def run_quality_report(df: pd.DataFrame) -> dict:
    cols = ["location", "date", "new_cases", "new_deaths", "total_cases"]
    comp = check_completeness(df, cols)
    gaps = check_temporal_gaps(df)
    gap_penalty = min(gaps["gaps"] * 2, 30)
    total = max(0, comp["score"] - gap_penalty)
    return {
        "score_total": round(total, 1),
        "completitud": comp,
        "gaps_temporales": gaps,
        "filas": len(df),
    }
