import numpy as np
import pandas as pd
import plotly.express as px
from scipy.stats import gaussian_kde
import streamlit as st

COULEUR_BARRES = "#1F785C"
COULEUR_KDE = "#0a4a34"
COULEUR_MEDIANE = "#a43d3d"
N_BINS = 30


def histogramme_ovr(sel: pd.DataFrame) -> None:
    st.subheader("Distribution des notes globales (OVR)")

    valeurs = sel["OVR"].dropna()
    mediane = valeurs.median()

    fig = px.histogram(
        sel, x="OVR", nbins=N_BINS,
        color_discrete_sequence=[COULEUR_BARRES],
        opacity=0.75,
    )

    # Courbe de densité (KDE), mise à l'échelle du nombre de joueurs pour
    # rester cohérente avec l'axe Y de l'histogramme (comme kde=True en seaborn).
    largeur_bin = (valeurs.max() - valeurs.min()) / N_BINS
    kde = gaussian_kde(valeurs)
    xs = np.linspace(valeurs.min(), valeurs.max(), 200)
    ys = kde(xs) * len(valeurs) * largeur_bin
    fig.add_scatter(
        x=xs, y=ys, mode="lines", name="Densité (KDE)",
        line=dict(color=COULEUR_KDE, width=2),
    )

    fig.add_vline(
        x=mediane, line_dash="dash", line_color=COULEUR_MEDIANE,
        annotation_text=f"Médiane = {mediane:.0f}", annotation_position="top",
    )

    fig.update_layout(
        title="La distribution de OVR des joueurs",
        xaxis_title="Overall",
        yaxis_title="Nombre de joueurs",
        bargap=0.02,
        height=420,
    )

    st.plotly_chart(fig, width="stretch")