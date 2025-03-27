import numpy as np
import matplotlib.pyplot as plt

 # requete : select MONTH(datecom) as mois , count(numcom) as nbr, sum(qte*prixvente) as CA from LIVRE natural join DETAILCOMMANDE natural join COMMANDE group by mois;



# Création des listes représentant les chiffres d'affaire et les nombres de ventes :
CA = np.array([7808, 6678, 5993, 4803, 6075, 8735, 11105, 11630, 22724, 16931, 20721, 22475])
NbVentes = np.array([378, 260, 262, 240, 262, 334, 489, 524, 1072, 768, 907, 1039])

# Calcul des moyennes
mean_CA = np.mean(CA)
mean_Nbventes = np.mean(NbVentes)

# Calcul des écarts à la moyenne
CA_diff = CA - mean_CA
NbVentes_diff = NbVentes - mean_Nbventes

# Calcul de la somme des produits des écarts quadratiques
num = np.sum(NbVentes_diff * CA_diff)

# Calcul du dénominateur
denom_Nbventes = np.sum(NbVentes_diff ** 2)

# Calcul du coefficient de correlation de Pearson
correlation = num / (np.sqrt(np.sum(CA_diff**2)) * np.sqrt(denom_Nbventes))
print("Coefficient de corrélation de Pearson :", correlation)

# Représentation graphique
plt.scatter(NbVentes, CA, color="red", marker="o", alpha=0.7)

# Fonction de régression linéaire
def regression_lineaire(NbVentes, CA):
 a = num / denom_Nbventes 
 b = mean_CA - a * mean_Nbventes 
 plt.plot([0, max(NbVentes)], [b, a * max(NbVentes) + b], color="blue")
 plt.show()

regression_lineaire(NbVentes, CA)