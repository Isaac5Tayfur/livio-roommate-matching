import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st
from collections import Counter
import plotly.io as pio
import os

os.makedirs("Media", exist_ok=True)   # This guarantees the folder exists when saving images

# ---------------------------------------------------------------
# Bar chart with language-aware labels
# ---------------------------------------------------------------
def generate_compatibility_chart(similarity_series, language='English'):
    similarity_series = similarity_series * 100
    theme = st.get_option("theme.base")
    dark_mode = theme == "dark"
    bar_color = "#BD93F9" if dark_mode else "#6272A4"
    text_color = "white" if dark_mode else "black"

    ylabel = "Similarity (%)" if language == "English" else "Similitud (%)"
    xlabel = "Tenant ID" if language == "English" else "ID Inquilino"

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=similarity_series.index.astype(str),
                y=similarity_series.values,
                ax=ax,
                color=bar_color)

    sns.despine(top=True, right=True, left=True, bottom=False)
    ax.set_xlabel(xlabel, fontsize=10, color=text_color)
    ax.set_ylabel(ylabel, fontsize=10, color=text_color)
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_color(text_color)

    for label in ax.get_yticklabels():
        label.set_text('{:.1f}%'.format(float(label.get_text())))
        label.set_color(text_color)
        #label.set_fontsize(8)

    for p in ax.patches:
        height = p.get_height()
        ax.annotate('{:.1f}%'.format(height),
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 8),
                    textcoords='offset points', fontsize=8, color=text_color)

    fig.savefig("Media/chart_export.png", dpi=300, bbox_inches='tight')
    return fig

# ---------------------------------------------------------------
# Table with translated attribute names and values
# ---------------------------------------------------------------
def generate_compatibility_table(result_tuple, language='English'):
    theme = st.get_option("theme.base")
    dark_mode = theme == "dark"
    header_color = "#1E1E1E" if dark_mode else "#D3D3D3"
    cell_color = "#292929" if dark_mode else "#FFFFFF"
    text_color = "white" if dark_mode else "black"

    result_df = result_tuple[0].reset_index()
    attr_col_name = "ATRIBUTO" if language == "Español" else "ATTRIBUTE"
    result_df.rename(columns={'index': attr_col_name}, inplace=True)

    attribute_translations = {
        "sleep_schedule": "Sleep Schedule", "work_shift": "Work Shift",
        "energy_rhythm": "Energy Rhythm", "education_level": "Education Level",
        "budget": "Budget (€)", "languages_spoken": "Languages Spoken",
        "social_level": "Social Level", "cleanliness_rating": "Cleanliness Rating",
        "likes_reading": "Likes Reading", "likes_cooking": "Likes Cooking",
        "cooking_preference": "Cooking Preference", "on_diet": "On Diet",
        "smoker": "Smoker", "likes_pets": "Likes Pets",
        "pet_allergy": "Pet Allergy", "frequent_visits": "Frequent Visits",
        "remote_worker": "Remote Worker", "plays_sports": "Plays Sports",
        "listens_loud_music": "Listens to Loud Music",
        "preferred_music_genre": "Preferred Music Genre",
        "ideal_weekend_plan": "Ideal Weekend Plan",
        "shares_common_items": "Shares Common Items",
        "relationship_status": "Relationship Status",
        "noise_tolerance": "Noise Tolerance",
        "null": "-"
    }

    value_translations = {}

    if language == "Español":
        result_df = result_df.replace("Yes", "Sí").replace("No", "No")
        attribute_translations.update({
            "sleep_schedule": "Horario de sueño", "work_shift": "Turno laboral",
            "energy_rhythm": "Ritmo energético", "education_level": "Nivel educativo",
            "budget": "Presupuesto (€)", "languages_spoken": "Idiomas hablados",
            "social_level": "Nivel social", "cleanliness_rating": "Valor de limpieza",
            "likes_reading": "Le gusta leer", "likes_cooking": "Le gusta cocinar",
            "cooking_preference": "Preferencia culinaria", "on_diet": "Sigue dieta",
            "smoker": "Fumador", "likes_pets": "Le gustan las mascotas",
            "pet_allergy": "Alergia a mascotas", "frequent_visits": "Visitas frecuentes",
            "remote_worker": "Teletrabaja", "plays_sports": "Practica deporte",
            "listens_loud_music": "Escucha música alta",
            "preferred_music_genre": "Género musical preferido",
            "ideal_weekend_plan": "Plan ideal de fin de semana",
            "shares_common_items": "Comparte Artículos Comunes",
            "relationship_status": "Relación sentimental",
            "noise_tolerance": "Tolerancia al ruido"
        })

        value_translations = {
            "Early bird": "Madrugador", "Balanced": "Equilibrado", "Night owl": "Nocturno",
            "Morning": "Mañana", "Afternoon": "Tarde", "Night": "Noche", "Flexible": "Flexible",
            "High": "Alta", "Medium": "Media", "Low": "Baja",
            "Italian": "Italiano", "Spanish": "Español", "English": "Inglés", "German": "Alemán", "French": "Francés",
            "High School": "Secundaria", "Bachelor's": "Grado", "Master's": "Máster", "PhD": "Doctorado",
            "Extrovert": "Extrovertido", "Introvert": "Introvertido",
            "Order": "Orden", "Cook": "Cocinar",
            "Pop": "Pop", "Techno": "Techno", "Reggaeton": "Reguetón", "Classical": "Clásica",
            "Jazz": "Jazz", "Rock": "Rock", "Chill": "Relajada",
            "Family Time": "Tiempo en familia", "Hike": "Excursión", "Party": "Fiesta", "Travel": "Viajar",
            "Relationship": "Relación", "Single": "Soltero/a",
            "None": "Ninguno", "null": "-"
        }
        def translate_cell(value):
            if isinstance(value, str):
                # Handle multi-word or comma-separated lists
                parts = [v.strip() for v in value.split(',')]
                translated = [value_translations.get(part, part) for part in parts]
                return ', '.join(translated)
            return value

        result_df = result_df.map(translate_cell)

    result_df = result_df.fillna("-")  # prevents raw NaN/null showing
    result_df.replace("null", "-", inplace=True)

    result_df[attr_col_name] = result_df[attr_col_name].apply(lambda x: attribute_translations.get(x, x.replace("_", " ").capitalize()))

    fig_table = go.Figure(data=[go.Table(
        columnwidth=[20] + [10] * (len(result_df.columns) - 1),
        header=dict(values=list(result_df.columns),
                    fill_color=header_color,
                    font=dict(color=text_color),
                    align='left'),
        cells=dict(values=[result_df[col] for col in result_df.columns],
                   fill_color=cell_color,
                   font=dict(color=text_color, size=12),
                   align='left'))
    ])
    fig_table.update_layout(autosize=True, margin=dict(l=10, r=10, t=10, b=10), height=500, xaxis=dict(automargin=True))

    num_cols = len(result_df.columns)
    table_width = 200 + 150 * (num_cols - 1)  # base 200 + 150px per column


    # Skip image export on Streamlit Cloud (Kaleido not supported there)
    if not os.environ.get("STREAMLIT_SERVER_HEADLESS", False):
        try:
            pio.write_image(fig_table, "Media/table_export.png", format="png", scale=2, width=table_width, height=600)
        except Exception as e:
            print("⚠️ Could not export table image:", e)


    return fig_table

# ---------------------------------------------------------------
# Match explanation block – top shared traits with emojis
# ---------------------------------------------------------------
def generate_explanation_block(result_df, language='English'):
    trait_counter = Counter()
    traits_used = []

    for i in range(len(result_df)):
        row = result_df.iloc[i, 1:]
        trait_name = result_df.iloc[i, 0]
        values = list(row)
        if all(v == values[0] for v in values):
            trait_counter[trait_name] += 1
            traits_used.append(trait_name)

    top_traits = [trait for trait, _ in trait_counter.most_common(5)]

    trait_emojis = {
        "likes_pets": "🐶", "smoker": "🚭", "on_diet": "🥗", "remote_worker": "💻",
        "cooking_preference": "🍳", "ideal_weekend_plan": "🏞️", "relationship_status": "❤️",
        "sleep_schedule": "🛏️", "social_level": "🗣️", "education_level": "🎓",
        "listens_loud_music": "🎧", "cleanliness_rating": "🧼", "pet_allergy": "🐾",
        "noise_tolerance": "🔇"
    }

    translations = {
        "likes_pets": "Likes Pets", "smoker": "Non-smoker", "on_diet": "On Diet",
        "remote_worker": "Remote Worker", "cooking_preference": "Cooking Preference",
        "ideal_weekend_plan": "Ideal Weekend Plan", "relationship_status": "Relationship Status",
        "sleep_schedule": "Sleep Schedule", "social_level": "Social Level",
        "education_level": "Education Level", "listens_loud_music": "Loud Music",
        "cleanliness_rating": "Cleanliness", "pet_allergy": "No Pet Allergy",
        "noise_tolerance": "Noise Tolerance"
    }

    if language == "Español":
        translations = {
            "likes_pets": "Le gustan las mascotas", "smoker": "No fumador", "on_diet": "Sigue dieta",
            "remote_worker": "Teletrabaja", "cooking_preference": "Preferencia culinaria",
            "ideal_weekend_plan": "Plan ideal de fin de semana", "relationship_status": "Relación sentimental",
            "sleep_schedule": "Horario de sueño", "social_level": "Nivel social",
            "education_level": "Nivel educativo", "listens_loud_music": "Música alta",
            "cleanliness_rating": "Valor de limpieza", "pet_allergy": "Sin alergia a mascotas",
            "noise_tolerance": "Tolerancia al ruido"
        }

    styled = [f"{trait_emojis.get(trait, '🔹')} {translations.get(trait, trait.replace('_', ' ').capitalize())}" for trait in top_traits]

    return styled
