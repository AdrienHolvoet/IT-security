#include "check_pass.c"

int check_group(struct passwd *pw_user, char *file)
{
    struct stat info;
    stat(file, &info);

    struct group *file_gr = getgrgid(info.st_gid);

    if (file_gr == NULL)
    {
        return -1;
    }
    char *filegr = malloc(strlen(file_gr->gr_name) + 1);

    strcpy(filegr, file_gr->gr_name);

    int ngroups = 0;
    //this call is just to get the correct ngroups
    getgrouplist(pw_user->pw_name, pw_user->pw_gid, NULL, &ngroups);
    __gid_t groups[ngroups];

    //here we actually get the groups
    getgrouplist(pw_user->pw_name, pw_user->pw_gid, groups, &ngroups);

    for (int i = 0; i < ngroups; i++)
    {

        struct group *gr = getgrgid(groups[i]);
        if (strcmp(gr->gr_name, filegr) == 0)
        {
            free(filegr);
            return 0;
        }
    }
    free(filegr);
    return 1;
}

int main(int argc, char *argv[])
{
    register struct passwd *pw_user;
    register struct passwd *pw_file;

    if (argc != 2)
    {
        printf("Un seul argument est accepté. \n");
        return EXIT_FAILURE;
    }

    pw_user = getpwuid(getuid());

    char *file;
    file = argv[1];

    if (pw_user == NULL)
    {
        return EXIT_FAILURE;
    }

    int code = check_group(pw_user, file);

    if (code == 0)
    {
        char mdp[200];
        printf("Mot de passe contenue in /home/admin/passwd: ");
        scanf("%s", mdp);
        if (check_pass(mdp, pw_user->pw_name) == 0)
        {
            int del = remove(file);
            if (!del)
                printf("Le fichier a été supprimé. \n");
            else
                printf("Le fichier n'as pas été supprimé. \n");
        }
        else
        {
            printf("Mot de passe incorrect. Utilisez la commande pwd pour l'ajouter ou le changer \n");
        }

        return EXIT_SUCCESS;
    }
    else if (code == -1)
    {
        printf("Ce fichier %s n'existe pas \n", file);
        return EXIT_FAILURE;
    }
    else
    {
        printf("Vous n'appartenez pas au même groupe que ce fichier, vous ne pouvez donc pas le supprimer. \n");
        return EXIT_FAILURE;
    }
}
