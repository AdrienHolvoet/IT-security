#!/bin/bash
#On se trouve dans le dossier qui contient dir_b, dir_a, dir_c

su admin -c "touch dir_a/fileAdmin.txt; touch dir_c/fileAdmin.txt;"
su - lambda_b -c "touch dir_b/fileb.txt;"
su - lambda_a -c "touch dir_a/file1.txt; touch dir_b/file2.txt; touch dir_c/file3.txt; mv dir_a/fileAdmin.txt dir_a/fileA.txt;cat dir_a/fileAdmin.txt;cat  dir_b/fileb.txt; cat  dir_c/fileAdmin.txt;"











