import math
import unicodedata
import os

import pandas as pd
import streamlit as st

API_KEY = os.environ.get("BBS_API_KEY")

_A = 9.857
_K = 0.145


def _sans_accents(texte: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", str(texte))
        if not unicodedata.combining(c)
    ).lower()


def _age_multiplicateur(age: float) -> float:
    if age <= 21:
        return 1.15
    if age <= 29:
        return 1.0
    return max(0.15, 1 - 0.09 * (age - 29))


def estimer_valeur_m_euros(ovr: float, age: float) -> float:
    base = _A * math.exp(_K * (ovr - 70))
    return round(base * _age_multiplicateur(age), 1)


def afficher_recherche_joueur(df: pd.DataFrame) -> None:
    st.subheader("***Rechercher un joueur***")

    nom_saisi = st.text_input("Nom du joueur", placeholder="ex. Kylian Mbappé")
    if not nom_saisi:
        return

    cible = _sans_accents(nom_saisi)
    correspondances = df[df["Name"].apply(_sans_accents).str.contains(cible, na=False)]

    if correspondances.empty:
        st.warning(f"Aucun joueur trouvé pour « {nom_saisi} ».")
        return

    if len(correspondances) > 1:
        choix = st.selectbox(
            f"{len(correspondances)} résultats — précise lequel :",
            correspondances["Name"].tolist(),
            key="recherche_joueur_choix",
        )
        joueur = correspondances[correspondances["Name"] == choix].iloc[0]
    else:
        joueur = correspondances.iloc[0]

    age = joueur.get("Age")
    valeur = estimer_valeur_m_euros(joueur["OVR"], age) if pd.notna(age) else None

    titre = f"**{joueur['Name']}**"
    if pd.notna(age):
        titre += f" — {int(age)} ans"
    st.markdown(titre)
    st.caption(f"{joueur.get('Position', '—')} · {joueur.get('Team', '—')}")
    st.caption(f"Championnat : {joueur.get('League', '—')} · Nation : {joueur.get('Nation', '—')}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("OVR", int(joueur["OVR"]))
    c2.metric("PAC", int(joueur["PAC"]))
    c3.metric("DRI", int(joueur["DRI"]))
    c4.metric("Valeur estimée", f"{valeur} M€" if valeur is not None else "—")