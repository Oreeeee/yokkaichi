#ifndef CHECKER_H
#define CHECKER_H

#include "yokkaichi_structs.h"

int getThreadId();
void checkServer(MinecraftServer server);
void *checkerThread(void *args);

#endif
