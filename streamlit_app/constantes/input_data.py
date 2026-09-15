import os

import numpy as np
import pandas as pd
import streamlit as st

CSV_PATH = "all_players_clean.csv"

BIG5_KEYWORDS = ["premier league", "la liga", "laliga", "serie a", "bundesliga", "ligue 1"]


def is_big5(league_name) -> bool:
    """Renvoie True si le championnat fait partie des 5 grands championnats."""
    l = str(league_name).lower()
    return any(k in l for k in BIG5_KEYWORDS)


def _generer_donnees_demo(n: int = 1200) -> pd.DataFrame:
    """Jeu de données synthétique de secours, utilisé si le CSV est absent."""
    rng = np.random.default_rng(42)
    leagues = [
        "Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1",
        "Eredivisie", "Liga Portugal", "Jupiler Pro League",
        "Super Lig", "MLS",
    ]
    positions = ["GK", "CB", "LB", "RB", "CDM", "CM", "CAM", "LW", "RW", "ST"]
    df = pd.DataFrame({
        "Name": [f"Joueur {i}" for i in range(n)],
        "League": rng.choice(leagues, n, p=[.14, .14, .14, .14, .14, .08, .08, .06, .06, .02]),
        "Position": rng.choice(positions, n),
        "PAC": rng.integers(40, 99, n),
    })
    df["DRI"] = np.clip(df["PAC"] * 0.5 + rng.integers(20, 60, n), 30, 99)
    df["SHO"] = rng.integers(30, 95, n)
    df["PAS"] = rng.integers(30, 95, n)
    df["PHY"] = rng.integers(40, 95, n)
    df["OVR"] = np.clip(
        (df["PAC"] + df["DRI"] + df["SHO"] + df["PAS"] + df["PHY"]) / 5
        + rng.integers(-5, 6, n),
        45, 94,
    ).astype(int)
    df["gender"] = rng.choice(["Male", "Female"], n, p=[0.85, 0.15])
    return df


@st.cache_data
def load_data(path: str = CSV_PATH) -> pd.DataFrame:
    if os.path.exists(path):
        return pd.read_csv(path)
    return _generer_donnees_demo()


def using_demo_data(path: str = CSV_PATH) -> bool:
    return not os.path.exists(path)
