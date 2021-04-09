#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include "check_pass.c"

#define MAX 80
#define PORT 4000
#define SA struct sockaddr 

int new_client(int client_fd)
{
	char buff[MAX]; 
	char delim[] = " ";
    int n;
	int res; 

	read(client_fd, buff, sizeof(buff));
	
	char *ptr = strtok(buff, delim);
	char *user = ptr;
	char *pass = strtok(NULL, delim);

	res = check_pass(pass, user);
	if (res == -1)
	{
		write(client_fd, "Wrong credentials\n", sizeof("Wrong credentials\n"));
		return EXIT_FAILURE;
	}

	pid_t pid = fork();
	if (pid == -1)
	{
		perror("fork");
		return EXIT_FAILURE;
	} 
	else if (pid == 0)
	{
		write(client_fd, "Authentification OK\n", sizeof("Authentification OK\n"));

		for (;;)
		{
			bzero(buff, MAX);
			read(client_fd, buff, sizeof(buff));
			if (strcmp(buff, "close\n") == 0)
			{
				write(client_fd, "Connection closed\n", sizeof("Connection closed\n"));
				close(client_fd);
				break;
			}
			else
			{
				char *ptr = strtok(buff, delim);
				char *command = ptr;
				char *data = strtok(NULL, delim);

				if (strcmp(command, "list") == 0)
				{
					char *buffer;
					FILE *fh = popen("/bin/ls", "r");
					if ( fh != NULL )
					{
						fseek(fh, 0L, SEEK_END);
						long s = ftell(fh);
						rewind(fh);
						buffer = malloc(s);
						if ( buffer != NULL )
						{
						fread(buffer, s, 1, fh);
						fclose(fh); fh = NULL;
					
						write(client_fd, buffer, sizeof(buffer));
					
						free(buffer);
						}
						if (fh != NULL) fclose(fh);
					}
					else
					{
						write(client_fd, "Wrong path", sizeof("Wrong path"));
					}
				}
				else if (strcmp(command, "read") == 0)
				{
					char *buffer;
					FILE *fh = popen("/bin/cat", "r");
					if ( fh != NULL )
					{
						fseek(fh, 0L, SEEK_END);
						long s = ftell(fh);
						rewind(fh);
						buffer = malloc(s);
						if ( buffer != NULL )
						{
						fread(buffer, s, 1, fh);
						fclose(fh); fh = NULL;
						
						write(client_fd, buffer, sizeof(buffer));
						
						free(buffer);
						}
						if (fh != NULL) fclose(fh);
					}
					else
					{
						write(client_fd, "Wrong path", sizeof("Wrong path"));
					}
				}
				else 
				{
					write(client_fd, "Wrong command\n", sizeof("Wrong command\n"));
				}
			}	
		}
	}
	return 0;
};

int close(int conn_fd)
{
	int err = close(conn_fd);
	if (err == -1)
	{
		perror("close");
		printf("failed to close connection\n");
		return err;
	}

	return err;
}

int main()
{
	int sockfd, connfd, len; 
    struct sockaddr_in servaddr, cli; 
  
    sockfd = socket(AF_INET, SOCK_STREAM, 0); 
    if (sockfd == -1) { 
        printf("socket creation failed...\n"); 
        exit(0); 
    } 
    else
        printf("Socket successfully created..\n"); 
    bzero(&servaddr, sizeof(servaddr)); 
  
    servaddr.sin_family = AF_INET; 
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY); 
    servaddr.sin_port = htons(PORT); 
  
    if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) { 
        printf("socket bind failed...\n"); 
        exit(0); 
    } 
    else
        printf("Socket successfully binded..\n"); 
  
    if ((listen(sockfd, 5)) != 0) { 
        printf("Listen failed...\n"); 
        exit(0); 
    } 
    else
        printf("Server listening..\n"); 
    len = sizeof(cli); 
  
	for (;;){
		connfd = accept(sockfd, (SA*)&cli, &len); 
		if (connfd < 0) { 
			printf("server accept failed...\n"); 
			exit(0); 
		} 
		else
			printf("server accept the client...\n"); 
	
		new_client(connfd);
	}
    
    close(sockfd); 
}
