#!/bin/bash

su admin -c "cat dir_b/fileb.txt; cat dir_a/filea.txt; cat dir_a/fileAdmin.txt; rm dir_a/filea.txt; mv dir_b/lala.txt dir_b/modifiedByAdmin.txt; touch dir_a/newAdminFile.txt; touch dir_b/newAdminFile.txt; touch dir_c/newAdminFile.txt; "









