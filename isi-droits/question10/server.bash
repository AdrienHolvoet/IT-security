#!/bin/bash

#Notre exécutable est appelé et ./server , L'admin doit être le owner, groupe_c le groupe et le flag setuid défini

gcc -o server server.c -lcrypt
sudo chown admin server
sudo chmod u+s server
gcc -o client client.c
