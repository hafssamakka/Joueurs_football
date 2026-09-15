import pandas as pd
import plotly.express as px
import streamlit as st

PALETTE_BLEUS = ["#040e1b", "#50757e", "#6f843d", "#044d52", "#379f7a", "#aae8d3"]

COULEUR_TENDANCE = "#d62a2a"
COULEUR_MEDIANE = "#7a7a7a"
COULEUR_QUARTILE = "#b5b5b5"


def afficher_scatter_pac_dri(sel: pd.DataFrame) -> None:
    st.subheader("Vitesse vs Dribble")
    correlation = sel["PAC"].corr(sel["DRI"])

    q1_pac, mediane_pac, q3_pac = sel["PAC"].quantile([0.25, 0.5, 0.75])
    q1_dri, mediane_dri, q3_dri = sel["DRI"].quantile([0.25, 0.5, 0.75])

    leagues = sorted(sel.League.unique())
    if len(leagues) <= len(PALETTE_BLEUS):
        palette = {lg: PALETTE_BLEUS[i] for i, lg in enumerate(leagues)}
    else:
        palette = None  # trop de championnats : Plotly choisit une palette qualitative

    fig = px.scatter(
        sel, x="PAC", y="DRI", color="League",
        color_discrete_map=palette,
        hover_data={"Name": True, "OVR": True, "League": True, "PAC": True, "DRI": True},
        trendline="ols", trendline_scope="overall",
        trendline_color_override=COULEUR_TENDANCE,
        opacity=0.75,
    )
    fig.update_traces(marker=dict(size=8, line=dict(width=0.5, color="white")))

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
    fig.update_xaxes(range=[sel["PAC"].min() - marge, sel["PAC"].max() + marge], title="Vitesse (PAC)")
    fig.update_yaxes(range=[sel["DRI"].min() - marge, sel["DRI"].max() + marge], title="Dribble (DRI)")
    fig.update_layout(
        title="Nuage de points PAC / DRI — tendance, médiane et quartiles",
        legend_title_text="Championnat",
        height=520,
    )

    st.plotly_chart(fig, width="stretch")