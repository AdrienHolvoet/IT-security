# Binome

Nom, Prénom, email: KROL Mikolaï mikolai.krol.etu@univ-lille.fr  
Nom, Prénom, email: HOLVOET Adrien adrien.holvoet.etu@univ-lile.fr

# Introduction

Pour plus de facilité pour la réalisation de cet exercice, nous avons supposé que les clés usb de chaque représentant correspondent à un dossier (_usb1/usb2/usb3/usb4_) avec toujours le même nom et que leur contenu serait toujours appelé _key.enc_. Nous retrouverons également un dossier _ramdisk_ qui contiendra notre clé en claire et que celui-ci a la même caractéristique que la ram volatile c'est à dire que son contenu s'effacera lors de la mise en off du serveur. Enfin un dossier _plugged_ qui simulera les clés usb branchées sur le serveur. Pour lancer le serveur il faut au moins que deux clés usb se trouvent dans le dossier plugged. Toutes nos paires nom/carte bancaire se trouvent dans le fichier card qui est crypté.

# Comment l'utiliser?

Tous les dossiers contiennent déjà des fichiers car il faut que le dossier soit non vide pour être uploadé sur git. Pour tout remettre à zéro et lancer un serveur neuf, il suffit de lancer `python3 serveur.py` et d'appuyez sur la touche _B_ comme demandé lors de l'apparition du premier menu, puis il suffit de suivre les instructions et ainsi regénérer une nouvelle clé de cryptage/décryptage et redéfinir les différents acteurs/clés usb. Enfin vous pouvez lancer le service afin d'enregistrer des paires de carte/nom cryptées.

# Partie 1 : Responsabilité partagée

## Question 1

Nous sommes partis sur ce principe pour être sur d'avoir besoin des deux responsables pour récuperer notre clé de chiffrement/déchiffrement:

1. On génère la clé en claire de taille 32
2. On génère un mask aléatoire de taille 28, on aura "MASK" + String aléatoire de taille 28 (=32)
3. On stocke la version cryptée du mask dans usb1
4. On stocke la version cryptée de mask xor la clé en claire dans usb2  
   Et pour récupérer notre clé en clair on doit alors :
5. Décrypter usb1 et usb2
6. usb1 XOR usb2

exemple :  
clé aléatoire en claire : rjtdoyvdeqrdmsbzxyjnwltjnsfhpfbp  
mask aléatoire : MASKabhdztgettdcooceqqqbjoohfnmf  
usb1 : crypt(mask)  
usb2 : crypt(mask xor clé)  
clé = decrypt(usb1) xor decrypt(usb2) = rjtdoyvdeqrdmsbzxyjnwltjnsfhpfbp

L'ajout du String MASK permettra de faire la différence entre les deux types de clés usb, par exemple le reponsable technique aura la clé avec le mask crypté et le responsable judicaire l'autre.

Notre clé utilisée pour chiffrer et déchiffrer sera en clair dans notre dossier ramdisk une fois que les deux clés usbs seront connectées et la clé recomposée/déchiffrée. Ce dossier ramdisk correpond/simule une mémoire ram qui disparaitra si on débranche le serveur(si on essaie de le voler) ce qui rendra impossible le vol notre clé.

## Question 2

Voir code

# Partie 2 : Délégation de droit

## Question 3

Pour chaque représentant on va prendre la clé de son responsable à laquelle on va rajouter "REPR" au début avant de la crypter et la stocker sur sa clé usb. Quand quelqu'un va brancher sa clé usb, on la décodera et on verra si sa partie de la clé décodée est plus grande que 32(= taille de la clé en claire et du mask) et que ses premiers caractères sont "REPR", si oui c'est un représentant, il suffira donc d'enlever cette partie pour l'assembler à l'autre partie de la clé. Ce système nous permet de faire la différence entre un responsable et un représentant.
Nous avons également ajouté le moyen de faire la différence entre un responsable judiciaire et l'autre technique. Le responsable technique possèdera la clé avec le mask crypté et la personne judiciaire possedera la clé avec le mask XOR la clé en claire cryptée.

## Question 4

Voir code

# Partie 3 : Révocation de droit

## Question 5

Nous somme partis du principe que si le représentant/reponsable est répudié, il est fort probable qu'il conserve sa clé usb avec sa clé encryptée et donc nous n'aurions pas accès à celle-ci, ça rendrait la suppression de sa clé encryptée assez difficile voir impossible. C'est pourquoi nous avons décidé que lors d'une révocation de droit, il est bien plus sécuritaire de changer la valeur de la clé en claire servant à chiffrer/déchiffrer nos paires nom/carte. En effet, pour se faire nous avons besoin de la présence de tous les responsables excepté celui qui est répudié, une fois que ceux-ci sont authentifiés, nous décryptons notre fichier de carte avec l'ancienne clé en claire, sauvegardons le contenue et créons ainsi une nouvelle clé de cryptage/décryptage, mettons à jour les clés usbs des responsables authentifiés et recryptons le contenu de notre fichier de paire carte/nom.  
Cette solution peut-être très longue et fastidieuse en fonction de la taille du fichier de paire de carte/nom et de la fonction de cryptage utilisée. Cependant, celle-ci est la plus sécurisés.

## Question 6

Voir code
