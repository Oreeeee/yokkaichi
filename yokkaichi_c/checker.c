#include <stdio.h>
#include <stdbool.h>
#include "yokkaichi_structs.h"

void checkServer(MinecraftServer server) {
    printf("Got: IP: %s, Port: %d\n", server.ip, server.port);
}
