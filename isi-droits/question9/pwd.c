#include "check_pass.c"

char *check_user_exist(char *username)
{
    FILE *inputFile = fopen(PATH_PASSWD, "a+");
    if (inputFile == NULL)
    {
        printf("Cannot open file %s\n", PATH_PASSWD);
        exit(-1);
    }

    char *buffer = (char *)malloc(MAX_LENGTH);
    while (fgets(buffer, MAX_LENGTH, inputFile))
    {

        //remove the \n after the fgets
        buffer[strcspn(buffer, "\n")] = 0;

        if (strcmp(username, buffer) == 0)
        {
            fgets(buffer, MAX_LENGTH, inputFile);
            buffer[strcspn(buffer, "\n")] = 0;

            fclose(inputFile);

            return buffer;
        }
    }
    fclose(inputFile);
    free(buffer);
    return NULL;
}

int main()
{

    register struct passwd *pw_user;
    pw_user = getpwuid(getuid());

    char *current_mdp = check_user_exist(pw_user->pw_name);
    printf("User : %s\n", pw_user->pw_name);
    FILE *inputFile;

    if (current_mdp == NULL)
    {
        inputFile = fopen(PATH_PASSWD, "a+");
        char mdp[150];
        fprintf(inputFile, "%s\n", pw_user->pw_name);
        fprintf(inputFile, "%s\n", crypt(getpass("tape ton nouveau mot de passe :"), SALT));

        fclose(inputFile);
        return 0;
    }
    else
    {
        char *oldpasswd = crypt(getpass("tape ton mot de passe actuel :"), SALT);
        if (strcmp(oldpasswd, current_mdp) == 0)
        {
            char *newmdp = crypt(getpass("tape ton nouveau mot de passe :"), SALT);
            if (newmdp == NULL)
            {
                printf("error, something went wrong \n");
                return -1;
            }
            char *buffer = (char *)malloc(MAX_LENGTH);
            FILE *fTemp = fopen(TEMPO_FILE, "w");
            inputFile = fopen(PATH_PASSWD, "r");
            if (inputFile == NULL || fTemp == NULL)
            {
                printf("cannot open file %s\n", TEMPO_FILE);
                exit(-1);
            }

            buffer = (char *)malloc(MAX_LENGTH);
            while (fgets(buffer, MAX_LENGTH, inputFile))
            {
                //remove the \n after the fgets
                buffer[strcspn(buffer, "\n")] = 0;
                if (strcmp(pw_user->pw_name, buffer) == 0)
                {
                    fgets(buffer, MAX_LENGTH, inputFile);
                }
                else
                {
                    fprintf(fTemp, "%s\n", buffer);
                }
            }
            fclose(inputFile);
            fclose(fTemp);
            free(buffer);

            fTemp = fopen(TEMPO_FILE, "r");
            inputFile = fopen(PATH_PASSWD, "w");

            while (fgets(buffer, MAX_LENGTH, fTemp))
            {
                //remove the \n after the fgets
                buffer[strcspn(buffer, "\n")] = 0;
                fprintf(inputFile, "%s\n", buffer);
            }

            fprintf(inputFile, "%s\n", pw_user->pw_name);
            fprintf(inputFile, "%s\n", newmdp);
            fclose(inputFile);
            fclose(fTemp);
            free(buffer);
            remove(TEMPO_FILE);
            return 0;
        }
        else
        {
            printf("error : mauvaise mot de passe \n");
            return -1;
        }
    }
}