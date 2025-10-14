import logging
import pandas as pd

from src.config.settings import INDICADORES

log = logging.getLogger(__name__)


def clean_covid_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df["anio"] = df["date"].dt.year
        df["mes"] = df["date"].dt.month
        df["semana"] = df["date"].dt.isocalendar().week.astype(int)

    base_cols = ["location", "date", "anio", "mes", "semana"]
    available = [c for c in INDICADORES if c in df.columns]
    cols = base_cols + available
    df = df[[c for c in cols if c in df.columns]]

    before = len(df)
    df = df.drop_duplicates(subset=["location", "date"])
    dupes = before - len(df)
    if dupes > 0:
        log.info("eliminados %d duplicados", dupes)

    return df.reset_index(drop=True)


def fill_missing_daily(df: pd.DataFrame, country: str) -> pd.DataFrame:
    sub = df[df["location"] == country].copy()
    if sub.empty:
        return sub
    date_range = pd.date_range(sub["date"].min(), sub["date"].max())
    sub = sub.set_index("date").reindex(date_range)
    sub.index.name = "date"
    sub["location"] = country

    cumulative = ["total_cases", "total_deaths", "total_vaccinations",
                  "people_vaccinated", "people_fully_vaccinated"]
    for col in cumulative:
        if col in sub.columns:
            sub[col] = sub[col].ffill()

    sub["anio"] = sub.index.year
    sub["mes"] = sub.index.month
    sub["semana"] = sub.index.isocalendar().week.astype(int)

    return sub.reset_index().rename(columns={"index": "date"})
