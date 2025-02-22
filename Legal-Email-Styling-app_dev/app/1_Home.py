import streamlit as st
import pandas as pd  # Ajout de l'import pandas
from utils.helpers import apply_custom_css, generate_fake_data, add_logo_and_icons
import time
from utils.stats import topic_stats, legal_spam_noise

st.set_page_config(
    page_title="Home Reports",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()
add_logo_and_icons()

# Ajout d'un conteneur principal
with st.container():
    # Titre avec espacement
    st.markdown("""
        <h1 style='margin-bottom: 2rem; color: white;'>Home Reports</h1>
    """, unsafe_allow_html=True)

    # Métriques modifiées
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Number of emails", value="500k", delta="↓ 30%")
    with col2:
        st.metric(label="Collaborators", value="160")
    #with col3:
        #st.metric(label="Departments", value="87")

    # Barre de recherche et tri
    #col1, col2 = st.columns([3, 1])
    #with col1:
        #search = st.text_input("Rechercher par titre...")
    #with col2:
        #sort_option = st.selectbox(
            #"Trier par...",
            #["Aucun tri", "Valeur (croissant)", "Valeur (décroissant)", "Titre (A-Z)", "Titre (Z-A)"]
        #)

    # Ajout d'un filtre temporel
    #time_filter = st.select_slider(
        #"Période d'analyse",
        #options=["1h", "24h", "7j", "30j", "1an"],
        #value="24h"
    #)

    # Génération et filtrage des données
    #data = generate_fake_data()

    # Filtrage par recherche
    #if search:
        #data = [d for d in data if search.lower() in d["title"].lower()]

    # Tri des données
    #if sort_option != "Aucun tri":
        #if sort_option == "Valeur (croissant)":
            #data.sort(key=lambda x: x["value"])
        #elif sort_option == "Valeur (décroissant)":
            #data.sort(key=lambda x: x["value"], reverse=True)  # Correction ici - x["value"] au lieu de x: x["value"]
        #elif sort_option == "Titre (A-Z)":
            #data.sort(key=lambda x: x["title"])
        #elif sort_option == "Titre (Z-A)":
            #data.sort(key=lambda x: x["title"], reverse=True)

    # Affichage des tuiles dans une grille fixe
st.markdown("""
        <h2 style='margin-bottom: 1rem; color: white; font-size: 24px;'>Emails Topics Repartition</h2>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="grid-container">', unsafe_allow_html=True)
cols = st.columns(4)
for i, (theme, pourcentage) in enumerate(topic_stats):
    opacity = pourcentage / 70
    with cols[i % 4]:
        st.markdown(f"""
            <div class="tile" style="background: rgba(255, 50, 50, {opacity}); height: 180px;">
                <div class="tile-meta">
                    <div class="tile-title">{theme}</div>
                </div>
                <div class="tile-value">{pourcentage}%</div>
            </div>
        """, unsafe_allow_html=True)
    

st.markdown("""
        <h2 style='margin-bottom: 1rem; color: white; font-size: 24px;'>Legal-Spam-Noise</h2>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="grid-container">', unsafe_allow_html=True)
cols = st.columns(4)
for i, (theme, pourcentage) in enumerate(legal_spam_noise):
    opacity = pourcentage / 70
    with cols[i % 4]:
        st.markdown(f"""
            <div class="tile" style="background: rgba(255, 50, 50, {opacity}); height: 180px;">
                <div class="tile-meta">
                    <div class="tile-title">{theme}</div>
                </div>
                <div class="tile-value">{pourcentage}%</div>
            </div>
        """, unsafe_allow_html=True)