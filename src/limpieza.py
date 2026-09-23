"""
Limpieza e integración de los datasets de películas y series (StreamView Analytics).
Ejecutar desde la carpeta raíz del proyecto:  python src/limpieza.py
Genera: data/processed/catalogo.csv, generos.csv, paises.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- 1. Carga
peliculas = pd.read_csv(RAW / "netflix_movies_detailed_up_to_2025.csv")
series = pd.read_csv(RAW / "netflix_tv_shows_detailed_up_to_2025.csv")
print(f"Películas: {peliculas.shape} | Series: {series.shape}")

# ---------------------------------------------------------------- 2. Unificar formatos
# 'duration' está 100% vacía en películas y en series vale siempre "1 Seasons":
# no aporta información, se elimina.
peliculas = peliculas.drop(columns=["duration"])
series = series.drop(columns=["duration"])

# Las series no traen budget ni revenue: se crean vacíos para poder unir ambas tablas.
series["budget"] = np.nan
series["revenue"] = np.nan

df = pd.concat([peliculas, series], ignore_index=True)

# El show_id puede repetirse entre películas y series (IDs de TMDB distintos),
# por eso la clave única combina tipo + id.
df["id_unico"] = df["type"].str.replace(" ", "") + "_" + df["show_id"].astype(str)
antes = len(df)
df = df.drop_duplicates(subset="id_unico").reset_index(drop=True)
print(f"Duplicados eliminados: {antes - len(df)}")

# ---------------------------------------------------------------- 3. Tipos y faltantes
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
df["anio_agregado"] = df["date_added"].dt.year

# budget/revenue con valor 0 significan "dato no informado", no cero real.
for col in ["budget", "revenue"]:
    df[col] = df[col].replace(0, np.nan)

# Un rating de 0 con 0 votos es "sin calificación", no una mala calificación.
sin_votos = df["vote_count"] == 0
df.loc[sin_votos, ["rating", "vote_average"]] = np.nan

for col in ["director", "cast", "country", "genres", "description"]:
    df[col] = df[col].fillna("Sin dato")

# ---------------------------------------------------------------- 4. Estandarizar
df["type"] = df["type"].replace({"Movie": "Película", "TV Show": "Serie"})
df["country"] = df["country"].str.replace("United States of America", "United States", regex=False)

idiomas = {"en": "Inglés", "fr": "Francés", "ja": "Japonés", "ko": "Coreano",
           "es": "Español", "zh": "Chino", "hi": "Hindi", "de": "Alemán",
           "it": "Italiano", "pt": "Portugués"}
df["idioma"] = df["language"].map(idiomas).fillna("Otro")

df["genero_principal"] = df["genres"].str.split(",").str[0].str.strip()
df["pais_principal"] = df["country"].str.split(",").str[0].str.strip()

# ---------------------------------------------------------------- 5. Métricas derivadas
df["decada"] = (df["release_year"] // 10 * 10).astype(int).astype(str) + "s"
df["anios_hasta_agregado"] = df["anio_agregado"] - df["release_year"]
df["roi"] = (df["revenue"] - df["budget"]) / df["budget"]          # solo si hay ambos datos
df["nivel_popularidad"] = pd.qcut(df["popularity"], 4, labels=["Baja", "Media", "Alta", "Muy alta"])
df["calificacion_confiable"] = df["vote_count"] >= 100             # filtro para rankings

# ---------------------------------------------------------------- 6. Tablas largas (géneros y países múltiples)
def explotar(columna, nombre):
    tabla = df[["id_unico", "type", columna]].copy()
    tabla[columna] = tabla[columna].str.split(",")
    tabla = tabla.explode(columna)
    tabla[columna] = tabla[columna].str.strip()
    tabla = tabla[tabla[columna] != "Sin dato"].rename(columns={columna: nombre})
    return tabla

generos = explotar("genres", "genero")
paises = explotar("country", "pais")

# ---------------------------------------------------------------- 7. Guardar
df.to_csv(OUT / "catalogo.csv", index=False)
generos.to_csv(OUT / "generos.csv", index=False)
paises.to_csv(OUT / "paises.csv", index=False)

print(f"catalogo.csv: {df.shape} | generos.csv: {generos.shape} | paises.csv: {paises.shape}")
print(df[["rating", "budget", "revenue", "roi"]].isna().mean().round(2).to_string())