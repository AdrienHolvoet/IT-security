#!/bin/bash
#Ce bash doit être exécuté dans le dossier qui contient dir_b, dir_a, dir_c et nos fichier rmg.c, pwd.c,  check_pass.c et check_pass.h
#Notre exécutable est appelé et ./pwd , L'admin doit être le owner, groupe_c le groupe et le flag setuid défini

su admin -c "touch dir_a/fileAdminDirA.txt; touch dir_b/fileAdminDirB.txt; gcc -o rmg rmg.c -lcrypt; chgrp groupe_c rmg;chmod u+s rmg; gcc -o pwd pwd.c -lcrypt; chown admin pwd; chgrp groupe_c pwd; chmod u+s pwd;"
su - lambda_a -c "./pwd;rm dir_a/fileAdminDirA.txt; ./rmg dir_a/fileAdminDirA.txt;"
su - lambda_b -c "./pwd;rm dir_b/fileAdminDirB.txt; ./rmg dir_b/fileAdminDirB.txt;"
