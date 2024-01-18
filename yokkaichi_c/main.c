#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "yokkaichi_constants.h"
#include "yokkaichi_structs.h"
#include "checker.h"

int main() {
    int ports[] = {25565, 25566};
    char ipLine[MAX_IP_LINE_LEN];
    MinecraftServer srv;
    FILE *ipList;

    printf("Loading IP List\n");

    ipList = fopen("data/ips.txt", "r");
    if (ipList == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    while(fgets(ipLine, MAX_IP_LINE_LEN, ipList)) { // Get one line from IP List file
        ipLine[strcspn(ipLine, "\n")] = 0; // Remove the newline
        for (int i = 0; i < sizeof(ports) / sizeof(int); i++) {
            strncpy(srv.ip, ipLine, IP_LENGHT);
            srv.port = ports[i];
            checkServer(srv);
        }
    }
    
    fclose(ipList);
    return 0;
}
