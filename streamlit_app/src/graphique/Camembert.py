import pandas as pd
import plotly.express as px
import streamlit as st

PALETTE = ["#040e1b", "#50757e", "#6f843d", "#044d52", "#379f7a", "#aae8d3"]
MAX_CATEGORIES = 6  # au-delà, on regroupe le reste dans "Autres"

LIBELLES_POSTES = {
    "GK": "Gardien de but",
    "CB": "Défenseur central",
    "LB": "Arrière gauche",
    "RB": "Arrière droit",
    "CDM": "Milieu défensif",
    "CM": "Milieu central",
    "CAM": "Milieu offensif",
    "LM": "Milieu gauche",
    "RM": "Milieu droit",
    "LW": "Ailier gauche",
    "RW": "Ailier droit",
    "ST": "Attaquant",
    "Autres": "Autres postes",
}


def afficher_camembert_poste(sel: pd.DataFrame) -> None:
    st.subheader("Répartition des joueurs sélectionnés par poste")

    comptes = sel["Position"].value_counts()

    if len(comptes) > MAX_CATEGORIES:
        top = comptes.iloc[: MAX_CATEGORIES - 1]
        autres = comptes.iloc[MAX_CATEGORIES - 1:].sum()
        comptes = pd.concat([top, pd.Series({"Autres": autres})])

    donnees = pd.DataFrame({
        "Poste": comptes.index,
        "Nombre": comptes.values,
        "Libellé": [f"{p} — {LIBELLES_POSTES.get(p, p)}" for p in comptes.index],
    })
    couleurs = dict(zip(comptes.index, PALETTE[: len(comptes)]))

    fig = px.pie(
        donnees, names="Poste", values="Nombre",
        color="Poste", color_discrete_map=couleurs,
        hover_name="Libellé",
        custom_data=["Libellé"],
    )
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="%{customdata[0]}<br>%{value} joueurs (%{percent})<extra></extra>",
        marker=dict(line=dict(color="white", width=1)),
    )
    fig.update_layout(
        title="Postes dans la sélection",
        legend_title_text="Poste",
        height=420,
    )

    st.plotly_chart(fig, width="stretch")



