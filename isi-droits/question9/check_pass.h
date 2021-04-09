#define PATH_PASSWD "/home/admin/passwd"
#define MAX_LENGTH 20
#define ADMINID 1002
#define SALT "50"
#define TEMPO_FILE "replace.txt"

#include <stdlib.h>
#include <unistd.h>
#include <grp.h>
#include <pwd.h>
#include <sys/stat.h>
#include <stdio.h>
#include <string.h>
#include <crypt.h>
#include <termios.h>


int check_pass(char *mdp, char *username);
