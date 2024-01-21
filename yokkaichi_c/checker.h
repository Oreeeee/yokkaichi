#ifndef CHECKER_H
#define CHECKER_H

#include "yokkaichi_structs.h"

int getThreadId();
void checkServer(char *ip, uint16_t port);
void *checkerThread(void *args);

#endif
