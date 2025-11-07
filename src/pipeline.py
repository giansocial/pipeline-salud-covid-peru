import argparse
import json
import logging
import time
from pathlib import Path

import pandas as pd

from src.config.settings import RAW_DIR, PROCESSED_DIR
from src.extract.owid_client import download_owid_csv, filter_country, filter_latam, load_from_file
from src.transform.cleaner import clean_covid_data, fill_missing_daily
from src.transform.enricher import (
    weekly_summary, monthly_summary, case_fatality_rate,
    vaccination_progress, compare_latam, wave_detection,
)
from src.quality.validators import run_quality_report
from src.load.warehouse import init_db, load_to_db
from src.utils.logger import get_logger

log = get_logger(__name__)


def run_pipeline(source: str = "download", filepath: Path = None) -> dict:
    t0 = time.time()

    if source == "file" and filepath:
        df = load_from_file(filepath)
    else:
        df = download_owid_csv()

    peru = filter_country(df, "Peru")
    latam = filter_latam(df)

    peru = clean_covid_data(peru)
    latam = clean_covid_data(latam)

    peru = fill_missing_daily(peru, "Peru")

    quality = run_quality_report(peru)
    log.info("calidad Peru: %.1f%%", quality["score_total"])

    conn = init_db()
    loaded_peru = load_to_db(peru, conn)
    loaded_latam = load_to_db(latam, conn)
    conn.close()

    weekly = weekly_summary(peru)
    weekly.to_csv(PROCESSED_DIR / "resumen_semanal.csv", index=False)

    monthly = case_fatality_rate(peru)
    monthly.to_csv(PROCESSED_DIR / "letalidad_mensual.csv", index=False)

    vax = vaccination_progress(peru)
    if not vax.empty:
        vax.to_csv(PROCESSED_DIR / "vacunacion.csv", index=False)

    comparison = compare_latam(latam)
    comparison.to_csv(PROCESSED_DIR / "comparacion_latam.csv", index=False)

    waves = wave_detection(peru)
    if not waves.empty:
        waves.to_csv(PROCESSED_DIR / "olas_covid.csv", index=False)

    elapsed = round(time.time() - t0, 1)
    log.info("pipeline completado en %.1fs", elapsed)

    return {
        "registros_peru": len(peru),
        "registros_latam": len(latam),
        "cargados": loaded_peru + loaded_latam,
        "calidad_pct": quality["score_total"],
        "olas_detectadas": len(waves),
        "duracion_seg": elapsed,
    }


def main():
    parser = argparse.ArgumentParser(description="Pipeline COVID Peru - OWID")
    parser.add_argument("--source", choices=["download", "file"], default="download")
    parser.add_argument("--file", type=Path, help="CSV local")
    args = parser.parse_args()
    result = run_pipeline(args.source, args.file)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
