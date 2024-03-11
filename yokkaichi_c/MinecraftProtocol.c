#include "../submodules/varint.c/varint.h"
#include "MinecraftProtocol.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

void writeVarInt(uint32_t value, char* buffer) {
    int index = 0;
    do {
        char byte = value & SEGMENT_BITS;
        value >>= 7;
        if (value != 0) {
            byte |= CONTINUE_BIT;
        }
        buffer[index++] = byte;
    } while (value != 0 && index < MAX_VARINT_LEN);
}

void packPingPacket() {
    MinecraftJavaPacket packet;
    MinecraftSLP pingPacket;

    // Fill in packet ID for Minecraft packet
    writeVarInt(PING_PACKET_ID, packet.packetID);

    // Fill in data for ping packet
    writeVarInt(47, pingPacket.protocolVersion); // We use 47 (1.8) because it's compatible with everything
    strncpy(pingPacket.serverAddress, "127.0.0.1", sizeof(pingPacket.serverAddress)); // We temporarily use localhost here
    pingPacket.serverPort = 25565; // We use 25565 here temporarily
    writeVarInt(1, pingPacket.nextState); // We use 1 here for getting the SLP
}

void pingJava(char *ip, uint16_t port) {
    // Create socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        printf("Error creating socket\n");
    }

    // Specify address
    struct sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    inet_pton(AF_INET, ip, &server_address.sin_addr);

    // Connect to server
    if (connect(sock, (struct sockaddr*)&server_address, sizeof(server_address)) == -1) {
        printf("Error connecting\n");
    }

    // Close socket
    close(sock);
}
