import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


def histogramme_ovr(sel: pd.DataFrame) -> None:
    st.subheader("Distribution des notes globales (OVR)")
    fig, ax = plt.subplots(figsize=(5, 3.8))
    sns.histplot(sel.OVR, bins=30, kde=True, color="#1F785C", alpha=0.7)
    mediane = sel.OVR.median()
    ax.axvline(mediane, color="#a43d3d", linestyle="--", linewidth=1.5, label=f"Médiane = {mediane:.0f}",)
    ax.set_xlabel("Overall")
    ax.set_ylabel("Nombre de joueurs")
    ax.set_title("La distribution de OVR des joueurs")
    ax.legend(fontsize=6)
    st.pyplot(fig)

