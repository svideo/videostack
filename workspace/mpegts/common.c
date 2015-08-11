#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

void hex_print(const char* buf, int len) {
    int count = 0;
    int i = 0;

    for(i=0; i<len; i++){
        if( count % 2 == 0)
            printf(" ");
        if( count % 16 == 0)
            printf("\n%09d: ", count);

        if( (unsigned char) buf[i] < 16)
            printf("0%x", (unsigned char) buf[i]);
        else
            printf("%x", (unsigned char) buf[i]);
        count++;
    }
    printf("\n");
}

void binary_print(int buf) {
    int i;
    char result[8];
    for (i=0; i<8; i++) {
        if (buf % 2 == 0)
            result[i] = '0';
        else
            result[i] = '1';
        buf = buf >> 1;
    }

    for (i=7; i>=0; i--) {
        printf("%c", result[i]);
    }
    printf("\n");
}

