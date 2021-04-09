#!/bin/bash
#On se trouve dans le dossier qui contient dir_b, dir_a, dir_c

su admin -c "touch dir_b/fileAdmin.txt; touch dir_c/fileAdmin.txt;"
su - lambda_a -c "touch dir_a/filea.txt;"
su - lambda_b -c "touch dir_b/file1.txt; touch dir_b/lala.txt; touch dir_a/file2.txt; touch dir_c/file3.txt; mv dir_b/fileAdmin.txt dir_b/fileB.txt;cat dir_b/fileAdmin.txt;cat  dir_a/filea.txt; nano dir_c/fileAdmin.txt;"











