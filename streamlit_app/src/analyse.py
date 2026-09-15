import pandas as pd
import streamlit as st

from constantes.input_data import is_big5
from src.barre_filtre import Filtres


def filtrer_donnees(df: pd.DataFrame, filtres: Filtres) -> pd.DataFrame:
    sel = df.query(
        "OVR >= @filtres.ovr_min and PAC >= @filtres.pac_min and DRI >= @filtres.dri_min"
    )

    if filtres.ligue_sel:
        sel = sel[sel.League.isin(filtres.ligue_sel)]
    elif filtres.exclure_big5:
        sel = sel[~sel.League.apply(is_big5)]

    if filtres.poste_sel:
        sel = sel[sel.Position.isin(filtres.poste_sel)]

    if filtres.genre_sel:
        sel = sel[sel.gender.isin(filtres.genre_sel)]

    return sel


def afficher_metriques(sel: pd.DataFrame) -> None:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        with st.container(border=True):
            st.metric("Joueurs sélectionnés", len(sel))
    with c2:
        with st.container(border=True):
            st.metric("OVR moyen", round(sel.OVR.mean(), 1) if len(sel) else "—")
    with c3:
        with st.container(border=True):
            st.metric("PAC moyen", round(sel.PAC.mean(), 1) if len(sel) else "—")
    with c4:
        with st.container(border=True):
            st.metric("DRI moyen", round(sel.DRI.mean(), 1) if len(sel) else "—")
