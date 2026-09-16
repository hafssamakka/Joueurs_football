# Cellule de recrutement — Dashbord Streamlit

**Question métier.** Le directeur sportif cherche des profils précis (ex. « ailier rapide et bon dribbleur, hors des cinq grands championnats, OVR > 75 »). Le tableau de bord doit permettre de filtrer instantanément la base de joueurs selon ces critères et de comparer les profils retenus.

**Filtres.** Championnat (avec un raccourci « exclure les 5 grands championnats », détecté par sous-chaîne pour s'adapter aux libellés exacts du CSV), poste, genre (si la colonne `gender` est présente), et trois seuils numériques (OVR, PAC, DRI). Une seule source de vérité : le DataFrame `sel`, recalculé à chaque interaction et utilisé par les métriques, les graphiques et le tableau.

**Choix des graphiques.**
- *Histogramme (OVR)* : une distribution — pour juger si le vivier sélectionné est homogène ou très étalé en niveau.
- *Boxplot (DRI par poste)* : une comparaison de groupes — pour repérer quels postes tirent la médiane de dribble vers le haut dans la sélection.
- *Nuage de points (PAC vs DRI)* : une relation entre deux variables continues — pour repérer visuellement les joueurs qui combinent vitesse et dribble, avec la taille des points encodant l'OVR et la couleur le championnat.

**Honnêteté visuelle.** Histogramme à zéro sur l'axe des effectifs, mêmes échelles PAC/DRI (20–99) pour rendre les comparaisons lisibles, palette catégorielle limitée pour le nuage de points.

**Limite du dataset.** Sans fichier `joueurs.csv` fourni, l'app génère des données synthétiques à but de démonstration uniquement — les corrélations qu'on y observe (ex. DRI corrélé à PAC) sont artificielles et ne reflètent pas de vrais joueurs.

**Lancement :** `pip install streamlit pandas seaborn matplotlib` puis `streamlit run app.py`.
