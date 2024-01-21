#include <stdio.h>
#include <stdbool.h>
#include "yokkaichi_structs.h"

#ifdef __unix__
#include <unistd.h>
#include <sys/syscall.h>
#endif

int getThreadId() {
    #ifdef __unix__
    int threadId = syscall(SYS_gettid) - syscall(SYS_getpid);
    #else
    int threadId = 0;
    #endif

    return threadId;
}

void checkServer(MinecraftServer server) {
    printf("Got: IP: %s, Port: %d\n", server.ip, server.port);
}

void *checkerThread(void *args) {
    MinecraftServer *pServer = (MinecraftServer*)args;
    MinecraftServer server = *pServer;
    int threadId = getThreadId();
    /* TODO: Add scanning logic here:
        - run a loop
        - check is a srv pointer NULL
        - if it is, then sleep for a few miliseconds and do nothing
        - if it isn't, pass the server to checkServer()
        - then, set srv pointer to NULL
     */
    printf("[THREAD-%d] Hello World from Thread!\nReceived: %s %d\n", threadId, server.ip, server.port);
    while (server.scanning) {
        printf("[THREAD-%d] Scanning currently...\n", threadId);
    }
    return NULL;
}
