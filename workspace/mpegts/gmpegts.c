#include "common.c"
#include "x100mpegts.h"
#include "x100mpegts_debug.c"
#include "x100mpegts_alloc.c"

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

void parse_pat(struct unit * unit, struct pid_table * pid_table, struct program_association_table * pat) {
    pat->table_id = unit->buffer[0];
    pat->section_syntax_indicator = unit->buffer[1] >> 7;
    debug_program_association_table(pat);
}

void parse_unit(struct unit * unit, struct pid_table * pid_table, struct program_association_table * pat) {
    if(unit->pid == pid_table->pid_pat) {
        printf("[%d]=[%d]PAT found\n", unit->pid, pid_table->pid_pat);
        parse_pat(unit, pid_table, pat);
    }
}

int main() {
    const char *path = "cku.ts";

    FILE * fp = fopen(path, "r");
    char buf[TS_PACKET_SIZE];

    struct transport_packet_header * tph = alloc_tph();
    struct unit * unit = alloc_unit();
    struct pid_table * pid_table = alloc_pid_table();
    struct program_association_table * pat = alloc_pat();
    int packet_id = 0;

    while(fread(buf, TS_PACKET_SIZE, 1, fp)) {
        if ( buf[0] != 0x47 ) {
            printf("wrong sync_byte\n");
            return -1;
        }

        parse_transport_packet_header(tph, buf);

        if (tph->payload_unit_start_indicator == 1 && packet_id > 0) {
            parse_unit(unit, pid_table, pat);
            reset_unit(unit);
        }

        int payload_offset = TS_PACKET_HEADER_SIZE + tph->adaptation_fields_length;
        int payload_size = TS_PACKET_SIZE - payload_offset;
        memcpy(buf + payload_offset, unit->buffer + unit->buffer_offset, payload_size);
        unit->buffer_offset += payload_size;
        unit->pid = tph->pid;
        //printf("[%d]\n", unit->buffer_offset);

        packet_id++;

#if DEBUG
        //debug_transport_packet_header(tph);
#endif
    }

    free_pat(pat);
    free_tph(tph);
    free_unit(unit);
    free_pid_table(pid_table);

    return 0;
}

