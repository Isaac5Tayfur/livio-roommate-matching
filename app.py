import streamlit as st
from logic import compatible_tenants, df_raw
from ui_helpers import (
    generate_compatibility_chart,
    generate_compatibility_table,
    generate_explanation_block
)
import os

# PAGE CONFIGURATION
st.set_page_config(layout="wide", page_title="Livio – Smart Roommate Matching", page_icon="🧩")

# THEME & STYLE
theme = st.get_option("theme.base")
dark_mode = theme == "dark"
accent_color = "#BD93F9"
button_color = "#F04B82" if dark_mode else "#6272A4"
text_color = "white" if dark_mode else "black"

# FONTS + CSS
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    .subtitle-text {
        text-align: center;
        color: #CCCCCC;
        font-size: 25px;
        margin-bottom: 20px;
    }
    .highlight-box {
        background-color: #A899D8;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 20px auto;
        max-width: 600px;
        text-align: left;
    }
    .centered-banner {
        text-align: center;
        margin-top: 20px;
        margin-bottom: -10px;
    }
    .centered-banner img {
        width: 500px;
        border-radius: 10px;
        border: 2px solid white;
    }
</style>
""", unsafe_allow_html=True)

# LANGUAGE TOGGLE
language = st.sidebar.radio("🌐 Language", ["English", "Español"], horizontal=True)
_ = lambda x: x

if language == "Español":
    def _(text):
        translations = {
            "Tenant 1 ID": "Inquilino 1",
            "Tenant 2 ID": "Inquilino 2",
            "Tenant 3 ID": "Inquilino 3",
            "How many new matches?": "¿Cuántas coincidencias nuevas?",
            "Only show non-smokers": "Solo mostrar no fumadores",
            "Only show healthy eaters": "Solo mostrar quienes siguen dieta",
            "Exclude pet allergies": "Excluir alergias a mascotas",
            "FIND MATCHES": "🔍 Buscar coincidencias",
            "Match Setup": "Configuración de coincidencia",
            "Match Scores": "Puntajes de coincidencia",
            "Profile Comparison": "Comparación de perfiles",
            "Why These Matches?": "¿Por qué estas coincidencias?",
            "Optional Filters": "Filtros opcionales",
            "Compatibility Results": "Resultados de compatibilidad",
            "Export Files": "Exportar archivos",
            "Results CSV": "CSV de resultados",
            "Chart PNG": "Gráfico de coincidencias",
            "Table PNG": "Tabla de comparación",
            "Shared Traits": "Principales rasgos compartidos",
            "Download": "Descargar",
            "No matches found with the selected filters.": "No se encontraron coincidencias con los filtros seleccionados.",
            "Expand comparison table": "Expandir tabla de comparación"
        }
        return translations.get(text, text)

# BANNER
with st.container():
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; text-align: center; margin-top: 10px; margin-bottom: -10px;">
    """, unsafe_allow_html=True)
    
    st.image("Media/banner.png", width=360)

    st.markdown("""
        <p style="font-size: 25px; color: #CCCCCC; margin-top: 5px;">
            Discover compatibility that feels like home.
        </p>
    </div>
    """, unsafe_allow_html=True)

# BUTTON STYLE
st.markdown(f"""
<style>
div.stButton > button:first-child {{
    background-color: {button_color};
    color: {text_color};
    font-size: 16px;
    border-radius: 10px;
    border: none;
}}
div.stButton > button:first-child:hover {{
    background-color: {accent_color};
    color: black;
}}
.element-container:has(> .stPlotlyChart), .element-container:has(> .stPyplot) {{
    max-width: 800px !important;
    margin: auto;
}}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.header(f"🔎 {_('Match Setup')}")
    tenant_ids_available = df_raw["id_tenant"].sort_values().tolist()
    tenant1 = st.selectbox(_(f"Tenant 1 ID"), tenant_ids_available, index=0, key="t1")
    tenant2 = st.selectbox(_(f"Tenant 2 ID"), tenant_ids_available, index=1, key="t2")
    tenant3 = st.selectbox(_(f"Tenant 3 ID"), tenant_ids_available, index=2, key="t3")
    top_n = st.slider(_(f"How many new matches?"), 1, 10, value=5)

    st.markdown("---")
    st.subheader(f"🧼 {_('Optional Filters')}")
    filter_non_smokers = st.checkbox(_(f"Only show non-smokers"), value=False)
    filter_diet = st.checkbox(_(f"Only show healthy eaters"), value=False)
    filter_pets = st.checkbox(_(f"Exclude pet allergies"), value=False)

    result = None
    if st.button(_(f"FIND MATCHES")):
        seed_ids = list(set([tenant1, tenant2, tenant3]))
        result = compatible_tenants(seed_ids, top_n)

        if not isinstance(result, str):
            result_df, similarity_scores = result
            matched_ids = similarity_scores.index.tolist()
            filtered_ids = matched_ids
            if filter_non_smokers:
                filtered_ids = [i for i in filtered_ids if df_raw.loc[df_raw['id_tenant'] == i, 'smoker'].values[0] == "No"]
            if filter_diet:
                filtered_ids = [i for i in filtered_ids if df_raw.loc[df_raw['id_tenant'] == i, 'on_diet'].values[0] == "Yes"]
            if filter_pets:
                filtered_ids = [i for i in filtered_ids if df_raw.loc[df_raw['id_tenant'] == i, 'pet_allergy'].values[0] == "No"]

            if len(filtered_ids) == 0:
                st.session_state["result"] = _("No matches found with the selected filters.")
            else:
                filtered_scores = similarity_scores[similarity_scores.index.isin(filtered_ids)]
                result_df = result_df.loc[:, result_df.columns.astype(str).isin([str(id) for id in seed_ids + filtered_ids])]
                st.session_state["result"] = (result_df, filtered_scores)

# MAIN CONTENT
result = st.session_state.get("result", None)

if isinstance(result, str):
    st.error(result)

elif result is not None:
    result_df, similarity_scores = result
    st.divider()
    st.markdown(f"## 🔗 {_('Compatibility Results')}")

    st.write(f"### 📊 {_('Match Scores')}")
    fig_chart = generate_compatibility_chart(similarity_scores, language)

    with st.container():
        st.markdown("<div style='max-width: 850px; margin: auto;'>", unsafe_allow_html=True)
        st.pyplot(fig_chart)
        st.markdown("</div>", unsafe_allow_html=True)


    st.markdown(f"### 🧬 {_('Profile Comparison')}")
    with st.expander(f"🔍 {_('Expand comparison table')}"):
        fig_table = generate_compatibility_table(result, language)

        st.markdown("""<div style="overflow-x: auto; overflow-y: auto; max-height: 600px;">""", unsafe_allow_html=True)
        st.plotly_chart(fig_table, use_container_width=False, config={
            "scrollZoom": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["toImage"]
        })
        st.markdown("</div>", unsafe_allow_html=True)


    st.markdown(f"### 🧠 {_('Why These Matches?')}")
    explanation = generate_explanation_block(result_df.reset_index(), language)

    if explanation:
        with st.container():
            st.markdown(
                f"""
                <div class="highlight-box">
                    <strong>{_('Shared Traits')}:</strong><br>• {"<br>• ".join(explanation)}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("These matches are based on overall lifestyle compatibility.")


    st.markdown("### 📥 " + (_("Export Files") if language == "English" else "Exportar archivos"))

    # CSV button
    download_df = result_df.T.reset_index().rename(columns={"index": _("ATTRIBUTE")})
    csv = download_df.to_csv(index=False).encode("utf-8")
    st.download_button(label="📄 " + (_("Results CSV") if language == "English" else "CSV de resultados"),
                    data=csv, file_name="livio_results.csv", mime="text/csv")

    # Chart PNG
    with open("Media/chart_export.png", "rb") as chart_file:
        st.download_button("📊 " + (_("Chart PNG") if language == "English" else "Gráfico de coincidencias"),
                        chart_file, file_name="livio_chart.png", mime="image/png")

    # Table PNG
    if os.path.exists("Media/table_export.png"):
        with open("Media/table_export.png", "rb") as table_file:
            st.download_button("📋 " + (_("Table PNG") if language == "English" else "Tabla de comparación"),
                            table_file, file_name="livio_table.png", mime="image/png")
    else:
        st.warning("📋 " + (_("Table export not available in this environment.") if language == "English" else "Exportar tabla no disponible en este entorno."))