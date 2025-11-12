from pathlib import Path
from src.extract.owid_client import filter_country, filter_latam, load_from_file

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_from_file():
    df = load_from_file(FIXTURES / "owid_sample.csv")
    assert len(df) > 0
    assert "location" in df.columns


def test_filter_country():
    df = load_from_file(FIXTURES / "owid_sample.csv")
    peru = filter_country(df, "Peru")
    assert (peru["location"] == "Peru").all()
    assert len(peru) > 5


def test_filter_country_empty():
    df = load_from_file(FIXTURES / "owid_sample.csv")
    empty = filter_country(df, "Narnia")
    assert len(empty) == 0


def test_filter_latam():
    df = load_from_file(FIXTURES / "owid_sample.csv")
    latam = filter_latam(df, ["Peru", "Brazil", "Chile"])
    countries = latam["location"].unique()
    assert "Peru" in countries
    assert "Brazil" in countries
