# SNIIM Scraping - Mexican Agricultural Prices

Web scraping of fruit and vegetable prices from [SNIIM](http://www.economia-sniim.gob.mx) (Sistema Nacional de Información e Integración de Mercados), Mexico's national market information system.

## Scripts

| File | Description |
|---|---|
| `01_scraping_sniim.py` | Scrapes price tables from SNIIM and saves raw CSVs per product |
| `02_transformacao_quinzenal.py` | Consolidates CSVs, computes average prices and biweekly variation by region |

## Setup

Before running, update the `PATH` variable in both scripts to your desired directory:

```python
PATH = "C:/Users/rafoliveira/Downloads/scraping-mxn/"
```

### Dependencies

```
pip install -r requirements.txt
```

## Usage

```bash
# 1. Scraping (outputs CSVs to raw_data/)
python 01_scraping_sniim.py

# 2. Transformation (outputs Excel files to output/)
python 02_transformacao_quinzenal.py
```

## Scraping Parameters

In `01_scraping_sniim.py` you can adjust:

- **`STR_FECHA_INICIO` / `STR_FECHA_FINAL`** — query date range (format `dd/mm/yyyy`)
- **`PRECIOS_POR`** — `1` for commercial presentation, `2` for calculated kg
- **`LISTA_PRODUCTOS`** — list of products to scrape

## Output

- `raw_data/` — raw CSVs from scraping
- `output/precos_produtos.xlsx` — average price by biweekly period and region (one sheet per product)
- `output/precos_variacao_quinzenal.xlsx` — biweekly % variation by region

## Note

The SNIIM website can be unstable. If you experience timeouts, try reducing the date range.
