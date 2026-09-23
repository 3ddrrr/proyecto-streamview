# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")# %% [markdown]
# # EDA — StreamView Analytics
# Audiencia: Gerente de Contenidos
# Pega este archivo en VS Code y ejecútalo por celdas (▷ Run Cell),
# o expórtalo a notebook con "Export as Jupyter Notebook" en la barra superior.

# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/processed/catalogo.csv")
generos = pd.read_csv("../data/processed/generos.csv")
paises = pd.read_csv("../data/processed/paises.csv")

TEMPLATE = "plotly_white"  # fondo limpio, sin grilla pesada

# %% [markdown]
# ## Pregunta 1: ¿Qué géneros tienen mejor recepción de audiencia?
# KPI para decidir en qué géneros invertir en adquisición.

# %%
g = generos.merge(df[["id_unico", "rating", "calificacion_confiable"]], on="id_unico")
g = g[g["calificacion_confiable"]]  # solo títulos con 100+ votos, para no distorsionar con muestras chicas
top_generos = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_generos.sort_values(),
    orientation="h",
    labels={"value": "Rating promedio", "genero": ""},
    title="Los géneros mejor evaluados por la audiencia",
)
fig1.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig1.update_traces(marker_color="#E50914")
fig1.show()

print(f"Hallazgo: '{top_generos.index[0]}' lidera con {top_generos.iloc[0]:.2f}/10, "
      f"por sobre géneros más masivos como Drama o Comedy.")

# %% [markdown]
# ## Pregunta 2: ¿Cómo ha evolucionado el catálogo agregado por año?
# Sirve para ver si el crecimiento de películas y series ha sido parejo.

# %%
evolucion = df.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")

fig2 = px.line(
    evolucion, x="anio_agregado", y="titulos", color="type",
    markers=True,
    labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
    title="Crecimiento del catálogo por año",
)
fig2.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig2.show()

print("Hallazgo: el catálogo crece a un ritmo estable de ~1.000 títulos por año "
      "en cada categoría, sin picos ni caídas relevantes.")

# %% [markdown]
# ## Pregunta 3: ¿Qué países concentran la producción de contenido?
# Ayuda a decidir en qué mercados priorizar futuras producciones.

# %%
top_paises = paises["pais"].value_counts().head(10).sort_values()

fig3 = px.bar(
    top_paises,
    orientation="h",
    labels={"value": "Títulos", "index": ""},
    title="Países que más contenido aportan al catálogo",
)
fig3.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
fig3.update_traces(marker_color="#221F1F")
fig3.show()

part_ee_uu = top_paises.iloc[-1] / len(df.drop_duplicates("id_unico")) * 100
print(f"Hallazgo: Estados Unidos concentra la mayor parte del catálogo "
      f"({top_paises.iloc[-1]:,} títulos), muy por sobre Japón y Reino Unido.")

# %% [markdown]
# ## Pregunta 4: ¿Lo más popular es también lo mejor evaluado?
# Si popularidad y rating no van de la mano, el gerente no debería
# promocionar solo por volumen de vistas.

# %%
muestra = df.dropna(subset=["rating"]).sample(3000, random_state=42)  # muestra para que el gráfico no se sature

fig4 = px.scatter(
    muestra, x="popularity", y="rating", color="type",
    opacity=0.4,
    labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
    title="Relación entre popularidad y calificación",
)
fig4.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig4.show()

corr = df["popularity"].corr(df["rating"])
print(f"Hallazgo: la correlación es prácticamente nula ({corr:.2f}). "
      f"Popularidad y calidad percibida son cosas distintas: un título muy visto "
      f"no necesariamente está bien evaluado.")

# %% [markdown]
# ## Pregunta 5: ¿Las películas y las series tienen distinto desempeño?
# Define si conviene priorizar inversión en un formato u otro.

# %%
fig5 = px.box(
    df.dropna(subset=["rating"]), x="type", y="rating",
    labels={"type": "", "rating": "Rating"},
    title="Distribución de rating: películas vs. series",
    color="type",
)
fig5.update_layout(template=TEMPLATE, showlegend=False)
fig5.show()

prom = df.groupby("type")["rating"].mean()
print(f"Hallazgo: las series promedian {prom['Serie']:.2f} vs. {prom['Película']:.2f} "
      f"de las películas, y tienen menos valores extremos bajos.")

# %% [markdown]
# ## Pregunta 6: ¿Qué géneros dominan cada formato?
# Compara el catálogo de películas y de series para detectar vacíos de oferta.

# %%
top6_peliculas = df[df.type == "Película"]["genero_principal"].value_counts().head(6)
top6_series = df[df.type == "Serie"]["genero_principal"].value_counts().head(6)
comparativo = pd.concat(
    [top6_peliculas.rename("Película"), top6_series.rename("Serie")], axis=1
).fillna(0).reset_index().melt(id_vars="genero_principal", var_name="type", value_name="titulos")

fig6 = px.bar(
    comparativo, x="genero_principal", y="titulos", color="type", barmode="group",
    labels={"genero_principal": "", "titulos": "Títulos", "type": ""},
    title="Géneros principales por formato",
)
fig6.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
fig6.show()

print("Hallazgo: Drama y Comedy dominan ambos formatos, pero Reality y Animation "
      "tienen mucho más peso en series que en películas.")