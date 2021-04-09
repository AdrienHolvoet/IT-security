#include "check_pass.h"

int check_pass(char *mdpnc, char *username)
{

    FILE *inputFile = fopen(PATH_PASSWD, "r");
    if (inputFile == NULL)
    {
        printf("Cannot open file %s\n", PATH_PASSWD);
        exit(-1);
    }
    char *mdp = crypt(mdpnc, SALT);
    char *buffer = (char *)malloc(MAX_LENGTH);
    while (fgets(buffer, MAX_LENGTH, inputFile))
    {

        //remove the \n after the fgets
        buffer[strcspn(buffer, "\n")] = 0;
        if (strcmp(username, buffer) == 0)
        {
            fgets(buffer, MAX_LENGTH, inputFile);
            buffer[strcspn(buffer, "\n")] = 0;
            if (strcmp(mdp, buffer) == 0)
            {
                fclose(inputFile);
                free(buffer);
                return 0;
            }
        }
    }
    fclose(inputFile);
    free(buffer);
    return -1;
}