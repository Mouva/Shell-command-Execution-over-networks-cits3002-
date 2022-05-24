//Adrian Bedford, 22973676
//Oliver Lynch, 22989775

#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(int argc, char *argv[])
{
    FILE *rakefile
    int sock;
    struct sockAddr servAddr;
    
    rfile = fopen(argv[1], "r")






    
    sock = socket(AF_INET, SOCK_STREAM, 0);
    
    if(sock < 0){
        printf("Unable to create socket\n");
        return -1;
    }
    
    printf("Socket created successfully\n");
    
    servAddr.sin_family = AF_INET;
    servAddr.sin_port = htons(6666);
    servAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    
    if(connect(sock, (struct sockAddr*)&servAddr, sizeof(servAddr)) < 0){
        printf("Unable to connect\n");
        return -1;
    }
    printf("Connected with server successfully\n");
    
    






    if(send(sock, client_message, strlen(client_message), 0) < 0){
        printf("Unable to send message\n");
        return -1;
    }
    
    // Receive the server's response:
    if(recv(sock, server_message, sizeof(server_message), 0) < 0){
        printf("Error while receiving server's msg\n");
        return -1;
    }
    
    printf("Server's response: %s\n",server_message);
    
    // Close the socket:
    close(sock);
    
    return 0;
}
