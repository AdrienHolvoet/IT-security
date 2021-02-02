# Rendu "Injection"

## Binome

Nom, Prénom, email: ___
Nom, Prénom, email: ___


## Question 1

* Quel est ce mécanisme?   

La mise en place d'une vérification de l'input par une function javascript avec un regex. Donc une vérification côté client.

* Est-il efficace? Pourquoi?   
Non car c'est très simple de contourner une vérification côté client, il est préférable de faire cela côté serveur. En effet cette vérification peut-être contourner par une simple requête curl ou encore en désactivant le javascript dans la navigateur.

## Question 2

* Votre commande curl   
```
curl -d "chaine=f(-(é_à" http://localhost:8080;
```

## Question 3

* Votre commande curl pour effacer la table  

curl -d "chaine=`'; DELETE FROM chaines; --`" http://localhost:8080;



curl -d 'chaine="DELETE FROM isi.chaines//;"( --; ' http://localhost:8080;




curl -d "chaine=" http://localhost:8080;

* Expliquez comment obtenir des informations sur une autre table

## Question 4

Rendre un fichier server_correct.py avec la correction de la faille de
sécurité. Expliquez comment vous avez corrigé la faille.

## Question 5

* Commande curl pour afficher une fenetre de dialog. 

* Commande curl pour lire les cookies

## Question 6

Rendre un fichier server_xss.py avec la correction de la
faille. Expliquez la demarche que vous avez suivi.


