import math

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

LEAGUES_PAR_PAGE = 6

# Palette de bleus cohérente avec histogramme.py / boxplot.py
PALETTE_BLEUS = ["#040e1b", "#50757e", "#6f843d", "#044d52", "#379f7a", "#aae8d3"]

COULEUR_TENDANCE = "#d62a2a"
COULEUR_MEDIANE = "#7a7a7a"
COULEUR_QUARTILE = "#b5b5b5"


def afficher_scatter_pac_dri(sel: pd.DataFrame) -> None:
    st.subheader("Vitesse vs Dribble")
    correlation = sel["PAC"].corr(sel["DRI"])

    q1_pac, mediane_pac, q3_pac = sel["PAC"].quantile([0.25, 0.5, 0.75])
    q1_dri, mediane_dri, q3_dri = sel["DRI"].quantile([0.25, 0.5, 0.75])

    # --- Pagination par championnat ---
    leagues = sorted(sel.League.unique())
    n_pages = max(1, math.ceil(len(leagues) / LEAGUES_PAR_PAGE))

    if "scatter_page" not in st.session_state:
        st.session_state.scatter_page = 0
    st.session_state.scatter_page = min(st.session_state.scatter_page, n_pages - 1)

    col_prev, col_label, col_next = st.columns([1, 4, 1])
    with col_prev:
        if st.button("◀", key="scatter_prev", disabled=st.session_state.scatter_page == 0):
            st.session_state.scatter_page -= 1
    with col_next:
        if st.button("▶", key="scatter_next", disabled=st.session_state.scatter_page >= n_pages - 1):
            st.session_state.scatter_page += 1

    debut = st.session_state.scatter_page * LEAGUES_PAR_PAGE
    leagues_page = leagues[debut: debut + LEAGUES_PAR_PAGE]

    with col_label:
        st.markdown(
            f"<div style='text-align:center'>Championnats {debut + 1}–"
            f"{debut + len(leagues_page)} sur {len(leagues)} "
            f"(page {st.session_state.scatter_page + 1}/{n_pages})</div>",
            unsafe_allow_html=True,
        )

    page_data = sel[sel.League.isin(leagues_page)]

    # Palette calculée sur TOUS les championnats pour qu'une même ligue garde
    # toujours la même couleur, même en changeant de page.
    if len(leagues) <= len(PALETTE_BLEUS):
        palette = {lg: PALETTE_BLEUS[i] for i, lg in enumerate(leagues)}
    else:
        palette = None  # trop de championnats : Plotly choisit une palette qualitative

    fig = px.scatter(
        page_data, x="PAC", y="DRI", color="League",
        color_discrete_map=palette,
        category_orders={"League": leagues},
        hover_data={"Name": True, "OVR": True, "League": True, "PAC": True, "DRI": True},
        opacity=0.75,
    )
    fig.update_traces(marker=dict(size=8, line=dict(width=0.5, color="white")))

    # Tendance générale : calculée sur toute la sélection (pas juste la page
    # affichée), ajoutée manuellement pour rester stable d'une page à l'autre.
    pente, ordonnee = np.polyfit(sel["PAC"], sel["DRI"], 1)
    xs = np.linspace(sel["PAC"].min(), sel["PAC"].max(), 100)
    fig.add_scatter(
        x=xs, y=pente * xs + ordonnee, mode="lines",
        line=dict(color=COULEUR_TENDANCE, width=2), name="Tendance générale",
    )

    # Médiane
    fig.add_vline(
        x=mediane_pac, line_dash="dash", line_color=COULEUR_MEDIANE,
        annotation_text=f"Médiane PAC = {mediane_pac:.0f}", annotation_position="top",
    )
    fig.add_hline(
        y=mediane_dri, line_dash="dash", line_color=COULEUR_MEDIANE,
        annotation_text=f"Médiane DRI = {mediane_dri:.0f}", annotation_position="top left",
    )

    # Q1 / Q3
    fig.add_vline(x=q1_pac, line_dash="dot", line_color=COULEUR_QUARTILE,
                  annotation_text=f"Q1 PAC = {q1_pac:.0f}", annotation_position="bottom")
    fig.add_vline(x=q3_pac, line_dash="dot", line_color=COULEUR_QUARTILE,
                  annotation_text=f"Q3 PAC = {q3_pac:.0f}", annotation_position="bottom")
    fig.add_hline(y=q1_dri, line_dash="dot", line_color=COULEUR_QUARTILE,
                  annotation_text=f"Q1 DRI = {q1_dri:.0f}", annotation_position="bottom left")
    fig.add_hline(y=q3_dri, line_dash="dot", line_color=COULEUR_QUARTILE,
                  annotation_text=f"Q3 DRI = {q3_dri:.0f}", annotation_position="bottom left")

    marge = 3
    fig.update_xaxes(range=[sel["PAC"].min() - marge, sel["PAC"].max() + marge], title="Vitesse")
    fig.update_yaxes(range=[sel["DRI"].min() - marge, sel["DRI"].max() + marge], title="Dribble")
    fig.update_layout(
        title="Nuage de points de la vitesse vs le dribble — tendance, médiane et quartiles",
        legend_title_text="Championnat",
        height=520,
    )

    st.plotly_chart(fig, width="stretch")