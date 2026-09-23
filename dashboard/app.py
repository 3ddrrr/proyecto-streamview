"""
Dashboard StreamView Analytics — Audiencia: Gerente de Contenidos
Ejecutar desde la raíz del proyecto:  streamlit run dashboard/app.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------- Configuración de página
st.set_page_config(page_title="StreamView Analytics", layout="wide", page_icon="🎬")
TEMPLATE = "plotly_white"
ROJO = "#E50914"

# ---------------------------------------------------------------- Carga de datos (cacheada)
@st.cache_data
def cargar_datos():
    df = pd.read_csv("data/processed/catalogo.csv")
    generos = pd.read_csv("data/processed/generos.csv")
    paises = pd.read_csv("data/processed/paises.csv")
    return df, generos, paises

df, generos, paises = cargar_datos()

# ---------------------------------------------------------------- Sidebar: filtros
st.sidebar.title("Filtros")

tipo_sel = st.sidebar.multiselect(
    "Tipo de contenido", options=["Película", "Serie"], default=["Película", "Serie"]
)

anio_min, anio_max = int(df["release_year"].min()), int(df["release_year"].max())
rango_anio = st.sidebar.slider(
    "Año de estreno", anio_min, anio_max, (anio_min, anio_max)
)

generos_disp = sorted(generos["genero"].dropna().unique())
generos_sel = st.sidebar.multiselect("Género", options=generos_disp, default=[])

paises_disp = paises["pais"].value_counts().head(20).index.tolist()
paises_sel = st.sidebar.multiselect("País (top 20)", options=paises_disp, default=[])

# ---------------------------------------------------------------- Aplicar filtros
df_f = df[
    df["type"].isin(tipo_sel)
    & df["release_year"].between(rango_anio[0], rango_anio[1])
]

if generos_sel:
    ids_genero = generos[generos["genero"].isin(generos_sel)]["id_unico"].unique()
    df_f = df_f[df_f["id_unico"].isin(ids_genero)]

if paises_sel:
    ids_pais = paises[paises["pais"].isin(paises_sel)]["id_unico"].unique()
    df_f = df_f[df_f["id_unico"].isin(ids_pais)]

# ---------------------------------------------------------------- Encabezado
st.title("🎬 StreamView Analytics")
st.caption("Panel de decisión para el Gerente de Contenidos")

if df_f.empty:
    st.warning("No hay títulos con los filtros seleccionados. Ajusta los filtros.")
    st.stop()

# ---------------------------------------------------------------- KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Títulos", f"{len(df_f):,}")
c2.metric("Rating promedio", f"{df_f['rating'].mean():.2f}")
c3.metric("Popularidad promedio", f"{df_f['popularity'].mean():.1f}")
genero_top = (
    generos[generos["id_unico"].isin(df_f["id_unico"])]["genero"]
    .value_counts()
    .idxmax()
)
c4.metric("Género más frecuente", genero_top)

st.divider()

# ---------------------------------------------------------------- Navegación por pestañas
tab1, tab2, tab3 = st.tabs(["📊 Exploración", "🌍 Alcance", "📖 Storytelling"])

# --- Tab 1: Exploración
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        g = generos[generos["id_unico"].isin(df_f["id_unico"])].merge(
            df_f[["id_unico", "rating", "calificacion_confiable"]], on="id_unico"
        )
        g = g[g["calificacion_confiable"]]
        top_g = g.groupby("genero")["rating"].mean().sort_values(ascending=False).head(10)
        fig = px.bar(
            top_g.sort_values(), orientation="h",
            labels={"value": "Rating promedio", "genero": ""},
            title="Géneros mejor evaluados",
        )
        fig.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
        fig.update_traces(marker_color=ROJO)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        muestra = df_f.dropna(subset=["rating"])
        if len(muestra) > 3000:
            muestra = muestra.sample(3000, random_state=42)
        fig = px.scatter(
            muestra, x="popularity", y="rating", color="type", opacity=0.4,
            labels={"popularity": "Popularidad", "rating": "Rating", "type": ""},
            title="Popularidad vs. rating",
        )
        fig.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)

    evolucion = df_f.groupby(["anio_agregado", "type"]).size().reset_index(name="titulos")
    fig = px.line(
        evolucion, x="anio_agregado", y="titulos", color="type", markers=True,
        labels={"anio_agregado": "Año", "titulos": "Títulos agregados", "type": ""},
        title="Crecimiento del catálogo por año",
    )
    fig.update_layout(template=TEMPLATE, legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 2: Alcance geográfico
with tab2:
    top_paises = (
        paises[paises["id_unico"].isin(df_f["id_unico"])]["pais"]
        .value_counts()
        .head(10)
        .sort_values()
    )
    fig = px.bar(
        top_paises, orientation="h",
        labels={"value": "Títulos", "index": ""},
        title="Países que más aportan al catálogo",
    )
    fig.update_layout(template=TEMPLATE, showlegend=False, yaxis_title="")
    fig.update_traces(marker_color="#221F1F")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.box(
        df_f.dropna(subset=["rating"]), x="type", y="rating", color="type",
        labels={"type": "", "rating": "Rating"},
        title="Distribución de rating: películas vs. series",
    )
    fig.update_layout(template=TEMPLATE, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 3: Storytelling / hallazgos y recomendaciones
with tab3:
    st.subheader("Hallazgos principales")
    st.markdown(
        """
        1. **La popularidad no garantiza calidad.** La correlación entre ambas
           variables es prácticamente nula: promocionar solo por volumen de vistas
           es riesgoso para la reputación del catálogo.
        2. **Las series superan a las películas en rating promedio**, con menos
           valores extremos bajos.
        3. **Estados Unidos concentra la mayor parte del catálogo**, seguido de
           lejos por Japón y Reino Unido — hay espacio para diversificar origen.
        4. **El catálogo crece a un ritmo estable** en ambos formatos, sin señales
           de desaceleración.
        """
    )
    st.subheader("Recomendaciones")
    st.markdown(
        """
        - Priorizar adquisición en géneros con mejor recepción validada
          (100+ votos), no solo los más populares.
        - Evaluar producción propia de series, dado su mejor desempeño relativo.
        - Explorar acuerdos de contenido en mercados fuera de EE. UU. para
          diversificar el catálogo.
        """
    )

st.divider()
st.caption("Filtros aplicados: "
           f"{', '.join(tipo_sel) or 'ninguno'} · "
           f"{rango_anio[0]}–{rango_anio[1]}"
           + (f" · Géneros: {', '.join(generos_sel)}" if generos_sel else "")
           + (f" · Países: {', '.join(paises_sel)}" if paises_sel else ""))