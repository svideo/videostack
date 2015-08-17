#define DEBUG 1

#define TS_PACKET_SIZE 188
#define UNIT_BUF_SIZE 1024*1024
#define TS_PACKET_HEADER_SIZE 4

#define STREAM_TYPE_VIDEO_MPEG1     0x01
#define STREAM_TYPE_VIDEO_MPEG2     0x02
#define STREAM_TYPE_AUDIO_MPEG1     0x03
#define STREAM_TYPE_AUDIO_MPEG2     0x04
#define STREAM_TYPE_PRIVATE_SECTION 0x05
#define STREAM_TYPE_PRIVATE_DATA    0x06
#define STREAM_TYPE_AUDIO_AAC       0x0f
#define STREAM_TYPE_AUDIO_AAC_LATM  0x11
#define STREAM_TYPE_VIDEO_MPEG4     0x10
#define STREAM_TYPE_VIDEO_H264      0x1b
#define STREAM_TYPE_VIDEO_CAVS      0x42
#define STREAM_TYPE_VIDEO_VC1       0xea
#define STREAM_TYPE_VIDEO_DIRAC     0xd1

#define STREAM_TYPE_AUDIO_AC3       0x81
#define STREAM_TYPE_AUDIO_DTS       0x8a

typedef struct pid_table {
    unsigned int pid_pat;
    unsigned int pid_cat;
    unsigned int pid_pmt;
    unsigned int pid_video;
    unsigned int video_codec_id;
    unsigned int pid_audio;
    unsigned int audio_codec_id;
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
    unsigned char * buffer;
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
    unsigned int program_number:16;
    unsigned int :3;
    unsigned int program_map_pid:13;
    unsigned int crc_32:32;
} program_association_table;

typedef struct program_map_table {
    unsigned int table_id:8;
    unsigned int section_syntax_indicator:1;
    unsigned int :1;
    unsigned int reserved0:2;
    unsigned int section_length:12;
    unsigned int program_number:16;
    unsigned int reserved1:2;
    unsigned int version_number:5;
    unsigned int current_next_indicator:1;
    unsigned int section_number:8;
    unsigned int last_section_number:8;
    unsigned int reserved2:3;
    unsigned int pcr_pid:13;
    unsigned int reserved3:4;
    unsigned int program_info_length:12;
    unsigned int crc_32:32;
} program_map_table;

