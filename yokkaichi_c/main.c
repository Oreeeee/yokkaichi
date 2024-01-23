#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h> /* Temporary */
#include "yokkaichi_constants.h"
#include "yokkaichi_structs.h"
#include "checker.h"

void assignScanJob(Thread *threads, OpenPort openPort) {
    /* Assign the scanning job for the first free thread */
    ThreadData *threadContext;
    while (true) {
        for (int i = 0; i < THREAD_COUNT; i++) {
            threadContext = &threads[i].threadData;
            if (!threadContext->isBusy) {
                threadContext->openPort = openPort;
                threadContext->isBusy = true;
                return;
            }
        }
    }
}

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

    printf("[THREAD-MAIN] Starting up threads\n");
    for (int i = 0; i < THREAD_COUNT; i++) {
        threads[i].threadData.isWorking = true;
        pthread_create(&threads[i].t, NULL, checkerThread, &threads[i].threadData);
    }

    /* Pretend we find a open port here */
    sleep(3);
    OpenPort p;
    strncpy(p.ip, "127.0.0.1", IP_LENGHT);
    p.port = 25565;
    assignScanJob(threads, p);
    sleep(3);

    for (int i = 0; i < THREAD_COUNT; i++) {
        ThreadData *threadContext = &threads[i].threadData;
        printf("[THREAD-MAIN] Joining thread ID %d\n", i);
        while (true) {
            if (!threadContext->isBusy) {
                threadContext->isWorking = false;
                break;
            }
        }
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
