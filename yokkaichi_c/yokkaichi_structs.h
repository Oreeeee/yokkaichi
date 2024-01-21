#ifndef YOKKAICHI_STRUCTS_H
#define YOKKAICHI_STRUCTS_H

#include <stdint.h>
#include <stdbool.h>
#include <pthread.h>
#include "yokkaichi_constants.h"


typedef struct {
    char ip[IP_LENGHT];
    uint16_t port;
    bool scanning;
} ThreadData;

typedef struct {
    pthread_t t;
    ThreadData threadData;
} Thread;

#endif
