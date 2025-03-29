import sqlalchemy
import argparse
import getpass

class MySQL(object):
    def __init__(self, user, passwd, host, database,timeout=20):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.database = database
        #try:
        self.engine = sqlalchemy.create_engine(
                'mariadb://' + self.user + ':' + self.passwd + '@' + self.host + '/' + self.database,
                )
        self.cnx = self.engine.connect()
        print("connexion réussie")

    def close(self):
        self.cnx.close()

    def execute(self, requete, liste_parametres):
        for param in liste_parametres:
            if type(param)==str:
                requete=requete.replace('?',"'"+param+"'",1)
            else:
                requete=requete.replace('?',str(param),1)
        return self.cnx.execute(requete)

def faire_factures(requete: str, mois: int, annee: int, base_donnees: MySQL):
    curseur = base_donnees.execute(requete, (mois, annee))
    
    resultat = f"Factures du {mois}/{annee}\n"
    magasin_actuel = None
    commande_actuelle = None
    total_livres = 0
    total_factures = 0
    chiffre_affaire_total = 0
    nombre_factures = 0
    nombre_livres = 0
    
    for ligne in curseur:
        magasin = ligne['nommag']
        if magasin != magasin_actuel:
            if magasin_actuel is not None:
                resultat += f"--------\nTotal {total_commande:.2f}\n"
                resultat += "--------------------------------------------------------------------------------\n"
                resultat += f"{nombre_factures} factures éditées\n"
                resultat += f"{nombre_livres} livres vendus\n"
                resultat += "********************************************************************************\n"
            resultat += f"Edition des factures du magasin {magasin}\n"
            resultat += "--------------------------------------------------------------------------------\n"
            magasin_actuel = magasin
            commande_actuelle = None
            total_commande = 0
            nombre_factures = 0
            nombre_livres = 0
        
        if ligne['numcom'] != commande_actuelle:
            if commande_actuelle is not None:
                resultat += f"--------\nTotal {total_commande:.2f}\n"
                resultat += "--------------------------------------------------------------------------------\n"
            resultat += f"{ligne['prenomcli']} {ligne['nomcli']}\n{ligne['adressecli']}\n{ligne['codepostal']} {ligne['villecli']}\n"
            resultat += f"commande n°{ligne['numcom']} du {ligne['datecom'].strftime('%d/%m/%Y')}\n"
            resultat += "ISBN                Titre                                  qte    prix     total\n"
            resultat += "--------------------------------------------------------------------------------\n"
            commande_actuelle = ligne['numcom']
            total_commande = 0
            nombre_factures += 1
        
        resultat += f"{ligne['isbn']:<20} {ligne['titre'][:35]:<35}    {ligne['qte']:<5} {ligne['prixvente']:<8.2f} {ligne['total']:<8.2f}\n"
        total_commande += ligne['total']
        total_livres += ligne['qte']
        nombre_livres += ligne['qte']
        chiffre_affaire_total += ligne['total']
    
    if commande_actuelle is not None:
        resultat += f"--------\nTotal {total_commande:.2f}\n"
        resultat += "--------------------------------------------------------------------------------\n"
        resultat += f"{nombre_factures} factures éditées\n"
        resultat += f"{nombre_livres} livres vendus\n"
        resultat += "********************************************************************************\n"
    
    resultat += f"Chiffre d’affaire total: {chiffre_affaire_total:.2f}\n"
    resultat += f"Nombre total de livres vendus: {total_livres}\n"
    
    curseur.close()
    return resultat
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--serveur",dest="nomServeur", help="Nom ou adresse du serveur de base de données", type=str, default="127.0.0.1")
    parser.add_argument("--bd",dest="nomBaseDeDonnees", help="Nom de la base de données", type=str,default='Librairie')
    parser.add_argument("--login",dest="nomLogin", help="Nom de login sur le serveur de base de donnée", type=str, default='limet')
    parser.add_argument("--requete", dest="fichierRequete", help="Fichier contenant la requete des commandes", type=str)    
    args = parser.parse_args()
    passwd = getpass.getpass("mot de passe SQL:")
    try:
        ms = MySQL(args.nomLogin, passwd, args.nomServeur, args.nomBaseDeDonnees)
    except Exception as e:
        print("La connection a échoué avec l'erreur suivante:", e)
        exit(0)
    rep=input("Entrez le mois et l'année sous la forme mm/aaaa ")
    mm,aaaa=rep.split('/')
    mois=int(mm)
    annee=int(aaaa)
    with open(args.fichierRequete) as fic_req:
        requete=fic_req.read()
    print(faire_factures(requete,mois,annee,ms))
