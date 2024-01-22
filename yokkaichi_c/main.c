#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include "yokkaichi_constants.h"
#include "yokkaichi_structs.h"
#include "checker.h"

int main() {
    char ipLine[MAX_IP_LINE_LEN];
    Thread *threads = calloc(THREAD_COUNT, sizeof(Thread));
    FILE *ipList;

    printf("[THREAD-MAIN] Loading IP List\n");

    ipList = fopen("data/ips.txt", "r");
    if (ipList == NULL) {
        printf("[THREAD-MAIN] Error opening file\n");
        return 1;
    }

    for (int i = 0; i < THREAD_COUNT; i++) {
        pthread_create(&threads[i].t, NULL, checkerThread, &threads[i].threadData);
    }

    for (int i = 0; i <= THREAD_COUNT; i++) {
        printf("[THREAD-MAIN] Joining thread ID %d\n", i);
        pthread_join(threads[i].t, NULL);
    }

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
