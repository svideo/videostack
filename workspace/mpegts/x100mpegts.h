#define DEBUG 1

#define TS_PACKET_SIZE 188
#define UNIT_BUF_SIZE 1024*1024
#define TS_PACKET_HEADER_SIZE 4

typedef struct pid_table {
    unsigned int pid_pat;
    unsigned int pid_cat;
    unsigned int pid_pmt;
    unsigned int pid_video;
    unsigned int pid_audio;
} pid_table;

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

typedef struct unit {
    char * buffer;
    int buffer_offset;
    int buffer_total_length;
    int pid;
} unit;

typedef struct program_association_table {
    unsigned int table_id:8;
    unsigned int section_syntax_indicator:1;
    unsigned int :1;
    unsigned int reserved0:2;
    unsigned int section_length:12;
    unsigned int transport_stream_id:16;
    unsigned int reserved1:2;
    unsigned int version_number:5;
    unsigned int current_next_indicator:1;
    unsigned int section_number:8;
    unsigned int last_section_number:8;
    unsigned int crc_32:32;
} program_association_table;
