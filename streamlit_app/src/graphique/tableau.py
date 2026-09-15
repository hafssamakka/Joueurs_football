import pandas as pd
import streamlit as st

COLONNES_AFFICHEES = ["Name", "League", "Position", "OVR", "PAC", "DRI", "SHO", "PAS", "PHY"]


def tableau_meilleurs_profils(sel: pd.DataFrame, top_n: int = 10) -> None:
    st.subheader("Meilleurs profils correspondant aux critères")
    colonnes = [c for c in COLONNES_AFFICHEES if c in sel.columns]
    st.dataframe(
        sel.sort_values("OVR", ascending=False)[colonnes].head(top_n),
        width='stretch',
        hide_index=True,
    )
