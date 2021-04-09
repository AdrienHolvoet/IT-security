#include <netdb.h> 
#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#include <sys/socket.h> 
#define MAX 80 
#define PORT 4000
#define SA struct sockaddr 

void func(int sockfd, char *file) 
{ 
	FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read_;
    char buff[MAX];

    fp = fopen(file, "r");
    if (fp == NULL) {
        printf("Incorrect file path\n");
        exit(EXIT_FAILURE);
    } 
    
    read_ = getline(&line, &len, fp);
    write(sockfd, line, MAX);
    read(sockfd, buff, sizeof(buff));
    printf("From server: %s", buff);
     
    if (strcmp("Wrong credentials", buff) != 0) {
        bzero(line, 2*sizeof(line));

         while ((read_ = getline(&line, &len, fp)) != -1) {
            bzero(buff, sizeof(buff));
            printf("Command: %s\n", line);
            write(sockfd, line, 2*sizeof(line));
            read(sockfd, buff, sizeof(buff));
            printf("From server: %s\n", buff);
            bzero(line, 2*sizeof(line));
        }
     }
    fclose(fp);
    if (line)
        free(line);

    printf("Client Exit...\n");
} 

int main(int argc, char *argv[]) 
{ 
	int sockfd, connfd; 
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
	servaddr.sin_addr.s_addr = inet_addr("127.0.0.1"); 
	servaddr.sin_port = htons(PORT); 

	if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0) { 
		printf("connection with the server failed...\n"); 
		exit(0); 
	} 
	else
		printf("connected to the server..\n"); 

	func(sockfd, argv[1]); 

	close(sockfd); 
} 
