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

* Votre commande curl pour mettre le contenu que je souhaite dans le champ who autre que l'adresse ip 127.0.0.1
```
curl -d 'chaine=mon text%27%,%27ce que je veux%27) -- '  http://localhost:8080;
```


* Expliquez comment obtenir des informations sur une autre table

Pour obtenir les infos d'une autre table, il faudrait connaitre le nom de celle-ci et également les colonnes que l'on souhaite regarder. Et on pourrait alors combiner la commande INSERT INTO avec la commande SELECT pour selectionner les valeurs comprises dans une autres tables, les insérer dans notre table chaines qui s'affichera sur notre page web.
La commande SQL ressemblerais à ça `INSERT INTO chaines(txt,who) SELECT col1, col2 FROM otherTable`

## Question 4

Rendre un fichier server_correct.py avec la correction de la faille de
sécurité. Expliquez comment vous avez corrigé la faille.

## Question 5

* Commande curl pour afficher une fenetre de dialog. 

* Commande curl pour lire les cookies

## Question 6

Rendre un fichier server_xss.py avec la correction de la
faille. Expliquez la demarche que vous avez suivi.


