#include <stdio.h>
#include <stdbool.h>
#include "yokkaichi_structs.h"


void checkServer(MinecraftServer server) {
    printf("Got: IP: %s, Port: %d\n", server.ip, server.port);
}

void *checkerThread(void *argsRaw) {
    ThreadArgs *args = (ThreadArgs*)argsRaw;
    MinecraftServer *srv = args->server;
    /* TODO: Add scanning logic here:
        - run a loop
        - check is a srv pointer NULL
        - if it is, then sleep for a few miliseconds and do nothing
        - if it isn't, pass the server to checkServer()
        - then, set srv pointer to NULL
     */
    printf("[THREAD-%d] Hello World from Thread!\nReceived: %s %d\n", args->threadId, srv->ip, srv->port);
    return NULL;
}
