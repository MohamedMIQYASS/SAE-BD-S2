import numpy as np
import matplotlib.pyplot as plt

 # requete : select MONTH(datecom) as mois , count(numcom) as nbr, sum(qte*prixvente) as CA from LIVRE natural join DETAILCOMMANDE natural join COMMANDE group by mois;

CA = [7808 , 6678 , 5993 , 4803 , 6075 ,8735 ,  11105 ,  11630 ,22724 ,  16931 , 20721 , 22475 ]
NbVentes = [378 ,260 ,  262 ,240 ,  262 , 334 , 489 ,524 , 1072 ,768 , 907 , 1039 ]


plt.scatter(CA, NbVentes, color="blue", marker="o", alpha=0.7)


