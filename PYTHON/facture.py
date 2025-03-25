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

def faire_factures(requete: str, mois: int, annee: int, bd: MySQL):
    curseur = bd.execute(requete, (mois, annee))
    
    res = f"Factures du {mois}/{annee}\n"
    current_magasin = None
    current_commande = None
    total_livres = 0
    total_factures = 0
    chiffre_affaire_global = 0
    facture_count = 0
    livre_count = 0
    
    for ligne in curseur:
        magasin = ligne['nommag']
        if magasin != current_magasin:
            if current_magasin is not None:
                res += f"--------\nTotal {total_commande:.2f}\n"
                res += "--------------------------------------------------------------------------------\n"
                res += f"{facture_count} factures éditées\n"
                res += f"{livre_count} livres vendus\n"
                res += "********************************************************************************\n"
            res += f"Edition des factures du magasin {magasin}\n"
            res += "--------------------------------------------------------------------------------\n"
            current_magasin = magasin
            current_commande = None
            total_commande = 0
            facture_count = 0
            livre_count = 0
        
        if ligne['numcom'] != current_commande:
            if current_commande is not None:
                res += f"--------\nTotal {total_commande:.2f}\n"
                res += "--------------------------------------------------------------------------------\n"
            res += f"{ligne['prenomcli']} {ligne['nomcli']}\n{ligne['adressecli']}\n{ligne['codepostal']} {ligne['villecli']}\n"
            res += f"commande n°{ligne['numcom']} du {ligne['datecom'].strftime('%d/%m/%Y')}\n"
            res += "ISBN                Titre                                  qte    prix     total\n"
            res += "--------------------------------------------------------------------------------\n"
            current_commande = ligne['numcom']
            total_commande = 0
            facture_count += 1
        
        res += f"{ligne['isbn']:<20} {ligne['titre'][:35]:<35} {ligne['qte']:<5} {ligne['prixvente']:<8.2f} {ligne['total']:<8.2f}\n"
        total_commande += ligne['total']
        total_livres += ligne['qte']
        livre_count += ligne['qte']
        chiffre_affaire_global += ligne['total']
    
    if current_commande is not None:
        res += f"--------\nTotal {total_commande:.2f}\n"
        res += "--------------------------------------------------------------------------------\n"
        res += f"{facture_count} factures éditées\n"
        res += f"{livre_count} livres vendus\n"
        res += "********************************************************************************\n"
    
    res += f"Chiffre d’affaire global: {chiffre_affaire_global:.2f}\n"
    res += f"Nombre livres vendus {total_livres}\n"
    
    curseur.close()
    return res
        


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
