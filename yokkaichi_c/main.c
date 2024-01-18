#include <stdio.h>

int main() {
    printf("Loading IP List\n");

    FILE *ipList;

    ipList = fopen("data/ips.txt", "r");
    if (ipList == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    char c = fgetc(ipList);
    while (c != EOF) {
        printf("%c", c);
        c = fgetc(ipList);
    }
    fclose(ipList);

    return 0;
}
