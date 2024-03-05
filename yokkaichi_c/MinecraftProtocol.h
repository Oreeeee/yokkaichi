#ifndef MINECRAFT_PROTOCOL_H
#define MINECRAFT_PROTOCOL_H

#include <stdint.h>

#define MAX_VARINT_LEN 5

typedef struct {
    char lenght[MAX_VARINT_LEN];
    char packetID[MAX_VARINT_LEN];
    char data[2097151];
} MinecraftJavaPacket;

typedef struct {
    char protocolVersion[MAX_VARINT_LEN];
    char serverAddress[255]; // TODO: Replace this with Unicode string
    uint16_t serverPort;
    char nextState[MAX_VARINT_LEN];
} MinecraftSLP;

void pingJava(char *ip, uint16_t port);

#endif