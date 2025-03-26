-- Devoir 127
-- Nom: KURAC , Prenom: ADNAN-ERDEM
-- Nom: MIQYASS , Prenom: MOHAMED


-- Feuille SAE2.05 Exploitation d'une base de données: Livre Express
-- 
-- Veillez à bien répondre aux emplacements indiqués.
-- Seule la première requête est prise en compte.

-- +-----------------------+--
-- * Question 127156 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Quels sont les livres qui ont été commandés le 1er décembre 2024 ?

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +---------------+--------------------------------------------+---------+-----------+-------+
-- | isbn          | titre                                      | nbpages | datepubli | prix  |
-- +---------------+--------------------------------------------+---------+-----------+-------+
-- | etc...
-- = Reponse question 127156.
select isbn, titre, nbpages, datepubli, prix 
from LIVRE natural join DETAILCOMMANDE 
where numcom in (select numcom from COMMANDE where datecom = '2024-12-01');


-- +-----------------------+--
-- * Question 127202 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Quels clients ont commandé des livres de René Goscinny en 2021 ?

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+---------+-----------+-----------------------------+------------+-------------+
-- | idcli | nomcli  | prenomcli | adressecli                  | codepostal | villecli    |
-- +-------+---------+-----------+-----------------------------+------------+-------------+
-- | etc...
-- = Reponse question 127202.
select idcli, nomcli, prenomcli, adressecli, codepostal, villecli 
from CLIENT 
natural join COMMANDE natural join DETAILCOMMANDE natural join LIVRE natural join ECRIRE natural join AUTEUR 
where nomauteur = 'René Goscinny' and YEAR(datecom) = 2021;


-- +-----------------------+--
-- * Question 127235 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Quels sont les livres sans auteur et étant en stock dans au moins un magasin en quantité strictement supérieure à 8 ?

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +---------------+-----------------------------------+-------------------------+-----+
-- | isbn          | titre                             | nommag                  | qte |
-- +---------------+-----------------------------------+-------------------------+-----+
-- | etc...
-- = Reponse question 127235.
select isbn,titre,nommag,qte
from LIVRE natural left join ECRIRE natural join POSSEDER natural join MAGASIN
where idmag is null and qte > 8;


-- +-----------------------+--
-- * Question 127279 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Pour chaque magasin, on veut le nombre de clients qui habitent dans la ville de ce magasin (en affichant les 0)

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+-------------------------+-------+
-- | idmag | nommag                  | nbcli |
-- +-------+-------------------------+-------+
-- | etc...
-- = Reponse question 127279.
select idmag, nommag, count(idcli) as nbcli
from MAGASIN natural join COMMANDE natural join CLIENT 
where villecli = villemag
group by idmag;


-- +-----------------------+--
-- * Question 127291 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Pour chaque magasin, on veut la quantité de livres achetés le 15/09/2022 en affichant les 0.

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------------+------+
-- | nommag                  | nbex |
-- +-------------------------+------+
-- | etc...
-- = Reponse question 127291.
with aaa as(select * from COMMANDE natural join DETAILCOMMANDE where datecom = '2022-09-15')
select nommag, IFNULL(sum(qte),0) as nbex from MAGASIN natural left join aaa group by nommag;



-- +-----------------------+--
-- * Question 127314 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Instructions d'insertion dans la base de données

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +------------+
-- | insertions |
-- +------------+
-- | etc...
-- = Reponse question 127314.

-- insertions dans la tables EDITEUR :

insert into EDITEUR(nomedit , idedit) values ('First Interactive' , 240);

-- insertions dans la table AUTEUR  :

insert into AUTEUR(idauteur , nomauteur , anneenais , anneedeces) values 
('OL246259A' , 'Allen G. Taylor' , NULL , NULL ), 	
('OL7670824A' , 'Reinhard Engel' , NULL , NULL);

-- insertions dans la table LIVRE : 

insert into LIVRE(isbn , titre , nbpages , datepubli , prix) values 
('9782844273765' , 'SQL pour les Nuls' , 292 , 2002 , 33.5);


-- insertions dans la table EDITER :

insert into EDITER(isbn , idauteur) values ('9782844273765',240);


-- insertions dans la table ECRIRE :

insert into ECRIRE(isbn,idauteur) values 	('9782844273765','OL246259A'),
('9782844273765' , 'OL7670824A');


-- insertions dans la table POSSEDER :

insert into POSSEDER(idmag,isbn,qte) values (7, '9782844273765' ,3);


-- +-----------------------+--
-- * Question 127369 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 1 Nombre de livres vendus par magasin et par an

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------------+-------+-----+
-- | Magasin                 | Année | qte |
-- +-------------------------+-------+-----+
-- | etc...
-- = Reponse question 127369.
select nommag Magasin, YEAR(datecom) as Année, sum(qte) as qte
from MAGASIN natural join COMMANDE natural join DETAILCOMMANDE
group by nommag, YEAR(datecom);


-- +-----------------------+--
-- * Question 127370 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 2  Chiffre d'affaire par thème en 2024

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +--------------------------------------+---------+
-- | Theme                                | Montant |
-- +--------------------------------------+---------+
-- | etc...
-- = Reponse question 127370.
select nomclass as Theme, IFNULL(sum(prixvente*qte),0) as Montant 
from CLASSIFICATION natural join THEMES natural join LIVRE natural join DETAILCOMMANDE
group by nomclass;



-- +-----------------------+--
-- * Question 127381 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 3 Evolution chiffre d'affaire par magasin et par mois en 2024

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +------+-------------------------+---------+
-- | mois | Magasin                 | CA      |
-- +------+-------------------------+---------+
-- | etc...
-- = Reponse question 127381.
select Month(datecom) mois, nommag Magasin, IFNULL(sum(prixvente*qte),0) CA from 
MAGASIN natural join COMMANDE natural join DETAILCOMMANDE 
group by mois,nommag;


-- +-----------------------+--
-- * Question 127437 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 4 Comparaison ventes en ligne et ventes en magasin

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+------------+---------+
-- | annee | typevente  | montant |
-- +-------+------------+---------+
-- | etc...
-- = Reponse question 127437.
select YEAR(datecom) annee, enligne as typevente, IFNULL(sum(prixvente*qte),0) montant
from COMMANDE natural join DETAILCOMMANDE
group by YEAR(datecom), enligne;


-- +-----------------------+--
-- * Question 127471 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 5

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------+-----------+
-- | Editeur           | nbauteurs |
-- +-------------------+-----------+
-- | etc...
-- = Reponse question 127471.
select nomedit as Editeur, count(idauteur) nbauteurs from 
EDITEUR natural join EDITER natural join LIVRE natural join ECRIRE natural join AUTEUR
group by Editeur order by nbauteurs desc limit 10;


-- +-----------------------+--
-- * Question 127516 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 6 Origine des clients ayant acheter des livres de R. Goscinny

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------+-----+
-- | ville       | qte |
-- +-------------+-----+
-- | etc...
-- = Reponse question 127516.

select villecli ville, sum(qte) as qte from CLIENT 
natural join COMMANDE natural join DETAILCOMMANDE natural join LIVRE natural join ECRIRE natural join AUTEUR
where nomauteur = 'René Goscinny'
group by villecli;



-- +-----------------------+--
-- * Question 127527 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 7 Valeur du stock par magasin

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------------+---------+
-- | Magasin                 | total   |
-- +-------------------------+---------+
-- | etc...
-- = Reponse question 127527.

select nommag as Magasin , IFNULL(sum(qte*prix),0) as total 
from MAGASIN natural join POSSEDER natural join LIVRE
group by Magasin;



-- +-----------------------+--
-- * Question 127538 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:


--  Requête Graphique 8 Statistiques sur l'évolution du chiffre d'affaire total par client 


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+---------+---------+---------+
-- | annee | maximum | minimum | moyenne |
-- +-------+---------+---------+---------+
-- | etc...
-- = Reponse question 127538.
with Client as (select YEAR(datecom) annee, idcli, sum(prixvente*qte)as CA from COMMANDE natural join DETAILCOMMANDE group by YEAR(datecom), idcli) -- ici on calcule pour chaque annee et client, LE CA
select annee, max(CA) as maximum, min(CA) as minimum, ROUND(avg(CA),2) as moyenne from Client group by annee;






-- +-----------------------+--
-- * Question 127572 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête imprimer les commandes en considérant que l'on veut celles de février 2020

--  Requête Palmarès


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+-----------------------+-------+
-- | annee | nomauteur             | total |
-- +-------+-----------------------+-------+
-- | etc...
-- = Reponse question 127572.

with LivreVendu as (select YEAR(datecom) as annee, idauteur, sum(qte) total from ECRIRE
 natural join LIVRE 
 natural join DETAILCOMMANDE 
 natural join COMMANDE where YEAR(datecom) != 2025
 group by annee,idauteur
 order by total desc)

select annee, nomauteur, max(total) from LivreVendu natural left join AUTEUR group by annee;








