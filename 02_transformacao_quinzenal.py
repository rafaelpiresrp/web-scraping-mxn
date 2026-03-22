"""
Transformação dos dados do SNIIM:
- Consolida CSVs do scraping
- Calcula preço médio por quinzena e região
- Gera variação quinzenal (%) por produto
"""

import os
import re
import unicodedata

import numpy as np
import pandas as pd

# ── Configuração de caminhos ──────────────────────────────────────────────
PATH = "C:/Users/rafoliveira/Downloads/scraping-mxn/"
RAW_DIR = os.path.join(PATH, "raw_data/")
OUTPUT_DIR = os.path.join(PATH, "output/")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Parâmetros ────────────────────────────────────────────────────────────
REGIOES_PERMITIDAS = [
    "Distrito Federal", "Jalisco", "Michoacán",
    "Nayarit", "Nuevo León", "Puebla", "Sinaloa",
]

PRODUTOS_INTERESSE = [
    "Aguacate", "Calabacita", "Cebolla", "Cilantro", "Epazote", "Perejil",
    "Chayote", "Chile Anaheim", "Chile California", "Chile Bola", "Chile Caloro",
    "Chile Caribe", "Chile Cat", "Chile Chilaca", "Chile de Árbol fresco",
    "Chile Dulce", "Chile Habanero", "Chile Húngaro", "Chile Mirasol",
    "Chile Jalapeño", "Chile Pimiento morrón", "Chile Poblano",
    "Chile Puya fresco", "Chile Serrano", "Coliflor", "Durazno", "Ejote",
    "Guayaba", "Jitomate", "Lechuga", "Col", "Limón", "Manzana", "Melón",
    "Naranja", "Nopal", "Papa", "Papaya", "Pepino", "Pera", "Piña",
    "Plátano", "Sandía", "Tomate Verde", "Toronja", "Uva", "Zanahoria",
]

# ── 1. Leitura e consolidação dos CSVs ───────────────────────────────────
archivos = [f for f in os.listdir(RAW_DIR) if f.endswith(".csv")]
lista_df = []

for archivo in archivos:
    df_temp = pd.read_csv(os.path.join(RAW_DIR, archivo), thousands=",")
    df_temp = df_temp.drop([0])  # Remove cabeçalho duplicado da tabela HTML

    match = re.search(r"(.+)_\d{4}-\d{4}\.csv", archivo)
    if match is None:
        print(f"  ⚠ Nome fora do padrão, pulando: {archivo}")
        continue

    nombre_producto = unicodedata.normalize("NFC", match.group(1).replace("_", " "))
    df_temp["producto"] = nombre_producto
    lista_df.append(df_temp)

if not lista_df:
    print("Nenhum CSV encontrado em", RAW_DIR)
    exit()

df = pd.concat(lista_df, ignore_index=True)
df.columns = df.columns.str.strip().str.lower()
df.rename(
    columns={
        "precio mín": "precio_min",
        "precio max": "precio_max",
        "precio frec": "precio_frec",
        "obs.": "observaciones",
    },
    inplace=True,
)
df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=True, format="%d/%m/%Y")

# ── 2. Filtros ────────────────────────────────────────────────────────────
df = df[df["origen"].isin(REGIOES_PERMITIDAS)].copy()

df["produto_base"] = df["producto"].apply(
    lambda x: next((p for p in PRODUTOS_INTERESSE if p in x), None)
)
df = df[df["produto_base"].notna()].copy()

# ── 3. Cálculos de quinzena e preço médio ────────────────────────────────
df["quinzena"] = df["fecha"].dt.day.apply(lambda x: 1 if x <= 15 else 2)
df["ano_mes"] = df["fecha"].dt.to_period("M")

for col in ["precio_min", "precio_max", "precio_frec"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["preco_medio"] = df[["precio_min", "precio_max", "precio_frec"]].mean(axis=1)

# ── 4. Agrupamento ───────────────────────────────────────────────────────
df_grouped = (
    df.groupby(["produto_base", "origen", "ano_mes", "quinzena"])["preco_medio"]
    .mean()
    .reset_index()
)

# ── 5. Export: preços por região (uma aba por produto) ────────────────────
output_precos = os.path.join(OUTPUT_DIR, "precos_produtos.xlsx")
with pd.ExcelWriter(output_precos) as writer:
    for produto in sorted(df_grouped["produto_base"].unique()):
        df_produto = df_grouped[df_grouped["produto_base"] == produto]
        df_pivot = df_produto.pivot_table(
            index=["ano_mes", "quinzena"], columns="origen", values="preco_medio"
        ).reset_index()
        # Limita nome da aba a 31 caracteres (limite do Excel)
        sheet_name = produto[:31]
        df_pivot.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"✔ Preços salvos em: {output_precos}")

# ── 6. Export: variação quinzenal (%) ─────────────────────────────────────
output_var = os.path.join(OUTPUT_DIR, "precos_variacao_quinzenal.xlsx")
with pd.ExcelWriter(output_var) as writer:
    for produto in sorted(df_grouped["produto_base"].unique()):
        df_produto = df_grouped[df_grouped["produto_base"] == produto]
        df_pivot = df_produto.pivot_table(
            index=["ano_mes", "quinzena"], columns="origen", values="preco_medio"
        )
        df_var = df_pivot.pct_change() * 100
        df_var.columns = [f"var_{col}" for col in df_var.columns]

        df_final = df_pivot.join(df_var)
        df_final["media_variacao"] = df_var.mean(axis=1)

        sheet_name = produto[:31]
        df_final.to_excel(writer, sheet_name=sheet_name)

print(f"✔ Variações salvas em: {output_var}")
print("\nProcessamento concluído!")

