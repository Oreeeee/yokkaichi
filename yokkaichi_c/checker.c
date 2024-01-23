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

void checkServer(OpenPort openPort, int threadId) {
    printf("[THREAD-%d] Got: IP: %s, Port: %d\n", threadId, openPort.ip, openPort.port);
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
    while (pSelf->isWorking) {
        if (pSelf->isBusy) {
            printf("[THREAD-%d] Got a server to check \n", threadId);
            checkServer(pSelf->openPort, threadId);
            pSelf->isBusy = false;
        }
    }
    return NULL;
}
