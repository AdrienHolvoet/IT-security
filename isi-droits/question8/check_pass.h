#define PATH_PASSWD "/home/admin/passwd"
#define MAX_LENGTH 20
#define ADMINID 1002

#include <stdlib.h>
#include <unistd.h>
#include <grp.h>
#include <pwd.h>
#include <sys/stat.h>
#include <stdio.h>
#include <string.h>


int check_pass(char *mdp, char *username);
