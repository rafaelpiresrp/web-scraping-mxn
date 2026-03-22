# Scraping SNIIM - Preços Agrícolas do México

Web scraping de preços de frutas e hortaliças do [SNIIM](http://www.economia-sniim.gob.mx) (Sistema Nacional de Información e Integración de Mercados) do México.

## Scripts

| Arquivo | Descrição |
|---|---|
| `01_scraping_sniim.py` | Faz o scraping das tabelas de preços do SNIIM e salva CSVs por produto |
| `02_transformacao_quinzenal.py` | Consolida os CSVs, calcula preço médio e variação quinzenal por região |

## Configuração

Antes de rodar, ajuste o `PATH` nos dois scripts para o diretório desejado:

```python
PATH = "C:/Users/rafoliveira/Downloads/scraping-mxn/"
```

### Dependências

```
pip install pandas beautifulsoup4 openpyxl
```

## Como usar

```bash
# 1. Scraping (gera CSVs em raw_data/)
python 01_scraping_sniim.py

# 2. Transformação (gera Excel em output/)
python 02_transformacao_quinzenal.py
```

## Parâmetros do scraping

No script `01_scraping_sniim.py` você pode alterar:

- **`STR_FECHA_INICIO` / `STR_FECHA_FINAL`** — período de consulta (formato `dd/mm/aaaa`)
- **`PRECIOS_POR`** — `1` para apresentação comercial, `2` para kg calculado
- **`LISTA_PRODUCTOS`** — lista de produtos a buscar

## Output

- `raw_data/` — CSVs crus do scraping
- `output/precos_produtos.xlsx` — preço médio por quinzena e região (uma aba por produto)
- `output/precos_variacao_quinzenal.xlsx` — variação % quinzenal por região

## Nota

O site do SNIIM pode ficar instável. Se ocorrerem timeouts, tente reduzir o intervalo de datas.


- Requirements
  - Python 3.8 or higher
  - pandas
  - numpy
  - matplotlib
  - BeautifulSoup4 (for sniim_scraping.py)
