#include "x100mpegts.h"
#include "common.c"
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
    pat->section_length = ( unit->buffer[1] & 0x03 ) | unit->buffer[2];
    pat->transport_stream_id = unit->buffer[3] << 8 | unit->buffer[4];
    pat->version_number = unit->buffer[5] & 0x3e;
    pat->current_next_indicator = unit->buffer[5] & 0x01;
    pat->section_number = unit->buffer[6];
    pat->last_section_number = unit->buffer[7];
    pat->program_number = unit->buffer[8] << 8 | unit->buffer[9];
    pat->program_map_pid = (unit->buffer[10] << 8 | unit->buffer[11]) & 0x1fff;
    pid_table->pid_pmt = pat->program_map_pid;
    debug_program_association_table(pat);
}

void parse_pmt(struct unit * unit, struct pid_table * pid_table, struct program_map_table * pmt) {
    pmt->table_id = unit->buffer[0];
    pmt->section_syntax_indicator = unit->buffer[1] >> 7;
    pmt->section_length = ( unit->buffer[1] & 0x03 ) | unit->buffer[2];
    pmt->program_number = unit->buffer[3] << 8 | unit->buffer[4];
    pmt->version_number = unit->buffer[5] & 0x3e;
    pmt->current_next_indicator = unit->buffer[5] & 0x01;
    pmt->section_number = unit->buffer[6];
    pmt->last_section_number = unit->buffer[7];
    pmt->pcr_pid = (unit->buffer[8] << 8 | unit->buffer[9]) & 0x1fff;
    pmt->program_info_length = (unit->buffer[10] << 8 | unit->buffer[11]) & 0x0fff;
    
    unsigned int type = unit->buffer[12];
    unsigned int epid = (unit->buffer[13] << 8 | unit->buffer[14] ) & 0x1fff;
    unsigned int es_info_length = (unit->buffer[15] << 8 | unit->buffer[16] ) & 0x0fff;
    printf("type:[%x]", type);
    printf("pid:[%x]", epid );
    printf("es_info_length:[%d]", es_info_length );

    unsigned int o = 5;
    unsigned int type2 = unit->buffer[12 + o];
    unsigned int epid2 = (unit->buffer[13+o] << 8 | unit->buffer[14+o] ) & 0x1fff;
    unsigned int es_info_length2 = (unit->buffer[15+o] << 8 | unit->buffer[16+o] ) & 0x0fff;
    printf("type:[%x]", type2 );
    printf("pid:[%x]", epid2 );
    printf("es_info_length:[%d]", es_info_length2 );
    debug_program_map_table(pmt);
}

void parse_unit(struct unit * unit, struct pid_table * pid_table, struct program_association_table * pat, struct program_map_table * pmt) {
    if(unit->pid == pid_table->pid_pat) {
        parse_pat(unit, pid_table, pat);
    } else if (unit->pid == pid_table->pid_pmt) {
        parse_pmt(unit, pid_table, pmt);
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
    struct program_map_table * pmt = alloc_pmt();
    int packet_id = 0;
    int packet_wanted_number = 100000;
    int section_wanted_number = 3;

    while(fread(buf, TS_PACKET_SIZE, 1, fp)) {
        if (!packet_wanted_number)
            return 0;

        if ( buf[0] != 0x47 ) {
            printf("wrong sync_byte\n");
            return -1;
        }

        parse_transport_packet_header(tph, buf);

        if (tph->payload_unit_start_indicator == 1 && packet_id > 0) {
            if(!section_wanted_number)
                return 0;
            
            parse_unit(unit, pid_table, pat, pmt);
            reset_unit(unit);
            section_wanted_number--;
        }

        int payload_offset = TS_PACKET_HEADER_SIZE + tph->adaptation_fields_length + 1;
        int payload_size = TS_PACKET_SIZE - payload_offset;
        memcpy(unit->buffer + unit->buffer_offset, buf + payload_offset, payload_size);
        unit->buffer_offset += payload_size;
        unit->pid = tph->pid;

        packet_id++;
        packet_wanted_number--;

#if DEBUG
        //debug_transport_packet_header(tph);
#endif
    }

    free_pmt(pmt);
    free_pat(pat);
    free_tph(tph);
    free_unit(unit);
    free_pid_table(pid_table);

    return 0;
}

