#!/user/bin/env python3 -tt

# Imports
import sys
import os
import random
import string
from simplecrypt import DecryptionException, encrypt, decrypt
from getpass import getpass
import getpass


class Server:
    card = "card"
    responsive_length = 32
    usb1_path = "usb1/key.enc"
    usb2_path = "usb2/key.enc"
    usb3_path = "usb3/key.enc"
    usb4_path = "usb4/key.enc"
    clear_key_path = "ramdisk/key.clear"
    is_commissioning = False
    plugged_path = "plugged/"

    is_technical_officer = -1
    is_judicial_officer = -1
    mask_key = "MASK"
    representative_key = "REPR"

    '''Pour le premier démarrage du serveur'''

    def init(self, content):

        subdirs = []
        files = []
        for root, subdir, file in os.walk(Server.plugged_path):
            subdirs += subdir
            files += file
        if len(subdirs) < 4 and len(files) < 4:
            raise Exception(
                "Vous devez ou moins avoir quatres clefs usb connectés pour un reset ou un premier démarrage du serveur")
        # remove all the config files
        if os.path.exists(Server.clear_key_path):
            os.remove(Server.clear_key_path)
        if os.path.exists(Server.plugged_path + Server.usb1_path):
            os.remove(Server.plugged_path + Server.usb1_path)
        if os.path.exists(Server.plugged_path + Server.usb2_path):
            os.remove(Server.plugged_path + Server.usb2_path)
        if os.path.exists(Server.plugged_path + Server.usb3_path):
            os.remove(Server.plugged_path + Server.usb3_path)
        if os.path.exists(Server.plugged_path + Server.usb4_path):
            os.remove(Server.plugged_path + Server.usb4_path)
        if os.path.exists(Server.card):
            os.remove(Server.card)

        # On génère la clear key
        clear_key = ''.join(random.choice(string.ascii_lowercase)
                            for i in range(Server.responsive_length))
        # On génère un mask aléatoire
        mask = Server.mask_key
        mask += ''.join(random.choice(string.ascii_lowercase)
                        for i in range(28))

        # On stocke la version cryptée du mask dans usb1
        self.write_usb1(mask)
        # On stocke la verion cryptée de mask xor clear key dans usb2
        self.write_usb2(clear_key, mask)

        # On stocke la version cryptée du mask dans usb3 avec la representative_key pour les dintinguer
        mask = Server.representative_key + mask
        self.write_usb3(mask)
        # On stocke la verion cryptée de mask xor clear key dans usb4 avec la representative_key pour les dintinguer
        clear_key_rep = Server.representative_key + clear_key
        self.write_usb4(clear_key_rep, mask)

        if(content == None):
            print("Le serveur a bien été configuré")
        else:
            print("Réécriture du fichier avec la nouvelle clef de cryptage...")

            with open(self.card, "ab") as f:
                for i in range(len(content)):
                    ciphertext = encrypt(clear_key, content[i])
                    f.write(ciphertext + '///---'.encode('utf-8'))
            print(
                "Procédure de révocation de droit terminée, la personne révoquée n'aura plus accès au système.")

    '''Mise en route du serveur'''

    def commissioning(self):
        # mise en service qui lira les contenus de 2 clefs usb pour recomposer la clef et l'écrira dans notre ram temporaire (ramdisk)
        subdirs = []
        files = []
        for root, subdir, file in os.walk(Server.plugged_path):
            subdirs += subdir
            files += file

        if len(subdirs) < 2 and len(files) < 2:
            raise Exception(
                "Vous devez ou moins avoir deux clefs usb connectés")
        print("Mise en service du serveur...")

        try:
            os.remove(Server.clear_key_path)
        except FileNotFoundError:
            pass

        try:
            with open(Server.plugged_path + subdirs[0] + "/" + files[0], "rb") as f:
                ciphertext = f.read()
            key1 = decrypt(getpass.getpass(
                prompt='Veuillez taper le mot de passe pour déverrouiller %s : ' % subdirs[0]), ciphertext).decode("utf-8")

            key1 = self.check_user_type(key1)

            with open(Server.plugged_path + subdirs[1] + "/" + files[1], "rb") as f:
                ciphertext = f.read()
            key2 = decrypt(getpass.getpass(
                prompt='Veuillez taper le mot de passe pour déverrouiller %s : ' % subdirs[1]), ciphertext).decode("utf-8")

            key2 = self.check_user_type(key2)

            if Server.is_judicial_officer == -1 or Server.is_technical_officer == -1:
                raise Exception("la Combinaison de la clef n'est pas bonne")

            with open(Server.clear_key_path, "w") as f:
                f.write(self.sxor(key1, key2))

            Server.is_commissioning = True

        except DecryptionException:
            raise DecryptionException("Mauvais mot de passe")

    def check_user_type(self, key):
        print("\n")
        length_key = len(key)
        if length_key > Server.responsive_length:
            key = key[len(Server.representative_key):length_key+1]
            if key[0:len(Server.mask_key)] == Server.mask_key:
                Server.is_technical_officer += 1
                print("Authentifié avec le REPRESENTANT technique")
            else:
                Server.is_judicial_officer += 1
                print("Authentifié avec le REPRESENTANT judiciare")
        else:
            if key[0:len(Server.mask_key)] == Server.mask_key:
                Server.is_technical_officer += 2
                print("Authentifié avec le RESPONSABLE technique")
            else:
                Server.is_judicial_officer += 2
                print("Authentifié avec le RESPONSABLE judiciare")
        print("\n")
        return key

    '''Suppression des droits de la 4ième personne'''

    def rights_revocation(self):
        subdirs = []
        files = []
        for root, subdir, file in os.walk(Server.plugged_path):
            subdirs += subdir
            files += file

        if len(subdirs) < 3 and len(files) < 3:
            raise Exception(
                "Vous devez ou moins avoir 3 clefs usb connectées")
        try:
            with open(Server.plugged_path + subdirs[0] + "/" + files[0], "rb") as f:
                ciphertext = f.read()
            key1 = decrypt(getpass.getpass(
                prompt='Veuillez taper le mot de passe pour déverrouiller %s : ' % subdirs[0]), ciphertext).decode("utf-8")

            key1 = self.check_user_type(key1)

            with open(Server.plugged_path + subdirs[1] + "/" + files[1], "rb") as f:
                ciphertext = f.read()
            key2 = decrypt(getpass.getpass(
                prompt='Veuillez taper le mot de passe pour déverrouiller %s : ' % subdirs[1]), ciphertext).decode("utf-8")

            key2 = self.check_user_type(key2)
            secondKey = None
            # condition pour récupérer la bonne deuxième clef
            if Server.is_judicial_officer > -1 and Server.is_judicial_officer < 2 and Server.is_technical_officer > -1 and Server.is_judicial_officer < 2:
                secondKey = key2

            with open(Server.plugged_path + subdirs[2] + "/" + files[2], "rb") as f:
                ciphertext = f.read()
            key3 = decrypt(getpass.getpass(
                prompt='Veuillez taper le mot de passe pour déverrouiller %s : ' % subdirs[2]), ciphertext).decode("utf-8")

            key3 = self.check_user_type(key3)
            # condition pour récupérer la bonne deuxième clef
            if Server.is_judicial_officer > -1 and Server.is_judicial_officer < 2 and Server.is_technical_officer > -1 and Server.is_judicial_officer < 2:
                secondKey = key3

            if Server.is_judicial_officer == -1 or Server.is_technical_officer == -1:
                raise Exception("la combinaison de la clef n'est pas bonne")

            clear_key = self.sxor(key1, secondKey)
            with open(Server.clear_key_path, "w") as f:
                f.write(clear_key)

            # Pour voir nous à qui nous essayons de révoquer les droits

            repudiated_person = None

            if Server.is_judicial_officer == 1:
                repudiated_person = "REPRESENTANT JUDICIAIRE"
            elif Server.is_judicial_officer == 0:
                repudiated_person = "RESPONSABLE JUDICIAIRE"
            elif Server.is_technical_officer == 1:
                repudiated_person = "REPRESENTANT TECHNIQUE"
            elif Server.is_technical_officer == 0:
                repudiated_person = "RESPONSABLE TECHNIQUE"

            print(
                "Commencement de la procédure de révocation de droit du " + repudiated_person + "...")

            clear_line = []
            with open(self.card, "rb") as f:
                lines = f.read().split('///---'.encode('utf-8'))

                for i in range(len(lines) - 1):
                    clear_line.append(decrypt(clear_key,
                                              lines[i]).decode("utf-8"))
            clear_key = None

            print(
                "Récupération du contenu des paires carte/nom avec l'ancienne clef de cryptage/decryptage : DONE")

            subdirs = []

            while(len(subdirs) < 4):
                for root, subdir, file in os.walk(Server.plugged_path):
                    subdirs += subdir
                print("Veuillez vérifier que quatres clefs usb sont branchées pour définir la nouvelle clef de cryptage et les 4 responsables/représentants")
                input(
                    "Appuyez sur une touche une fois que les quatres clefs usb sont branchées...")

            self.init(clear_line)

        except DecryptionException:
            raise DecryptionException("Mauvais mot de passe")

    '''Clef du responsable technique'''

    def write_usb1(self, mask):
        ciphertext = encrypt(getpass.getpass(
            prompt='Configurez le mot de passe de usb1 (responsable technique) : '), mask)
        with open(Server.plugged_path + Server.usb1_path, "wb") as f:
            f.write(ciphertext)

    '''Clef du responsable juridique'''

    def write_usb2(self, clear_key, mask):
        ciphertext = encrypt(getpass.getpass(
            prompt='Configurez le mot de passe de usb2 (responsable juridique) : '), self.sxor(clear_key, mask))
        with open(Server.plugged_path + Server.usb2_path, "wb") as f:
            f.write(ciphertext)

    '''Clef du représentant technique'''

    def write_usb3(self, mask):
        ciphertext = encrypt(getpass.getpass(
            prompt='Configurez le mot de passe de usb3 (représentant technique) : '), mask)
        with open(Server.plugged_path + Server.usb3_path, "wb") as f:
            f.write(ciphertext)

    '''Clef du représentant juridique'''

    def write_usb4(self, clear_key, mask):
        ciphertext = encrypt(getpass.getpass(
            prompt='Configurez le mot de passe de usb4 (représentant juridique) : '), self.sxor(clear_key, mask))
        with open(Server.plugged_path + Server.usb4_path, "wb") as f:
            f.write(ciphertext)

    def sxor(self, s1, s2):
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

    def byte_xor(self, ba1, ba2):
        return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

    def get_clear_key(self):
        with open(Server.clear_key_path, "r") as f:
            clear_key = f.read()
        return clear_key

    def write_pair(self, name, card):
        ciphertext = encrypt(self.get_clear_key(), name + ";" + card)
        with open(self.card, "ab") as f:
            f.write(ciphertext + '///---'.encode('utf-8'))

    def remove_pair(self, name):
        delete = 0
        with open(self.card, "rb") as f:
            lines = f.read().split('///---'.encode('utf-8'))
        for i in range(len(lines) - 1):
            clear_line = decrypt(self.get_clear_key(),
                                 lines[i]).decode("utf-8")
            strInFile = clear_line.split(";")
            # For each line, check if line contains the string
            if name == strInFile[0]:
                lines.pop(i)
                with open(self.card, "wb") as f:
                    for j in range(len(lines) - 1):
                        f.write(lines[j] + '///---'.encode('utf-8'))
                return "      Votre numéro a été supprimé"
        return "        Nous n'existez pas dans le sytème"

    def search_pair_by_name(self, name):
        with open(self.card, "rb") as f:
            lines = f.read().split('///---'.encode('utf-8'))
            for i in range(len(lines) - 1):
                clear_line = decrypt(self.get_clear_key(),
                                     lines[i]).decode("utf-8")
                strInFile = clear_line.split(";")
                # For each line, check if line contains the string
                if name == strInFile[0]:
                    return "       Votre numéro de carte : " + strInFile[1].rstrip()
        return "       Vous n'existez pas dans le sytème"


def main():
    server = Server()

    try:
        os.remove("plugged/empty")
    except FileNotFoundError:
        pass
    while(1):
        try:
            if Server.is_commissioning:
                print("1) Ajouter une paire")
                print("2) Supprimer une paire")
                print("3) Chercher les n° de cartes associés à un nom")
                print("4) Revenir au menu de configuration du serveur")
                print("5) Eteindre le serveur")

                action = input("Tapez le numéro de l'action désirée : ")
                if(action == "1"):
                    name = input("      Tapez votre nom : ")
                    card = input("      Tapez votre numéro de carte : ")
                    if(name != "" and card != ""):
                        server.write_pair(name, card)
                elif(action == "2"):
                    name = input(
                        "      Tapez votre nom afin de supprimer votre compte: ")
                    print(server.remove_pair(name))
                elif(action == "3"):
                    name = input(
                        "       Tapez votre nom afin de retrouver votre numéro de carte: ")
                    print(server.search_pair_by_name(name))

                elif(action == "4"):
                    Server.is_commissioning = False
                    try:
                        os.remove("plugged/empty")
                        print("     Suppression de la ram volatile \n")
                    except FileNotFoundError:
                        pass
                elif(action == "5"):
                    exit()
                else:
                    print("     Numéro incorrecte \n")
            else:
                print("A) Mettre en route le service")
                print("B) Reset le serveur")
                print("C) Révoquez les droits d'un utilisateurs")
                print("D) Eteindre le serveur")
                action = input("Tapez la lettre de l'action désirée : ")
                if(action == "A"):
                    server.commissioning()
                elif(action == "B"):
                    server.init(None)
                elif(action == "C"):
                    server.rights_revocation()
                elif(action == "D"):
                    exit()
                else:
                    print("     Action inconnue \n")
        except Exception as e:
            print("\nERROR : ", end='')
            print(e)
            print("\n")


# Main body
if __name__ == '__main__':
    main()
