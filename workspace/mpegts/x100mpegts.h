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
    int buffer_active_length;
    int buffer_total_length;
    int pid;
} unit;

typedef struct pid_table {
    unsigned int pid_pat;
    unsigned int pid_cat;
    unsigned int pid_pmt;
    unsigned int pid_video;
    unsigned int pid_audio;
} pid_table;
