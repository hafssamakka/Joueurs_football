
from pathlib import Path

import streamlit as st

from constantes.input_data import load_data, using_demo_data
from src.analyse import filtrer_donnees, afficher_metriques
from src.barre_filtre import afficher_filtres
from src.recherche_joueur import afficher_recherche_joueur
from src.graphique import (
    histogramme_ovr,
    boxplot_dri_poste,
    afficher_scatter_pac_dri,
    tableau_meilleurs_profils,
    afficher_camembert_poste,
)

def set_page() -> None:
    path_logo = Path(__file__).resolve().parents[1] / "ballon.avif"
    st.set_page_config(
        page_title="Cellule de recrutement : Joueurs de football",
        page_icon=str(path_logo),
        layout="wide",
    )

    logo_col, title_col = st.columns([0.12, 0.88], vertical_alignment="center")
    with logo_col:
        st.image(str(path_logo), width=80)
    with title_col:
        st.title("***Cellule de recrutement : Joueurs de football***")
    
    if using_demo_data():
        st.info(
            "Aucun fichier `all_players_clean.csv` trouvé — un jeu de données "
            "synthétique est utilisé à titre de démonstration.",
            icon="ℹ️",
        )


def main() -> None:
    set_page()

    df = load_data()

    afficher_recherche_joueur(df)
    st.divider()

    filtres = afficher_filtres(df)
    sel = filtrer_donnees(df, filtres)

    afficher_metriques(sel)
    st.divider()

    if sel.empty:
        st.warning(
            "Aucun joueur ne correspond à ces critères. Essayez d'assouplir "
            "un filtre (seuils plus bas, plus de championnats ou de postes)."
        )
        return

    col_a, col_b = st.columns(2)
    with col_a:
        histogramme_ovr(sel)
    with col_b:
        boxplot_dri_poste(sel)

    afficher_camembert_poste(sel)
    afficher_scatter_pac_dri(sel)
    st.divider()
    tableau_meilleurs_profils(sel)


if __name__ == "__main__":
    main()