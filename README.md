# Pipeline Salud COVID - Peru

Soy Gian Cruz.

Pipeline que procesa datos de COVID-19 en Peru y Latinoamerica usando el dataset abierto de Our World in Data (OWID). Analiza la evolucion de la pandemia, tasa de letalidad, progreso de vacunacion, deteccion de olas y comparacion regional.

Peru fue el pais con la mayor tasa de mortalidad por COVID-19 per capita del mundo. Este proyecto documenta la cronologia de la pandemia en el pais y lo compara con sus vecinos de la region.

## Que hace

- Descarga el dataset OWID completo (o carga CSV local)
- Filtra datos de Peru y paises LATAM
- Limpia y rellena gaps temporales (forward fill en acumulados)
- Genera resumenes semanales y mensuales
- Calcula tasa de letalidad (CFR) mensual
- Rastrea progreso de vacunacion
- Detecta olas de COVID por umbral de casos suavizados
- Compara mortalidad per capita entre paises LATAM
- Carga a SQLite con indices

## Instalacion

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
# Descarga automatica de OWID
python -m src.pipeline

# Desde CSV local
python -m src.pipeline --source file --file data/raw/owid-covid-data.csv
```

## Tests

```bash
pytest tests/ -v
```

## Stack

- Python 3.10+
- requests + pandas
- SQLite
- pytest

## Estructura

```
pipeline-salud-covid-peru/
├── src/
│   ├── config/settings.py
│   ├── extract/owid_client.py
│   ├── transform/
│   │   ├── cleaner.py
│   │   └── enricher.py
│   ├── quality/validators.py
│   ├── load/warehouse.py
│   ├── utils/logger.py
│   └── pipeline.py
├── tests/
│   ├── fixtures/owid_sample.csv
│   └── ...
└── requirements.txt
```

---

## What it does

Pipeline processing COVID-19 data for Peru and Latin America using the Our World in Data open dataset. Analyzes pandemic evolution, case fatality rate, vaccination progress, wave detection, and regional comparison.

Peru had the highest COVID-19 mortality rate per capita worldwide. This project documents the pandemic timeline and compares it with regional peers.

---

## Fuentes de datos

| Fuente | Descripcion | Enlace |
|--------|-------------|--------|
| Our World in Data - COVID-19 | Dataset global de COVID-19 actualizado diariamente | [https://github.com/owid/covid-19-data](https://github.com/owid/covid-19-data) |
| OWID - Explorador COVID | Visualizacion interactiva de datos | [https://ourworldindata.org/coronavirus](https://ourworldindata.org/coronavirus) |
| MINSA - Datos Abiertos | Ministerio de Salud - casos positivos Peru | [https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa](https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa) |
| INS Peru | Instituto Nacional de Salud - vigilancia epidemiologica | [https://web.ins.gob.pe/](https://web.ins.gob.pe/) |
