#ifndef YOKKAICHI_STRUCTS_H
#define YOKKAICHI_STRUCTS_H

#include "yokkaichi_constants.h"


typedef struct {
    char ip[IP_LENGHT];
    int port;
} MinecraftServer; /* TODO: Rename this struct, a different struct will use this name in the future */

typedef struct {
    int threadId;
    MinecraftServer *server;
} ThreadArgs;

#endif
