import numpy as np
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# from dashboard import traiter_donnees_villas

from dashboad import traiter_donnees_appartements_, traiter_donnees_villas_, traiter_donnees_terrains_
from scraping import scraper_appartements_raw, scraper_terrains_raw, scraper_villas_raw
from traitement import traiter_donnees_appartements, traiter_donnees_terrains,traiter_donnees_villas  # Assure-toi que le fichier scraping.py est bien dans le même dossier
st.set_page_config(layout="wide")

# --- Configuration de la page ---
st.set_page_config(page_title="Projet Coinafrica", layout="wide")

# --- Style pour les tabs ---
st.markdown(
    """
    <style>
    div[data-baseweb="tab-list"] {
        justify-content: space-between;
    }
    div[data-baseweb="tab"] {
        flex: 1;
        text-align: center;
    }


       /* Style de la sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0A6C6A;  /* Fond vert foncé */
        color: white;               /* Couleur du texte */
    }

    /* Style du header de la sidebar */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        color: #FFFFFF;
    }

    /* Style des labels/selectbox/titres dans la sidebar */
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stTextInput label {
        color: white !important;
    }

    /* Améliorer le padding */
    section[data-testid="stSidebar"] > div {
        padding: 1rem;
    }

    
    </style>
    """,
    unsafe_allow_html=True
)

# --- Titre principal ---
st.title("🧹 Application de Scraping - Coinafrica")

# --- Sidebar ---
st.sidebar.header("🎛️ Paramètres")


# Sélection de la tâche
choix_action = st.sidebar.selectbox(
    "Choisir une action",
    [
        "Scraper avec BeautifulSoup",
        "Télécharger données Web Scraper",
        "Voir dashboard des données",
        "Remplir le formulaire d’évaluation"
    ]
)

# --- Corps principal ---
if choix_action == "Scraper avec BeautifulSoup":
    st.subheader("📦 Scraping avec BeautifulSoup ou Selenium")
    # Sélection du nombre de pages
    nb_pages = st.sidebar.selectbox("Nombre de pages à scraper", list(range(1, 201)), index=0)

    st.write(f"Nombre de pages à scraper : {nb_pages}")
    st.markdown("### Choisissez une catégorie à scraper :")

    if st.button("Charger les villas"):
        with st.spinner("Scraping en cours..."):
            df_villas = scraper_villas_raw(nb_pages)

            # Convertir en DataFrame si nécessaire
            if isinstance(df_villas, list):
                df_villas = pd.DataFrame(df_villas)
        if not df_villas.empty:
            st.success("Scraping terminé ✅")

            # 💡 Traitement des données
            with st.spinner("🧹 Traitement des données..."):
                df_villas_traitees = traiter_donnees_villas(df_villas)

            st.subheader("📊 Données des villas (nettoyées)")
            st.dataframe(df_villas_traitees, use_container_width=True)


            st.download_button(
                label="📥 Télécharger le CSV nettoyé",
                data=df_villas_traitees.to_csv(index=False),
                file_name="villas_nettoyes.csv",
                mime="text/csv"
            )

        else:
            st.warning("⚠️ Aucune donnée trouvée. Vérifie le site ou essaie une autre page.")

    if st.button("Charger les terrains"):
        with st.spinner("⏳ Scraping en cours..."):
            df_terrains = scraper_terrains_raw(nb_pages)
            # Convertir en DataFrame si nécessaire
            if isinstance(df_terrains, list):
                df_terrains = pd.DataFrame(df_terrains)

        if not df_terrains.empty:
            st.success("Scraping terminé ✅")

            # 💡 Traitement des données
            with st.spinner("🧹 Traitement des données..."):
                df_terrains_traitees = traiter_donnees_terrains(df_terrains)

            st.subheader("📊 Données des terrains (nettoyées)")
            st.dataframe(df_terrains_traitees, use_container_width=True)

            st.download_button(
                label="📥 Télécharger le CSV nettoyé",
                data=df_terrains_traitees.to_csv(index=False),
                file_name="terrains_nettoyes.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Aucune donnée trouvée. Vérifie le site ou essaie une autre page.")


    if st.button("Charger les appartements"):
        with st.spinner("⏳ Scraping en cours..."):
            data_appartements = scraper_appartements_raw(nb_pages)
            # Convertir en DataFrame si nécessaire
            if isinstance(data_appartements, list):
                df_appartements = pd.DataFrame(data_appartements)
            else:
                df_appartements = data_appartements

        if not df_appartements.empty:
            st.success("Scraping terminé ✅")

            # 💡 Traitement des données
            with st.spinner("🧹 Traitement des données..."):
                df_appartements_traitees = traiter_donnees_appartements(df_appartements)

            st.subheader("📊 Données des appartements (nettoyées)")
            st.dataframe(df_appartements_traitees, use_container_width=True)

            st.download_button(
                label="📥 Télécharger le CSV nettoyé",
                data=df_appartements_traitees.to_csv(index=False),
                file_name="appartements_nettoyes.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Aucune donnée trouvée. Vérifie le site ou essaie une autre page.")


elif choix_action == "Télécharger données Web Scraper":
    st.subheader("💾 Téléchargement et affichage de données Web Scraper")
    with st.container():
        tabs = st.tabs(["🏠 Villas", "🌍 Terrains", "🏢 Appartements"])

        with tabs[0]:
            st.markdown("### Données Web Scraper - Villas")
            try:
                df_villas = pd.read_csv("data/Scrapper_villas.csv")
                st.dataframe(df_villas, use_container_width=True)

                st.download_button(
                    label="📥 Télécharger le CSV - Villas",
                    data=df_villas.to_csv(index=False),
                    file_name="villas_non_nettoyes.csv",
                    mime="text/csv"
                )
            except Exception:
                st.error("Erreur lors du chargement du fichier Villas.")

        with tabs[1]:
            st.markdown("### Données Web Scraper - Terrains")
            try:
                df_terrains = pd.read_csv("data/Scrapper_Terrains.csv")
                st.dataframe(df_terrains, use_container_width=True)

                st.download_button(
                    label="📥 Télécharger le CSV - Terrains",
                    data=df_terrains.to_csv(index=False),
                    file_name="terrains_non_nettoyes.csv",
                    mime="text/csv"
                )
            except Exception:
                st.error("Erreur lors du chargement du fichier Terrains.")

        with tabs[2]:
            st.markdown("### Données Web Scraper - Appartements")
            try:
                df_apparts = pd.read_csv("data/Scrapper_Appartements.csv")
                st.dataframe(df_apparts, use_container_width=True)

                st.download_button(
                    label="📥 Télécharger le CSV - Appartements",
                    data=df_apparts.to_csv(index=False),
                    file_name="appartements_non_nettoyes.csv",
                    mime="text/csv"
                )
            except Exception:
                st.error("Erreur lors du chargement du fichier Appartements.")


elif choix_action == "Voir dashboard des données":
    st.subheader("📊 Dashboard des données")
    tabs = st.tabs(["🏠 Villas", "🌍 Terrains", "🏢 Appartements"])

    with tabs[0]:
        st.markdown("### Statistiques Villas")
        try:
            raw = pd.read_csv("data/Scrapper_villas.csv")
            df = traiter_donnees_villas_(raw)
            st.table(df.iloc[0:10])
            
            st.markdown("### Statistiques générales sur les Villas")
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Nombre total de villas", len(df))

            col2.metric("Moyenne de pièces", f"{df['Pieces'].mean():.1f}")

            col3.metric("Moyenne de salles de bain", f"{df['Salles_bain'].mean():.1f}")

            col4.metric("Superficie moyenne", f"{df['Superficie'].mean():.0f} m²")

            st.markdown("#### 🏘️ Quartiers les plus fréquents")
            st.write(df['Adresse'].value_counts().head(5))

            # Heatmap des corrélations
            st.markdown("#### 📊 Corrélation entre les variables numériques")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.heatmap(df[['Pieces', 'Salles_bain', 'Superficie']].corr(), annot=True, cmap="YlGnBu", ax=ax2)
            st.pyplot(fig2)

        except Exception as e:
            st.warning(f"Erreur : {e}")

    with tabs[1]:
        st.markdown("### Statistiques Terrains")
        try:
            # Charger les données brutes
            raw_terrains = pd.read_csv("data/Scrapper_Terrains.csv")
            # Nettoyage avec ta fonction
            df_terrains = traiter_donnees_terrains_(raw_terrains)
            # Affichage dans le dashboard
            st.table(df_terrains.iloc[0:10])


            st.markdown("### Statistiques générales sur les Terrains")

            col1, col2 = st.columns(2)

            col1.metric("Nombre total de terrains", len(df_terrains))
            col2.metric("Superficie moyenne", f"{df_terrains['Superficie'].mean():.0f} m²")

            st.markdown("#### 🏘️ Quartiers les plus fréquents")
            st.write(df_terrains['Adresse'].value_counts().head(5))

            # Corrélation : Prix vs Superficie (si 'Prix' est présent)
            if 'Prix' in df_terrains.columns:
                st.markdown("#### 📊 Corrélation entre Prix et Superficie")
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.heatmap(df_terrains[['Superficie', 'Prix']].corr(), annot=True, cmap="YlGnBu", ax=ax)
                st.pyplot(fig)

        except Exception as e:
            st.warning(f"Erreur : {e}")

    with tabs[2]:
        st.markdown("### Statistiques Appartements")
        try:
            # Chargement et traitement
            raw = pd.read_csv("data/Scrapper_Appartements.csv")
            df = traiter_donnees_appartements_(raw)

            # Aperçu des 10 premières lignes
            st.table(df.iloc[0:10])

            # Statistiques générales
            st.markdown("### Statistiques générales sur les Appartements")
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Nombre total d'appartements", len(df))
            col2.metric("Moyenne de pièces", f"{df['Pieces'].mean():.1f}")
            col3.metric("Moyenne de salles de bain", f"{df['Salles_bain'].mean():.1f}")
            col4.metric("Superficie moyenne", f"{df['Superficie'].mean():.0f} m²")

            # Quartiers les plus fréquents
            st.markdown("#### 🏘️ Quartiers les plus fréquents")
            st.write(df['Adresse'].value_counts().head(5))

            # Heatmap de corrélation
            st.markdown("#### 📊 Corrélation entre les variables numériques")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.heatmap(df[['Pieces', 'Salles_bain', 'Superficie']].corr(), annot=True, cmap="YlGnBu", ax=ax2)
            st.pyplot(fig2)
        except Exception as e:
            st.warning(f"Erreur : {e}")

elif choix_action == "Remplir le formulaire d’évaluation":
    st.subheader("📝 Formulaire d’évaluation")

    st.info("Merci de prendre une minute pour partager votre avis sur l'application.")
    st.markdown("Vos réponses sont confidentielles et utilisées uniquement à des fins d'amélioration.")

    st.markdown("""
        <iframe src="https://ee.kobotoolbox.org/i/QjLrf0Fb" width="100%" height="700" style="border:none;"></iframe>
    """, unsafe_allow_html=True)
