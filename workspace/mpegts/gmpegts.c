#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include "common.c"

#define DEBUG 1

#define TS_PACKET_SIZE 188
#define UNIT_BUF_SIZE 1024*1024
#define TS_PACKET_HEADER_SIZE 4
#define PID_PAT 0

typedef struct transport_packet_header {
    unsigned int transport_error_indicator:1;
    unsigned int payload_unit_start_indicator:1;
    unsigned int transport_priority:1;
    unsigned int pid:13;
    unsigned int transport_scrambing_control:2;
    unsigned int adaption_field_control:2;
    unsigned int continuity_counter:4;

    unsigned int adaptation_fields_length:8;
} transport_packet_header;

void debug_transport_packet_header( struct transport_packet_header * tph) {
    printf("transport_error_indicator: %d\t", tph->transport_error_indicator);
    printf("payload_unit_start_indicator: %d\t", tph->payload_unit_start_indicator);
    printf("transport_priority: %d\t", tph->transport_priority);
    printf("PID: %d\t", tph->pid);
    printf("transport_scrambing_control: %d\t", tph->transport_scrambing_control);
    printf("adaption_field_control: %d\t", tph->adaption_field_control);
    printf("continuity_counter: %d\t", tph->continuity_counter);
    printf("adaptation_field_length: %d\t", tph->adaptation_fields_length);
    printf("\n");
}

struct transport_packet_header * alloc_tph() {
    struct transport_packet_header * tph = calloc(1, sizeof(transport_packet_header));
    //printf("[%lu]\n", sizeof(transport_packet_header));
    //exit(0);
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
    if (tph->adaption_field_control == 2) {
        tph->adaptation_fields_length = 183;
    } else if (tph->adaption_field_control == 3) {
        tph->adaptation_fields_length = packet[4];
    } else {
        tph->adaptation_fields_length = 0;
    }
}

void free_tph(struct transport_packet_header * tph) {
    free(tph);
}

typedef struct unit {
    char * buffer;
    int buffer_offset;
    int buffer_active_length;
    int buffer_total_length;
    int pid;
} unit;

struct unit * alloc_unit() {
    struct unit * unit = calloc(1, sizeof(unit));
    unit->buffer = calloc(1, UNIT_BUF_SIZE);
    unit->buffer_offset = 0;
    unit->buffer_active_length = 0;
    unit->buffer_total_length = UNIT_BUF_SIZE;
    return unit;
}

void parse_unit(struct unit * unit) {
}

void reset_unit(struct unit * unit) {
    memset(unit->buffer, 0, unit->buffer_total_length);
    unit->buffer_offset = 0;
    unit->buffer_active_length = 0;
}

void free_unit(struct unit * unit) {
    free(unit->buffer);
    free(unit);
}

int main() {
    const char *path = "cku.ts";

    FILE * fp = fopen(path, "r");
    char buf[TS_PACKET_SIZE];

    struct transport_packet_header * tph = alloc_tph();
    struct unit * unit = alloc_unit();
    int packet_id = 0;

    while(fread(buf, TS_PACKET_SIZE, 1, fp)) {
        if ( buf[0] != 0x47 ) {
            printf("wrong sync_byte\n");
            return -1;
        }

        parse_transport_packet_header(tph, buf);
        if (tph->payload_unit_start_indicator == 1 && packet_id > 0) {
            parse_unit(unit);
            reset_unit(unit);
        }

        int payload_offset = TS_PACKET_HEADER_SIZE + tph->adaptation_fields_length;
        int payload_size = TS_PACKET_SIZE - payload_offset;
        memcpy(buf + payload_offset, unit->buffer + unit->buffer_offset, payload_size);
        unit->buffer_offset += payload_size;
        printf("[%d]\n", unit->buffer_offset);

        packet_id++;

#if DEBUG
        debug_transport_packet_header(tph);
#endif
    }

    free_tph(tph);
    free_unit(unit);

    return 0;
}

