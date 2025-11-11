import pandas as pd


def weekly_summary(df: pd.DataFrame) -> pd.DataFrame:
    weekly = (
        df.groupby(["location", "anio", "semana"])
        .agg(
            casos_semana=("new_cases", "sum"),
            muertes_semana=("new_deaths", "sum"),
            fecha_inicio=("date", "min"),
            fecha_fin=("date", "max"),
        )
        .reset_index()
    )
    return weekly


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby(["location", "anio", "mes"])
        .agg(
            casos_mes=("new_cases", "sum"),
            muertes_mes=("new_deaths", "sum"),
            casos_acum=("total_cases", "last"),
            muertes_acum=("total_deaths", "last"),
        )
        .reset_index()
    )
    return monthly


def case_fatality_rate(df: pd.DataFrame) -> pd.DataFrame:
    monthly = monthly_summary(df)
    mask = monthly["casos_acum"] > 0
    monthly.loc[mask, "tasa_letalidad"] = (
        monthly.loc[mask, "muertes_acum"] / monthly.loc[mask, "casos_acum"] * 100
    ).round(2)
    return monthly


def vaccination_progress(df: pd.DataFrame) -> pd.DataFrame:
    vax_cols = ["people_vaccinated", "people_fully_vaccinated", "total_vaccinations"]
    available = [c for c in vax_cols if c in df.columns]
    if not available:
        return pd.DataFrame()
    weekly = (
        df.groupby(["location", "anio", "semana"])[available]
        .last()
        .reset_index()
    )
    return weekly


def compare_latam(df: pd.DataFrame) -> pd.DataFrame:
    latest = df.sort_values("date").groupby("location").last().reset_index()
    cols = ["location", "total_cases_per_million", "total_deaths_per_million"]
    available = [c for c in cols if c in latest.columns]
    compare = latest[available].copy()
    if "total_deaths_per_million" in compare.columns:
        compare = compare.sort_values("total_deaths_per_million", ascending=False)
    return compare.reset_index(drop=True)


def wave_detection(df: pd.DataFrame, country: str = "Peru", threshold: float = 1.5) -> pd.DataFrame:
    sub = df[df["location"] == country].copy()
    if "new_cases_smoothed" not in sub.columns or sub.empty:
        return pd.DataFrame()

    sub = sub.sort_values("date")
    mean_cases = sub["new_cases_smoothed"].mean()
    if mean_cases == 0:
        return pd.DataFrame()

    sub["above_threshold"] = sub["new_cases_smoothed"] > mean_cases * threshold
    sub["wave_start"] = sub["above_threshold"] & ~sub["above_threshold"].shift(1, fill_value=False)

    waves = []
    wave_num = 0
    in_wave = False
    start_date = None

    for _, row in sub.iterrows():
        if row["wave_start"]:
            wave_num += 1
            in_wave = True
            start_date = row["date"]
        elif in_wave and not row["above_threshold"]:
            waves.append({
                "ola": wave_num,
                "inicio": start_date,
                "fin": row["date"],
                "pico_casos": sub[
                    (sub["date"] >= start_date) & (sub["date"] <= row["date"])
                ]["new_cases_smoothed"].max(),
            })
            in_wave = False

    return pd.DataFrame(waves)
