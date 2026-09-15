import matplotlib.pyplot as plt
import pandas as pd
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

    fig, ax = plt.subplots(figsize=(12, 4))
    couleurs = PALETTE[: len(comptes)]
    wedges, _, _ = ax.pie(
        comptes.values,
        autopct="%1.0f%%",
        colors=couleurs,
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1},
        textprops={"color": "black", "fontsize": 10},
    )
    # legende pour expliquer la signification de chaque code de poste
    libelles = [f"{poste} — {LIBELLES_POSTES.get(poste, poste)}" for poste in comptes.index]
    ax.legend(wedges, libelles, title="Postes", bbox_to_anchor=(1.05, 1), loc="upper left")

    ax.set_title("Postes dans la sélection")
    ax.axis("equal")
    st.pyplot(fig)