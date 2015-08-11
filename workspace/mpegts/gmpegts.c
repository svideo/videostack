#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include "common.c"

#define DEBUG 1

#define TS_PACKET_SIZE 188

typedef struct transport_packet_header {
    unsigned int transport_error_indicator:1;
    unsigned int payload_unit_start_indicator:1;
    unsigned int transport_priority:1;
    unsigned int pid:13;
    unsigned int transport_scrambing_control:2;
    unsigned int adaption_field_control:2;
    unsigned int continuity_counter:4;
} transport_packet_header;

void debug_transport_packet_header( struct transport_packet_header * tph) {
    printf("transport_error_indicator: %d\t", tph->transport_error_indicator);
    printf("payload_unit_start_indicator: %d\t", tph->payload_unit_start_indicator);
    printf("transport_priority: %d\t", tph->transport_priority);
    printf("PID: %d\t", tph->pid);
    printf("transport_scrambing_control: %d\t", tph->transport_scrambing_control);
    printf("adaption_field_control: %d\t", tph->adaption_field_control);
    printf("continuity_counter: %d\n", tph->continuity_counter);
}

struct transport_packet_header * alloc_tph() {
    struct transport_packet_header * tph = calloc(1, sizeof(transport_packet_header));
    return tph;
}

void parse_transport_packet_header(transport_packet_header * tph, char * packet) {
    tph->transport_error_indicator    = packet[1] >> 7;
    tph->payload_unit_start_indicator = packet[1] << 1 >> 7;
    tph->transport_priority           = packet[1] << 2 >> 7;
    tph->pid                          = ( packet[1] << 8 | packet[2] ) << 3 >> 3;
    tph->transport_scrambing_control  = packet[3] >> 6;
    tph->adaption_field_control       = packet[3] << 2 >> 6;
    tph->continuity_counter           = packet[3] << 4 >> 4;
}

void free_tph(struct transport_packet_header * tph) {
    free(tph);
}

int main() {
    const char *path = "cku.ts";

    FILE * fp = fopen(path, "r");
    char buf[TS_PACKET_SIZE];

    struct transport_packet_header * tph = alloc_tph();

    while(fread(buf, TS_PACKET_SIZE, 1, fp)) {
        if ( buf[0] != 0x47 ) {
            printf("wrong sync_byte\n");
            return -1;
        }

        parse_transport_packet_header(tph, buf);

#if DEBUG
        debug_transport_packet_header(tph);
#endif
    }

    free_tph(tph);

    return 0;
}

