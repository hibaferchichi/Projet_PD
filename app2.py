
import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px

# Charger le modèle sauvegardé
try:
    model = joblib.load("meilleur_modele.pkl")
except FileNotFoundError:
    st.error("Erreur : Le fichier 'meilleur_modele.pkl' est introuvable. Vérifiez le chemin du fichier.")
    st.stop()

# Gestion du thème (clair/sombre)
if "theme" not in st.session_state:
    st.session_state.theme = "clair"
if "presentation_mode" not in st.session_state:
    st.session_state.presentation_mode = False

# État pour suivre l'interaction avec les champs
if "classe_touched" not in st.session_state:
    st.session_state.classe_touched = False
if "eng_touched" not in st.session_state:
    st.session_state.eng_touched = False
if "lgd_touched" not in st.session_state:
    st.session_state.lgd_touched = False

# CSS pour les thèmes et styles
theme_css = """
    /* Thème clair */
    .stApp {
        background: linear-gradient(135deg, #f9f9f9 0%, #ffffff 100%);
        animation: fadeIn 1s ease-in;
        font-family: 'Poppins', sans-serif;
    }
    .stText, .stMarkdown, .stSubheader {
        color: #333333;
    }
    .result-card {
        background-color: #ffffff;
    }
    .description-box {
        border-left: 4px solid #003087;
        padding-left: 10px;
        color: #333333;
    }
    .header-logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .header-logo h1 {
        font-size: 3em;
        color: #003087;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
    }
    .input-label {
        font-weight: 600;
        color: #003087;
        margin-bottom: 5px;
        border-bottom: 1px solid #d4af37;
        padding-bottom: 3px;
    }
    .input-container {
        margin-bottom: 25px;
    }
    .sidebar-instruction {
        margin-bottom: 15px;
    }
""" if st.session_state.theme == "clair" else """
    /* Thème sombre */
    .stApp {
        background: linear-gradient(135deg, #333333 0%, #454545 100%);
        animation: fadeIn 1s ease-in;
        font-family: 'Poppins', sans-serif;
    }
    .stText, .stMarkdown, .stSubheader {
        color: #f5f5f5;
    }
    .result-card {
        background-color: #454545;
    }
    .description-box {
        border-left: 4px solid #d4af37;
        padding-left: 10px;
        color: #f5f5f5;
    }
    .header-logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .header-logo h1 {
        font-size: 3em;
        color: #d4af37;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
    }
    .input-label {
        font-weight: 600;
        color: #d4af37;
        margin-bottom: 5px;
        border-bottom: 1px solid #003087;
        padding-bottom: 3px;
    }
    .input-container {
        margin-bottom: 25px;
    }
    .sidebar-instruction {
        margin-bottom: 15px;
    }
"""

st.markdown(
    f"""
    <style>
    /* Importer une police professionnelle */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    {theme_css}

    /* Animation fade-in */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    /* Titre principal */
    .css-1d391kg {{
        font-size: 2.5em;
        text-align: center;
        font-weight: 700;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
        color: {'#003087' if st.session_state.theme == "clair" else '#d4af37'};
    }}

    /* Sous-titres */
    .stSubheader {{
        font-weight: 600;
        font-size: 1.5em;
        border-bottom: 2px solid {'#003087' if st.session_state.theme == "clair" else '#d4af37'};
        padding-bottom: 5px;
    }}

    /* Texte général */
    .stText, .stMarkdown {{
        font-size: 1.1em;
        line-height: 1.5;
    }}

    /* Bouton */
    .stButton>button {{
        background-color: #d4af37;
        color: #333333;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
    }}
    .stButton>button:hover {{
        background-color: #c19b32;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
    }}

    /* Bouton de téléchargement */
    .stDownloadButton>button {{
        background-color: #003087;
        color: #ffffff;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
    }}
    .stDownloadButton>button:hover {{
        background-color: #00266b;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
    }}

    /* Champs d'entrée */
    .stNumberInput, .stSelectbox {{
        background-color: #ffffff;
        border-radius: 5px;
        padding: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #d4af37;
    }}

    /* Cartes de résultats */
    .result-card {{
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        margin: 15px 0;
        animation: slideIn 0.5s ease-out;
        opacity: 0;
        animation-fill-mode: forwards;
        border: 1px solid {'#003087' if st.session_state.theme == "clair" else '#d4af37'};
    }}
    .result-card.pd {{
        border-left: 4px solid #003087;
    }}
    .result-card.ecl {{
        border-left: 4px solid #d4af37;
    }}
    @keyframes slideIn {{
        from {{ transform: translateY(15px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}

    /* Messages de validation */
    .validation-error {{
        color: #e74c3c;
        font-size: 0.9em;
        margin-top: 5px;
    }}
    .validation-success {{
        color: #2ecc71;
        font-size: 0.9em;
        margin-top: 5px;
    }}

    /* Graphique animé */
    .chart-container {{
        animation: chartFade 0.8s ease-in forwards;
    }}
    @keyframes chartFade {{
        from {{ opacity: 0; transform: scale(0.98); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Logo / Titre stylisé
st.markdown(
    """
    <div class="header-logo">
        <h1>PD Predictor</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Bouton pour activer/désactiver le mode présentation
if st.button("Mode Présentation"):
    st.session_state.presentation_mode = not st.session_state.presentation_mode
    st.rerun()

# Si mode présentation, masquer la sidebar
if not st.session_state.presentation_mode:
    # Instructions
    st.sidebar.header("Instructions")
    st.sidebar.markdown(
        """
        <div class="sidebar-instruction">1. Saisissez les valeurs pour Classe (0 ou 1), Secteur, ENG, et LGD.</div>
        <div class="sidebar-instruction">2. Cliquez sur le bouton <b>Prédire PD et Calculer ECL</b>.</div>
        <div class="sidebar-instruction">3. Consultez les résultats affichés et téléchargez-les si besoin.</div>
        """,
        unsafe_allow_html=True
    )
    # Bascule thème
    if st.sidebar.button("Basculer thème"):
        st.session_state.theme = "sombre" if st.session_state.theme == "clair" else "clair"
        st.rerun()

# Titre de l'application
st.title("Prédiction de la PD et Calcul de l'ECL")

# Description
st.markdown(
    """
    <div class="description-box">
    Cette application permet de prédire la <b>Probabilité de Défaut (PD)</b> pour un client donné
    et de calculer la <b>Perte de Crédit Attendue (ECL)</b> en fonction des paramètres fournis.
    </div>
    """,
    unsafe_allow_html=True
)

# Créer des champs pour les entrées utilisateur
st.header("Entrez les paramètres du client")

# Disposition en colonnes
col1, col2 = st.columns(2)

with col1:
    # Variables pour la prédiction de la PD
    st.markdown('<div class="input-label">Classe (0 ou 1)</div><div class="input-container"></div>', unsafe_allow_html=True)
    classe = st.number_input("", min_value=0, max_value=1, value=0, step=1, label_visibility="collapsed", key="classe")
    if st.session_state.get("classe") != st.session_state.get("classe_prev", st.session_state.classe):
        st.session_state.classe_touched = True
        st.session_state.classe_prev = st.session_state.classe
    if st.session_state.classe_touched:
        if classe not in [0, 1]:
            st.markdown('<div class="validation-error">Classe doit être 0 ou 1.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="validation-success">Valeur correcte.</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-label">Secteur</div><div class="input-container"></div>', unsafe_allow_html=True)
    secteur = st.selectbox("", ["AGRICULTURE", "BTP", "COMMERCE", "INDUSTRIES", "SERVICES"], label_visibility="collapsed")

with col2:
    # Variables pour le calcul de l'ECL
    st.markdown('<div class="input-label">ENG (Exposition au défaut)</div><div class="input-container"></div>', unsafe_allow_html=True)
    eng = st.number_input("", min_value=0.0, value=100000.0, step=1000.0, label_visibility="collapsed", key="eng")
    if st.session_state.get("eng") != st.session_state.get("eng_prev", st.session_state.eng):
        st.session_state.eng_touched = True
        st.session_state.eng_prev = st.session_state.eng
    if st.session_state.eng_touched:
        if eng <= 0:
            st.markdown('<div class="validation-error">ENG doit être supérieur à 0.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="validation-success">Valeur correcte.</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-label">LGD (Perte en cas de défaut, entre 0 et 1)</div><div class="input-container"></div>', unsafe_allow_html=True)
    lgd = st.number_input("", min_value=0.0, max_value=1.0, value=0.45, step=0.01, label_visibility="collapsed", key="lgd")
    if st.session_state.get("lgd") != st.session_state.get("lgd_prev", st.session_state.lgd):
        st.session_state.lgd_touched = True
        st.session_state.lgd_prev = st.session_state.lgd
    if st.session_state.lgd_touched:
        if lgd < 0 or lgd > 1:
            st.markdown('<div class="validation-error">LGD doit être entre 0 et 1.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="validation-success">Valeur correcte.</div>', unsafe_allow_html=True)

# Bouton pour lancer la prédiction
if st.button("Prédire PD et Calculer ECL"):
    # Validation des entrées
    if lgd < 0 or lgd > 1:
        st.error("LGD doit être entre 0 et 1.")
        st.stop()
    if classe not in [0, 1]:
        st.error("Classe doit être 0 ou 1.")
        st.stop()
    if eng <= 0:
        st.error("ENG doit être supérieur à 0.")
        st.stop()

    # Préparer les données pour la prédiction
    input_data = pd.DataFrame({
        "Classe": [classe],
        "Secteur": [secteur]
    })

    # Encoder la variable catégorique "Secteur"
    input_data = pd.get_dummies(input_data, columns=["Secteur"], prefix="Secteur")

    # Colonnes attendues par le modèle
    expected_columns = [
        "Classe",
        "Secteur_AGRICULTURE", "Secteur_BTP", "Secteur_COMMERCE",
        "Secteur_INDUSTRIES", "Secteur_SERVICES"
    ]

    # Ajouter les colonnes manquantes avec des zéros
    for col in expected_columns:
        if col not in input_data.columns:
            input_data[col] = 0

    # Réorganiser les colonnes
    input_data = input_data[expected_columns]

    # Faire la prédiction de la PD
    with st.spinner("Prédiction en cours..."):
        try:
            pd_pred = model.predict(input_data)[0]  # Prédiction pour un régresseur
            pd_pred = np.clip(pd_pred, 0, 1)  # Contrainte pour que PD soit entre 0 et 1
        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {str(e)}")
            st.stop()

    # Calculer l'ECL
    ead = eng  # ENG comme proxy pour EAD
    ecl = pd_pred * lgd * ead

    # Afficher les résultats avec une mise en forme stylée
    st.subheader("Résultats")
    col_result1, col_result2 = st.columns(2)
    with col_result1:
        st.markdown(
            f"""
            <div class="result-card pd" style="animation-delay: 0.2s;">
                <h3>Probabilité de Défaut (PD) : <span style="color: #003087;">{pd_pred:.4f}</span></h3>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_result2:
        st.markdown(
            f"""
            <div class="result-card ecl" style="animation-delay: 0.4s;">
                <h3>Perte de Crédit Attendue (ECL) : <span style="color: #d4af37;">{ecl:,.2f} UM</span></h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Visualisation avec Plotly
    st.markdown("<h3>Visualisation des données</h3>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        "Catégories": ["PD", "LGD", "EAD ", "Classe"],
        "Valeurs": [pd_pred, lgd, ead / max(ead, 1), classe]
    })
    fig = px.bar(
        chart_data,
        x="Catégories",
        y="Valeurs",
        color="Catégories",
        color_discrete_sequence=["#003087", "#d4af37", "#666666", "#999999"],
        height=400,
        width=800
    )
    fig.update_traces(
        marker=dict(line=dict(width=2, color='#333333'))
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins", size=14, color="#f5f5f5" if st.session_state.theme == "sombre" else "#333333"),
        title="Résultats visuels",
        title_x=0.5
    )
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Téléchargement des résultats
    csv = pd.DataFrame({
        "PD": [pd_pred],
        "ECL": [ecl],
        "ENG": [eng],
        "LGD": [lgd],
        "Classe": [classe],
        "Secteur": [secteur]
    }).to_csv(index=False)
    st.download_button(
        label="Télécharger les résultats",
        data=csv,
        file_name="resultats.csv",
        mime="text/csv"

import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px

# Charger le modèle sauvegardé
try:
    model = joblib.load("meilleur_modele.pkl")
except FileNotFoundError:
    st.error("Erreur : Le fichier 'meilleur_modele.pkl' est introuvable. Vérifiez le chemin du fichier.")
    st.stop()

# Gestion du thème (clair/sombre)
if "theme" not in st.session_state:
    st.session_state.theme = "clair"
if "presentation_mode" not in st.session_state:
    st.session_state.presentation_mode = False

# État pour suivre l'interaction avec les champs
if "classe_touched" not in st.session_state:
    st.session_state.classe_touched = False
if "eng_touched" not in st.session_state:
    st.session_state.eng_touched = False
if "lgd_touched" not in st.session_state:
    st.session_state.lgd_touched = False

# CSS pour les thèmes et styles
theme_css = """
    /* Thème clair */
    .stApp {
        background: linear-gradient(135deg, #f9f9f9 0%, #ffffff 100%);
        animation: fadeIn 1s ease-in;
        font-family: 'Poppins', sans-serif;
    }
    .stText, .stMarkdown, .stSubheader {
        color: #333333;
    }
    .result-card {
        background-color: #ffffff;
    }
    .description-box {
        border-left: 4px solid #003087;
        padding-left: 10px;
        color: #333333;
    }
    .header-logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .header-logo h1 {
        font-size: 3em;
        color: #003087;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
    }
    .input-label {
        font-weight: 600;
        color: #003087;
        margin-bottom: 5px;
        border-bottom: 1px solid #d4af37;
        padding-bottom: 3px;
    }
    .input-container {
        margin-bottom: 25px;
    }
    .sidebar-instruction {
        margin-bottom: 15px;
    }
""" if st.session_state.theme == "clair" else """
    /* Thème sombre */
    .stApp {
        background: linear-gradient(135deg, #333333 0%, #454545 100%);
        animation: fadeIn 1s ease-in;
        font-family: 'Poppins', sans-serif;
    }
    .stText, .stMarkdown, .stSubheader {
        color: #f5f5f5;
    }
    .result-card {
        background-color: #454545;
    }
    .description-box {
        border-left: 4px solid #d4af37;
        padding-left: 10px;
        color: #f5f5f5;
    }
    .header-logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .header-logo h1 {
        font-size: 3em;
        color: #d4af37;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
    }
    .input-label {
        font-weight: 600;
        color: #d4af37;
        margin-bottom: 5px;
        border-bottom: 1px solid #003087;
        padding-bottom: 3px;
    }
    .input-container {
        margin-bottom: 25px;
    }
    .sidebar-instruction {
        margin-bottom: 15px;
    }
"""

st.markdown(
    f"""
    <style>
    /* Importer une police professionnelle */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    {theme_css}

    /* Animation fade-in */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    /* Titre principal */
    .css-1d391kg {{
        font-size: 2.5em;
        text-align: center;
        font-weight: 700;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
        color: {'#003087' if st.session_state.theme == "clair" else '#d4af37'};
    }}

    /* Sous-titres */
    .stSubheader {{
        font-weight: 600;
        font-size: 1.5em;
        border-bottom: 2px solid {'#003087' if st.session_state.theme == "clair" else '#d4af37'};
        padding-bottom: 5px;
    }}

    /* Texte général */
    .stText, .stMarkdown {{
        font-size: 1.1em;
        line-height: 1.5;
    }}

    /* Bouton */
    .stButton>button {{
        background-color: #d4af37;
        color: #333333;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
    }}
    .stButton>button:hover {{
        background-color: #c19b32;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
    }}

    /* Bouton de téléchargement */
    .stDownloadButton>button {{
        background-color: #003087;
        color: #ffffff;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
    }}
    .stDownloadButton>button:hover {{
        background-color: #00266b;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
    }}

    /* Champs d'entrée */
    .stNumberInput, .stSelectbox {{
        background-color: #ffffff;
        border-radius: 5px;
        padding: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #d4af37;
    }}

    /* Cartes de résultats */
    .result-card {{
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        margin: 15px 0;
        animation: slideIn 0.5s ease-out;
        opacity: 0;
        animation-fill-mode: forwards;
        border: 1px solid {'#003087' if st.session_state.theme == "clair" else '#d4af37'};
    }}
    .result-card.pd {{
        border-left: 4px solid #003087;
    }}
    .result-card.ecl {{
        border-left: 4px solid #d4af37;
    }}
    @keyframes slideIn {{
        from {{ transform: translateY(15px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}

    /* Messages de validation */
    .validation-error {{
        color: #e74c3c;
        font-size: 0.9em;
        margin-top: 5px;
    }}
    .validation-success {{
        color: #2ecc71;
        font-size: 0.9em;
        margin-top: 5px;
    }}

    /* Graphique animé */
    .chart-container {{
        animation: chartFade 0.8s ease-in forwards;
    }}
    @keyframes chartFade {{
        from {{ opacity: 0; transform: scale(0.98); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Logo / Titre stylisé
st.markdown(
    """
    <div class="header-logo">
        <h1>PD Predictor</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Bouton pour activer/désactiver le mode présentation
if st.button("Mode Présentation"):
    st.session_state.presentation_mode = not st.session_state.presentation_mode
    st.rerun()

# Si mode présentation, masquer la sidebar
if not st.session_state.presentation_mode:
    # Instructions
    st.sidebar.header("Instructions")
    st.sidebar.markdown(
        """
        <div class="sidebar-instruction">1. Saisissez les valeurs pour Classe (0 ou 1), Secteur, ENG, et LGD.</div>
        <div class="sidebar-instruction">2. Cliquez sur le bouton <b>Prédire PD et Calculer ECL</b>.</div>
        <div class="sidebar-instruction">3. Consultez les résultats affichés et téléchargez-les si besoin.</div>
        """,
        unsafe_allow_html=True
    )
    # Bascule thème
    if st.sidebar.button("Basculer thème"):
        st.session_state.theme = "sombre" if st.session_state.theme == "clair" else "clair"
        st.rerun()

# Titre de l'application
st.title("Prédiction de la PD et Calcul de l'ECL")

# Description
st.markdown(
    """
    <div class="description-box">
    Cette application permet de prédire la <b>Probabilité de Défaut (PD)</b> pour un client donné
    et de calculer la <b>Perte de Crédit Attendue (ECL)</b> en fonction des paramètres fournis.
    </div>
    """,
    unsafe_allow_html=True
)

# Créer des champs pour les entrées utilisateur
st.header("Entrez les paramètres du client")

# Disposition en colonnes
col1, col2 = st.columns(2)

with col1:
    # Variables pour la prédiction de la PD
    st.markdown('<div class="input-label">Classe (0 ou 1)</div><div class="input-container"></div>', unsafe_allow_html=True)
    classe = st.number_input("", min_value=0, max_value=1, value=0, step=1, label_visibility="collapsed", key="classe")
    if st.session_state.get("classe") != st.session_state.get("classe_prev", st.session_state.classe):
        st.session_state.classe_touched = True
        st.session_state.classe_prev = st.session_state.classe
    if st.session_state.classe_touched:
        if classe not in [0, 1]:
            st.markdown('<div class="validation-error">Classe doit être 0 ou 1.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="validation-success">Valeur correcte.</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-label">Secteur</div><div class="input-container"></div>', unsafe_allow_html=True)
    secteur = st.selectbox("", ["AGRICULTURE", "BTP", "COMMERCE", "INDUSTRIES", "SERVICES"], label_visibility="collapsed")

with col2:
    # Variables pour le calcul de l'ECL
    st.markdown('<div class="input-label">ENG (Exposition au défaut)</div><div class="input-container"></div>', unsafe_allow_html=True)
    eng = st.number_input("", min_value=0.0, value=100000.0, step=1000.0, label_visibility="collapsed", key="eng")
    if st.session_state.get("eng") != st.session_state.get("eng_prev", st.session_state.eng):
        st.session_state.eng_touched = True
        st.session_state.eng_prev = st.session_state.eng
    if st.session_state.eng_touched:
        if eng <= 0:
            st.markdown('<div class="validation-error">ENG doit être supérieur à 0.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="validation-success">Valeur correcte.</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-label">LGD (Perte en cas de défaut, entre 0 et 1)</div><div class="input-container"></div>', unsafe_allow_html=True)
    lgd = st.number_input("", min_value=0.0, max_value=1.0, value=0.45, step=0.01, label_visibility="collapsed", key="lgd")
    if st.session_state.get("lgd") != st.session_state.get("lgd_prev", st.session_state.lgd):
        st.session_state.lgd_touched = True
        st.session_state.lgd_prev = st.session_state.lgd
    if st.session_state.lgd_touched:
        if lgd < 0 or lgd > 1:
            st.markdown('<div class="validation-error">LGD doit être entre 0 et 1.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="validation-success">Valeur correcte.</div>', unsafe_allow_html=True)

# Bouton pour lancer la prédiction
if st.button("Prédire PD et Calculer ECL"):
    # Validation des entrées
    if lgd < 0 or lgd > 1:
        st.error("LGD doit être entre 0 et 1.")
        st.stop()
    if classe not in [0, 1]:
        st.error("Classe doit être 0 ou 1.")
        st.stop()
    if eng <= 0:
        st.error("ENG doit être supérieur à 0.")
        st.stop()

    # Préparer les données pour la prédiction
    input_data = pd.DataFrame({
        "Classe": [classe],
        "Secteur": [secteur]
    })

    # Encoder la variable catégorique "Secteur"
    input_data = pd.get_dummies(input_data, columns=["Secteur"], prefix="Secteur")

    # Colonnes attendues par le modèle
    expected_columns = [
        "Classe",
        "Secteur_AGRICULTURE", "Secteur_BTP", "Secteur_COMMERCE",
        "Secteur_INDUSTRIES", "Secteur_SERVICES"
    ]

    # Ajouter les colonnes manquantes avec des zéros
    for col in expected_columns:
        if col not in input_data.columns:
            input_data[col] = 0

    # Réorganiser les colonnes
    input_data = input_data[expected_columns]

    # Faire la prédiction de la PD
    with st.spinner("Prédiction en cours..."):
        try:
            pd_pred = model.predict(input_data)[0]  # Prédiction pour un régresseur
            pd_pred = np.clip(pd_pred, 0, 1)  # Contrainte pour que PD soit entre 0 et 1
        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {str(e)}")
            st.stop()

    # Calculer l'ECL
    ead = eng  # ENG comme proxy pour EAD
    ecl = pd_pred * lgd * ead

    # Afficher les résultats avec une mise en forme stylée
    st.subheader("Résultats")
    col_result1, col_result2 = st.columns(2)
    with col_result1:
        st.markdown(
            f"""
            <div class="result-card pd" style="animation-delay: 0.2s;">
                <h3>Probabilité de Défaut (PD) : <span style="color: #003087;">{pd_pred:.4f}</span></h3>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_result2:
        st.markdown(
            f"""
            <div class="result-card ecl" style="animation-delay: 0.4s;">
                <h3>Perte de Crédit Attendue (ECL) : <span style="color: #d4af37;">{ecl:,.2f} UM</span></h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Visualisation avec Plotly
    st.markdown("<h3>Visualisation des données</h3>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        "Catégories": ["PD", "LGD", "EAD ", "Classe"],
        "Valeurs": [pd_pred, lgd, ead / max(ead, 1), classe]
    })
    fig = px.bar(
        chart_data,
        x="Catégories",
        y="Valeurs",
        color="Catégories",
        color_discrete_sequence=["#003087", "#d4af37", "#666666", "#999999"],
        height=400,
        width=800
    )
    fig.update_traces(
        marker=dict(line=dict(width=2, color='#333333'))
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins", size=14, color="#f5f5f5" if st.session_state.theme == "sombre" else "#333333"),
        title="Résultats visuels",
        title_x=0.5
    )
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Téléchargement des résultats
    csv = pd.DataFrame({
        "PD": [pd_pred],
        "ECL": [ecl],
        "ENG": [eng],
        "LGD": [lgd],
        "Classe": [classe],
        "Secteur": [secteur]
    }).to_csv(index=False)
    st.download_button(
        label="Télécharger les résultats",
        data=csv,
        file_name="resultats.csv",
        mime="text/csv"

    )