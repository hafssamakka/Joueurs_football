import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


def boxplot_dri_poste(sel: pd.DataFrame) -> None:
    st.subheader("Comparaison du dribble par poste")
    fig, ax = plt.subplots(figsize=(5, 3.8))
    ordre = sel.groupby("Position")["DRI"].median().sort_values(ascending=False).index
    sns.boxplot(
        data=sel, x="Position", y="DRI", order=ordre, ax=ax,
        color="#098A61", showfliers=False,
    )
    ax.set_xlabel("Poste")
    ax.set_ylabel("Dribble")
    ax.set_title("Dribble par poste")
    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig)
