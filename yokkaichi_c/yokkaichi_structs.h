#ifndef YOKKAICHI_STRUCTS_H
#define YOKKAICHI_STRUCTS_H

#include <stdint.h>
#include "yokkaichi_constants.h"


typedef struct {
    char ip[IP_LENGHT];
    uint16_t port;
} MinecraftServer; /* TODO: Rename this struct, a different struct will use this name in the future */

typedef struct {
    uint16_t threadId;
    MinecraftServer *server;
} ThreadArgs;

#endif
