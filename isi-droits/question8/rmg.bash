#!/bin/bash
#Ce bash doit être exécuté dans le dossier qui contient dir_b, dir_a, dir_c et nos fichier rmg.c, check_pass.c et check_pass.h
#Notre exécutable est appelé ./rmg, admin doit être le owner et le flag setuid défini

su admin -c "touch dir_a/fileAdminDirA.txt; touch dir_c/fileAdminDirC.txt; touch dir_b/fileAdminDirB.txt; gcc -o rmg rmg.c;chgrp groupe_c rmg;chmod u+s rmg;"
su - lambda_a -c "rm dir_a/fileAdminDirA.txt; ./rmg dir_a/fileAdminDirA.txt;"
su - lambda_b -c "rm dir_b/fileAdminDirB.txt; ./rmg dir_b/fileAdminDirB.txt;"