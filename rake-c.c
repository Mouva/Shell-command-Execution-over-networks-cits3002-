//22973676, Adrian Bedford
//22989775, Oliver Lynch

//NEED TO ADD ABILITY IF COMMANDLINE ISNT PASSED FILEPATH TO CLOSE, OR ROUTE TO RAKEFILE IN CURRENT DIR

#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include "strsplit.c"

int main(int argc, char *argv[])
{
    int count = 0;
    char line[256];
    FILE *rakefile;
    rakefile = fopen(argv[1], "r");

    if (rakefile == NULL)
    {
        printf("Cannot open file \n");
        return 1;
    }

    while (fgets(line, sizeof(line), rakefile)) {
        for (int i = 0; line[i] != '\0'; i++){
            if (line[i] == ' ' && line[i+1] != ' ') {
                count++;
            }
        }
    }

    printf("%s",strsplit(line, count));

    printf("%d", count);

    fclose(rakefile);
    return 0;
}