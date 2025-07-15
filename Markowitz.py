import yfinance as yf
import pandas as pd
import numpy as np

def recuperation(titre,debut,fin,periode):
    """
    Récupération des données boursières pour un titre sur une période donnée."""
    return yf.download(titre, start=debut, end=fin, interval=periode, auto_adjust=False)

def rentabilite_attendue_portefeuille(titres, repart):
    """
    Calcul de la rentabilité attendue d'un portefeuille."""
    if len(titres) != len(repart):
        raise ValueError("Le nombre de titres et de répartitions doit être le même.")
    
#    df1 = pd.DataFrame(columns=["Rendement mensuel moyen"])
    rendement = pd.DataFrame()

    for titre in titres:
        prix = recuperation(titre, "2022-07-01", "2025-07-01", "1mo")['Adj Close']
        rendement[titre] = prix.pct_change().fillna(0)

    rendement_mensuel = rendement.mean() 
    rendement_pondere = rendement_mensuel * repart / 100
    rendement_pondere = rendement_pondere.sum()
    print(f"Rentabilité mensuelle attendue du portefeuille: {rendement_pondere:.2%}")
    rendement_annuel = (rendement_pondere + 1) ** 12 - 1
    print(f"Rentabilité annuelle attendue du portefeuille: {rendement_annuel:.2%}")

    cov = rendement.cov()
    print (f"Covariance mensuelle:\n{cov*100}")

    variance = rendement.var()
    print(f"Variance mensuelle:\n{variance*100}")


titres=['CAT', 'DSY.PA', 'RACE', 'NAK', '1WE.F','NKE','MCHA.F','PAH3.DE']
repart=[22.1,21.43,21.38,15.1,12.9,0.05,0.02,0.0015]

rentabilite_attendue_portefeuille(titres, repart)
