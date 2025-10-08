from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
LOG_DIR = BASE_DIR / "logs"

for _d in (RAW_DIR, PROCESSED_DIR, LOG_DIR):
    _d.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "covid.db"

OWID_CSV_URL = (
    "https://raw.githubusercontent.com/owid/covid-19-data/"
    "master/public/data/owid-covid-data.csv"
)
OWID_TIMEOUT = 60

MINSA_DATOS_URL = "https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa"

PAISES_LATAM = [
    "Peru", "Brazil", "Chile", "Colombia", "Argentina",
    "Mexico", "Ecuador", "Bolivia", "Paraguay", "Uruguay",
]

INDICADORES = [
    "total_cases", "new_cases", "total_deaths", "new_deaths",
    "total_cases_per_million", "total_deaths_per_million",
    "new_cases_smoothed", "new_deaths_smoothed",
    "total_vaccinations", "people_vaccinated", "people_fully_vaccinated",
    "stringency_index", "reproduction_rate",
]
