#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include "yokkaichi_constants.h"
#include "yokkaichi_structs.h"
#include "checker.h"

int main() {
    int ports[] = {25565, 25566};
    char ipLine[MAX_IP_LINE_LEN];

    /* Example values */
    MinecraftServer srv;
    strcpy(srv.ip, "127.0.0.1");
    srv.port = 25565;
    ThreadArgs tA;
    tA.threadId = 0;
    tA.server = &srv;

    // pthread_t *threads = malloc(THREAD_COUNT * sizeof(pthread_t));
    // ThreadArgs *threadArgs = malloc(THREAD_COUNT * sizeof(ThreadArgs));
    // MinecraftServer *serversPending = calloc(THREAD_COUNT, sizeof(MinecraftServer));
    // MinecraftServer srv;
    
    FILE *ipList;

    printf("Loading IP List\n");

    ipList = fopen("data/ips.txt", "r");
    if (ipList == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    pthread_t thread;
    pthread_create(&thread, NULL, checkerThread, &tA);
    pthread_join(thread, NULL);

    /*  TODO: Add spawning threads logic here:
        - create heap array for multiple threads
        - create heap array for server pointers
        - give every thread its own server pointer
        - when getting a new server, iterate over the entire server array
        - if any of them is NULL, set the pointer value to the server
        - if all of them aren't NULL, then iterate until something is NULL
    */
    
    fclose(ipList);
    return 0;
}
