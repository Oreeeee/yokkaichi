#include <stdio.h>
#include <stdbool.h>
#include "yokkaichi_structs.h"

#ifdef __linux__
#include <unistd.h>
#include <sys/syscall.h>
#endif

int getThreadId() {
    #ifdef __linux__
    int threadId = (syscall(SYS_gettid) - syscall(SYS_getpid)) - 1;
    #else
    int threadId = 0;
    #endif

    return threadId;
}

void checkServer(char *ip, uint16_t port, int threadId) {
    printf("[THREAD-%d] Got: IP: %s, Port: %d\n", threadId, ip, port);
}

void *checkerThread(void *args) {
    ThreadData *pSelf = (ThreadData*)args;
    int threadId = getThreadId();
    /* TODO: Add scanning logic here:
        - run a loop
        - check is a srv pointer NULL
        - if it is, then sleep for a few miliseconds and do nothing
        - if it isn't, pass the server to checkServer()
        - then, set srv pointer to NULL
     */
    printf("[THREAD-%d] Hello World from Thread!\nReceived: %s %d\n", threadId, pSelf->ip, pSelf->port);
    while (pSelf->isWorking) {
        if (pSelf->isBusy) {
            printf("[THREAD-%d] Got a server to check \n", threadId);
            checkServer(pSelf->ip, pSelf->port, threadId);
            pSelf->isBusy = false;
        }
    }
    return NULL;
}
