from dataclasses import dataclass, field

import pandas as pd
import streamlit as st


@dataclass
class Filtres:
    ligue_sel: list = field(default_factory=list)
    exclure_big5: bool = False
    poste_sel: list = field(default_factory=list)
    genre_sel: list = field(default_factory=list)
    ovr_min: int = 75
    pac_min: int = 80
    dri_min: int = 70


def afficher_filtres(df: pd.DataFrame) -> Filtres:
    #st.subheader("Filtres")
    f1, f2, f3, f4 = st.columns(4)

    with f1:
        ligue_sel = st.multiselect("*Championnat*", sorted(df.League.unique()))
        genre_sel = []
        if "gender" in df.columns:
            genre_sel = st.multiselect("*Genre*", sorted(df.gender.dropna().unique()))
    with f2:
        poste_sel = st.multiselect("*Poste*", sorted(df.Position.unique()))
        ovr_min = st.slider("*OVR minimum*", 40, 99, 75)
    with f3:
        pac_min = st.slider("*PAC minimum (vitesse)*", 20, 99, 80)
        dri_min = st.slider("*DRI minimum (dribble)*", 20, 99, 70)
    st.divider()

    with f4: 
        exclure_big5 = st.checkbox(
                    "Exclure les 5 grands championnats",
                    value=False,
                    help="Premier League, La Liga, Serie A, Bundesliga, Ligue 1",
                )

    return Filtres(
        ligue_sel=ligue_sel,
        exclure_big5=exclure_big5,
        poste_sel=poste_sel,
        genre_sel=genre_sel,
        ovr_min=ovr_min,
        pac_min=pac_min,
        dri_min=dri_min,
    )
