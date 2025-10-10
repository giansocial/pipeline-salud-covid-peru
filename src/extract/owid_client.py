import logging
import time
import requests
import pandas as pd
from io import StringIO

from src.config.settings import OWID_CSV_URL, OWID_TIMEOUT, PAISES_LATAM

log = logging.getLogger(__name__)


def download_owid_csv(url: str = None, timeout: int = None) -> pd.DataFrame:
    url = url or OWID_CSV_URL
    timeout = timeout or OWID_TIMEOUT

    log.info("descargando OWID dataset...")
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()

    df = pd.read_csv(StringIO(resp.text))
    log.info("descargadas %d filas, %d columnas", len(df), len(df.columns))
    return df


def filter_country(df: pd.DataFrame, country: str = "Peru") -> pd.DataFrame:
    filtered = df[df["location"] == country].copy()
    log.info("%s: %d registros", country, len(filtered))
    return filtered.reset_index(drop=True)


def filter_latam(df: pd.DataFrame, countries: list[str] = None) -> pd.DataFrame:
    countries = countries or PAISES_LATAM
    filtered = df[df["location"].isin(countries)].copy()
    log.info("LATAM (%d paises): %d registros", len(countries), len(filtered))
    return filtered.reset_index(drop=True)


def load_from_file(filepath) -> pd.DataFrame:
    return pd.read_csv(filepath)
