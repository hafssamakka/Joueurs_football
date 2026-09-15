import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

LEAGUES_PAR_PAGE = 6

PALETTE_BLEUS = ["#040e1b", "#50757e", "#6f843d", "#044d52", "#379f7a", "#aae8d3"]

COULEUR_MEDIANE = "#7a7a7a"


def _niveau_ovr(sel: pd.DataFrame, q: int = 3) -> pd.Series:
    """Regroupe l'OVR continu en quelques tranches lisibles (au lieu de 7+
    valeurs numériques proches dans la légende)."""
    try:
        cats = pd.qcut(sel["OVR"], q=q, duplicates="drop")
    except ValueError:
        # Trop peu de valeurs distinctes pour découper : une seule tranche
        return pd.Series(["Tous niveaux"] * len(sel), index=sel.index)
    labels = [f"OVR {int(iv.left)}–{int(iv.right)}" for iv in cats.cat.categories]
    return cats.cat.rename_categories(labels)


def afficher_scatter_pac_dri(sel: pd.DataFrame) -> None:
    st.subheader("Vitesse vs Dribble")
    correlation = sel["PAC"].corr(sel["DRI"])
    mediane_pac = sel["PAC"].median()
    mediane_dri = sel["DRI"].median()

    leagues = sorted(sel.League.unique())
    n_pages = max(1, math.ceil(len(leagues) / LEAGUES_PAR_PAGE))

    if "scatter_page" not in st.session_state:
        st.session_state.scatter_page = 0
    st.session_state.scatter_page = min(st.session_state.scatter_page, n_pages - 1)

    # la pagination
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

    page_data = sel[sel.League.isin(leagues_page)].copy()
    page_data["Niveau OVR"] = _niveau_ovr(page_data)
    palette = dict(zip(leagues_page, PALETTE_BLEUS[: len(leagues_page)]))

    fig, ax = plt.subplots(figsize=(9, 4.8))
    sns.scatterplot(
        data=page_data, x="PAC", y="DRI", hue="League", size="Niveau OVR",
        sizes=(40, 220), palette=palette, ax=ax, alpha=0.75, edgecolor="white", linewidth=0.3,
    )
    sns.regplot(
        data=sel, x="PAC", y="DRI", scatter=False, ax=ax,
        color="#d62a2a", line_kws={"linewidth": 2}, label="Tendance générale",
    )

    # Médianes : repères de lecture rapide, calculées sur toute la sélection
    ax.axvline(
        mediane_pac, color=COULEUR_MEDIANE, linestyle="--", linewidth=1.2,
        label=f"Médiane PAC = {mediane_pac:.0f}",
    )
    ax.axhline(
        mediane_dri, color=COULEUR_MEDIANE, linestyle="--", linewidth=1.2,
        label=f"Médiane DRI = {mediane_dri:.0f}",
    )

    marge = 3
    ax.set_xlim(sel["PAC"].min() - marge, sel["PAC"].max() + marge)
    ax.set_ylim(sel["DRI"].min() - marge, sel["DRI"].max() + marge)
    ax.set_xlabel("Vitesse")
    ax.set_ylabel("Dribble")
    ax.set_title("Nuage de points PAC / DRI, avec tendance générale et médianes")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    st.pyplot(fig)