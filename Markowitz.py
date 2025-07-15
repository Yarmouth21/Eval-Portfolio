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

    rend = rendement.sum(axis=1)
    rendement_mensuel = rendement.mean() 
    rendement_pondere = rendement_mensuel * repart / 100
    rendement_pondere = rendement_pondere.sum()
    print(f"Rentabilité mensuelle attendue du portefeuille: {rendement_pondere:.2%}")
    rendement_annuel = (rendement_pondere + 1) ** 12 - 1
    print(f"Rentabilité annuelle attendue du portefeuille: {rendement_annuel:.2%}")

    cov = rendement.cov()
    print (f"Covariance mensuelle:\n{cov*100}")

    w= np.array(repart) / 100
    variance_portefeuille = np.dot(w.T, np.dot(cov,w))
    print (variance_portefeuille)
    ecart_type_portefeuille = np.sqrt(variance_portefeuille)
    print(f"Ecart-type mensuel du portefeuille: {ecart_type_portefeuille:.2%}")
    ecart_type_annuel = ecart_type_portefeuille * np.sqrt(12)
    print(f"Ecart-type annuel du portefeuille: {ecart_type_annuel:.2%}")

    sharpe = (rendement_annuel - 0.024) / ecart_type_annuel
    print(f"Ratio de Sharpe: {sharpe:.2f}")

    sp = yf.download('^GSPC', start="2022-07-01", end="2025-07-01", interval="1mo")['Close']
    sp_rendement = sp.pct_change().fillna(0)

    beta = rend.cov(sp_rendement.iloc[:,0]) / sp_rendement.iloc[:,0].var()
    print(f"Beta des titres par rapport au S&P500:\n{beta}")

    rendement_attendu = 0.032 + beta * (rendement_annuel - 0.032)
    print(f"Rentabilité attendue des titres:\n{rendement_attendu}")


titres=['CAT', 'DSY.PA', 'RACE', 'NAK', '1WE.F','NKE','MCHA.F','PAH3.DE']
repart=[22.1,21.43,21.38,15.1,12.9,5,2,0.1]

rentabilite_attendue_portefeuille(titres, repart)
