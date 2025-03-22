import numpy as np
import matplotlib.pyplot as plt

 # requete : select MONTH(datecom) as mois , count(numcom) as nbr, sum(qte*prixvente) as CA from LIVRE natural join DETAILCOMMANDE natural join COMMANDE group by mois;



# Création des listes représentant les chiffres d'affaire et les nombres de ventes :

CA  = np.array([7808 , 6678 , 5993 , 4803 , 6075 ,8735 ,  11105 ,  11630 ,22724 ,  16931 , 20721 , 22475 ])
NbVentes = np.array([378 ,260 ,  262 ,240 ,  262 , 334 , 489 ,524 , 1072 ,768 , 907 , 1039 ])

# Calcul de la moyenne de ces 2 listes :

mean_CA = sum(CA)/ len(CA)
mean_Nbventes = sum(NbVentes)/ len(NbVentes)

# Calcul de la différences ce ces 2 listes et leur moyenne ; 

CA_diff = [ca - mean_CA for ca in CA]
NbVentes_diff = [nb - mean_Nbventes for nb in NbVentes]

# Calcul de la somme des produits des écarts quadratiques : 

num = sum(xd * yd for xd, yd in zip(CA_diff, NbVentes_diff))

# Calcul du dénominateur des 2 listes : 

denom_CA = sum(xd ** 2 for xd in CA_diff)
denom_Nbventes = sum(yd ** 2 for yd in NbVentes_diff)

# Calcul du coefficient de correlation : 

correlation = num / (np.sqrt(denom_CA) * np.sqrt(denom_Nbventes))
print("Coefficient de correlation de Pearson :", correlation)

# Representation graphique :

plt.scatter(CA, NbVentes, color="yellow", marker="o", alpha=0.7)

# Fonction python qui permet de représenter la droite de regression linéaire :

def regression_lineaire(CA , NbVentes):
    a = sum(xd * yd for xd , yd  in zip(CA_diff, NbVentes_diff)) / denom_CA
    b = mean_Nbventes - a * mean_CA
    plt.plot([0,25000],[b,a*25000+b])
    plt.show()
 
regression_lineaire(CA,NbVentes)




















































