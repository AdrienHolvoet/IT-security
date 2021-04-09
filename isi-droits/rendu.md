# Rendu "Les droits d’accès dans les systèmes UNIX"

## Binôme

- Nom, Prénom, email: KROL, Mikolaï, mikolai.krol.etu@univ-lille.fr

- Nom, Prénom, email: HOLVOET, Adrien, adrien.holvoet.etu@univ-lile.fr

## Question 1

Non toto ne peut pas écrire car il a seulement accès en lecture. Les droits de l’utilisateur ont un plus gros privilège que les droits de  groupe

## Question 2

### Que signifie le caractère x pour un répertoire ?
 
Lorsque ce droit est attribué à un répertoire, il autorise l'accès (ou ouverture) au répertoire.

### Maintenant, avec l’utilisateur toto, essayez d’entrer dans le répertoire avec cd mydir. — Que se passe-t-il ? Pourquoi ?


On ne peut pas y rentrer/ouvrir car on a enlevé les droits d'exécution au groupe ubuntu :
-bash: cd: mydir: Permission denied

### Maintenant, avec l’utilisateur toto essayez de lister le contenu du répertoire avec ls -al mydir. — Que se passe-t-il ? Pourquoi ?


- commande : cd mydir/  
  réponse : bash: cd: mydir/: Permission denied
- commande : toto@holvoet-tp-isi:/home/ubuntu$ ls mydir/    
reponse : ls: cannot access 'mydir/data.txt': Permission denied
data.txt


On voit qu’il y a le fichier data.txt dans le dossier mydir car on a les droits en lecture sur le dossier, mais on n’a pas plus d’informations puisque nous n’avons pas les droits d’exécution.

## Question 3

- Cannot open file: Permission denied  
EUID: 1001
EGID: 1001
RUID: 1001
RGID: 1001
Le processus n’arrive pas à ouvrir le fichier en lecture.

- Après avoir activé le flag set-user-id :  
EUID: 1000
EGID: 1001
RUID: 1001
RGID: 1001

Le processus a réussi à lire le fichier. 
car EUID égale au uid du proprio du fichier

## Question 4

### Quelles sont les valeurs des différents ids ?

EUID 1001
EGID 1001
RUID 1001
RGID 1001

Car les accès du fichier sont liés à l'interpréteur python. En effet, ce sont ces accès qui sont pris en compte et non directement les “vrais” accès du fichier. C’est pour cela que ce sont les RUIDs qui seront utilisés et affichés et non le EUID set par le flag si celui-ci est défini.

### Comment un utilisateur peut changer un de ses attributs sans demander à l’administrateur ?
- En utilisant la commande passwd, en pratique, il se voit affecté temporairement (par le biais de Setuid des valeurs 0 en EUID (valeur correspondant au root). Il peut donc changer son mot de passe.
- Ou encore on pourrait changer les permissions en ajoutant l’écriture pour tous les utilisateurs avec la commande : sudo chmod 646 /etc/passwd.
Tous les utilisateurs pourront changer le contenu du fichier.  
rw-r--rw- 1 root root 3082 janv. 13 17:59 /etc/passwd


## Question 5

Le fichier /etc/passwd est un fichier texte, chaque enregistrement décrivant un compte d'utilisateur.

### À quoi sert la commande chfn ? Donnez les résultats de ls -al /usr/bin/chfn, et expliquez les permissions.

- La commande chfn sert à modifier le nom complet et les informations associées à un utilisateur
- résultat de ls -al /usr/bin/chfn : 
      -rwsr-xr-x 1 root root 85064 mai   28  2020 /usr/bin/chfn

Ce fichier appartient à l’utilisateur root et au groupe root, il est accessible en écriture/lecture  et est executable pour son propriétaire et le set-user-id est défini.
Il est seulement accessible en lecture et executable pour les membres du groupe root et la même chose pour tous les autres utilisateurs



### Lancez la commande chfn en tant que utilisateur toto, répondez aux questions. Visualisez à nouveau le contenu du fichier /etc/passwd et vérifiez que les informations ont bien été mises à jour correctement.

Avant de lancer chfn :   
      ```  toto:x:1001:1001:,,,:/home/toto:/bin/bash``` 

Après :   
``` toto:x:1001:1001:,14,0678943,4795151615:/home/toto:/bin/bash```    
Des informations ont bien été ajoutées dans le fichier /etc/passwd après l'exécution de la commande chfn avec l’user toto.

## Question 6

Les mots de passe sont stockés dans le fichier ‘/etc/shadow’ et ne peuvent être lu que par le root. Cela est fait pour pour limiter encore plus l'accès à la version chiffrée des mots de passe.

## Question 7

drwxrws--t  3 admin  groupe_a 4096 janv. 20 17:23  dir_a  
drwxrws--t  2 admin  groupe_b 4096 janv. 20 16:47  dir_b  
drwxr-xr-x  2 admin  groupe_c 4096 janv. 20 16:29  dir_c

Mettre les scripts bash dans le repertoire *question7*.

Voir aussi dans le répertoire *question7* les commandes utilisées pour créer les groupes/users et changer les droits

## Question 8
- home/admin/passwd : -rw------- 1 admin admin   40 janv. 21 19:51 passwd, il est de la forme :  
username1  
mdp2  
username2  
mdp2

- il faut que le owner de l'executable soit l’utilisateur admin et que le flag setuid soit défini. Notre executable rmg doit avoir ces droits ;
-rwsrwxr-x  1 admin  groupe_c 17680 janv. 23 17:45 rmg

Le programme et les scripts dans le répertoire *question8*.


## Question 9

- Notre executable pwd doit appartenir à admin et au groupe_c et il faut également que le flag setuid soit défini.
on retrouve donc : -rwsrwxr-x  1 admin  groupe_c 17424 janv. 22 18:27 pwd


- Il faut changer rmg.c dans la question en ajoutant la librairie <crypt.h> et <termios.h>. Il faut également remplacer le scanf précédemment utilisé pour avoir le mdp par cette ligne :
char *mdp = crypt(getpass("tape ton mot de passe contenue in /home/admin/passwd: :"), SALT);*  
(Seul changement, voir ligne 66 du fichier rmg.c dans le dossier *question9*, SALT doit avoir la même valeur que pour pwd.c).


- Pour compiler avec la librarie crypt.h, il faut ajouter l’option -lcrypt : gcc -o pwd pwd.c -lcrypt et  gcc -o rmg rmg.c -lcrypt

Le programme et les scripts se trouve dans le repertoire *question9*.

## Question 10

Le owner de l’executable serveur doit être root et le setuid défini.


Les programmes *groupe_server* et *groupe_client* dans le repertoire
*question10* ainsi que les tests.
