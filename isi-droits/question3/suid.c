#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

char* ReadFile(char *filename)
{
   char *buffer = NULL;
   int string_size, read_size;
   FILE *handler = fopen(filename, "r");

   if (handler)
   {
       fseek(handler, 0, SEEK_END);
       string_size = ftell(handler);
       rewind(handler);
       buffer = (char*) malloc(sizeof(char) * (string_size + 1) );
       read_size = fread(buffer, sizeof(char), string_size, handler);
       buffer[string_size] = '\0';

       if (string_size != read_size)
       {
           free(buffer);
           buffer = NULL;
       }
       fclose(handler);
    }
    else 
    {
        perror("Cannot open file");
    }
    return buffer;
}

int main(int argc, char *argv[])
{  
    char *string = ReadFile("mydir/data.txt");
    if (string)
    {
        printf("File opens correctly : \n");
        puts(string);
        free(string);
    }
    
    printf("EUID: %d\n", geteuid());
    printf("EGID: %d\n", getegid());
    printf("RUID: %d\n", getuid());
    printf("RGID: %d\n", getgid());
    
    return 0;
}
