#ifndef MINECRAFT_PROTOCOL_H
#define MINECRAFT_PROTOCOL_H

#include <stdint.h>

#define MAX_VARINT_LEN 6
#define SEGMENT_BITS 0x7F
#define CONTINUE_BIT 0x80
#define PING_PACKET_ID 0

typedef struct {
    char lenght[MAX_VARINT_LEN];
    char packetID[MAX_VARINT_LEN];
    char data[2097151];
} MinecraftJavaPacket;

typedef struct {
    char protocolVersion[MAX_VARINT_LEN];
    char serverAddress[255]; // TODO: Replace this with Unicode string
    uint16_t serverPort;
    char nextState[MAX_VARINT_LEN]; // Will always be 1 (status) here
} MinecraftSLP;

void writeVarInt(uint32_t value, char* buffer);
void pingJava(char *ip, uint16_t port);

#endif