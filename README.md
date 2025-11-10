# Pipeline Salud COVID - Perú

¿Sabías que Perú tuvo la tasa de mortalidad por COVID-19 más alta del mundo? Con más de 220,000 muertes oficiales en un país de 33 millones, la tasa de letalidad superó a la de cualquier otro país de Latinoamérica. Sin embargo, la velocidad de vacunación fue una de las más rápidas de la región una vez que arrancó la campaña.

Soy Gian Cruz. Construí este pipeline para procesar el dataset abierto de Our World in Data (OWID), filtrar datos de Perú y sus vecinos latinoamericanos, y generar análisis que no existen en los dashboards públicos: detección automática de olas por umbral de casos suavizados, tasa de letalidad mensual, comparación de mortalidad per cápita entre países LATAM y progreso de vacunación.

## Qué hace

- Descarga el dataset OWID completo (o carga CSV local)
- Filtra datos de Perú y países LATAM
- Limpia y rellena gaps temporales (forward fill en acumulados)
- Genera resúmenes semanales y mensuales
- Calcula tasa de letalidad (CFR) mensual
- Rastrea progreso de vacunación
- Detecta olas de COVID por umbral de casos suavizados
- Compara mortalidad per cápita entre países LATAM
- Carga a SQLite con índices

## Instalación

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

## Fuentes de datos

| Fuente | Descripción | Enlace |
|--------|-------------|--------|
| Our World in Data - COVID-19 | Dataset global de COVID-19 actualizado diariamente | [https://github.com/owid/covid-19-data](https://github.com/owid/covid-19-data) |
| OWID - Explorador COVID | Visualización interactiva de datos | [https://ourworldindata.org/coronavirus](https://ourworldindata.org/coronavirus) |
| MINSA - Datos Abiertos | Ministerio de Salud - casos positivos Perú | [https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa](https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa) |
| INS Perú | Instituto Nacional de Salud - vigilancia epidemiológica | [https://web.ins.gob.pe/](https://web.ins.gob.pe/) |

## Licencia

MIT

---

# COVID-19 Health Pipeline - Peru

Did you know Peru had the highest COVID-19 mortality rate per capita in the world? With over 220,000 official deaths in a country of 33 million, the case fatality rate exceeded every other Latin American country. Yet once the vaccination campaign launched, Peru's rollout was among the fastest in the region.

I'm Gian Cruz. I built this pipeline to process the Our World in Data (OWID) open dataset, filter data for Peru and its Latin American neighbors, and generate analyses not available in public dashboards: automatic wave detection by smoothed case threshold, monthly case fatality rate, per-capita mortality comparison across LATAM, and vaccination progress tracking.

## Quick start

```bash
git clone https://github.com/giansocial/pipeline-salud-covid-peru.git
cd pipeline-salud-covid-peru
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline --source download
```

## Data sources

| Source | Description | Link |
|--------|-------------|------|
| Our World in Data - COVID-19 | Global COVID-19 dataset updated daily | [https://github.com/owid/covid-19-data](https://github.com/owid/covid-19-data) |
| OWID - COVID Explorer | Interactive data visualization | [https://ourworldindata.org/coronavirus](https://ourworldindata.org/coronavirus) |
| MINSA - Open Data | Ministry of Health - positive cases Peru | [https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa](https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa) |

## License

MIT
