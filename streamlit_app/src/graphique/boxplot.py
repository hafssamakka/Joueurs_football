"""Graphique de comparaison : boxplot du dribble par poste (Plotly)."""

import pandas as pd
import plotly.express as px
import streamlit as st

COULEUR_BOITES = "#098A61"


def boxplot_dri_poste(sel: pd.DataFrame) -> None:
    st.subheader("Comparaison du dribble par poste")

    ordre = sel.groupby("Position")["DRI"].median().sort_values(ascending=False).index.tolist()

    fig = px.box(
        sel, x="Position", y="DRI",
        category_orders={"Position": ordre},
        color_discrete_sequence=[COULEUR_BOITES],
        points=False,
    )
    fig.update_layout(
        title="Dribble par poste",
        xaxis_title="Poste",
        yaxis_title="Dribble",
        height=420,
        showlegend=False,
    )

    st.plotly_chart(fig, width="stretch")