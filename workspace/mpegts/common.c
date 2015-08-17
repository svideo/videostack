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

static char * show_code_type_str(int code_type){
    switch(code_type){
        case  STREAM_TYPE_VIDEO_MPEG1  :
        case  STREAM_TYPE_AUDIO_MPEG1    :
            return "mpeg1";
            break;
        case  STREAM_TYPE_VIDEO_MPEG2    :
        case  STREAM_TYPE_AUDIO_MPEG2    :
            return "mpeg2";
            break;
        case  STREAM_TYPE_PRIVATE_SECTION:
            return "section";
            break;
        case  STREAM_TYPE_PRIVATE_DATA   :
            return "data";
            break;
        case  STREAM_TYPE_AUDIO_AAC      :
            return "aac";
            break;
        case  STREAM_TYPE_AUDIO_AAC_LATM :
            return "aac-latm";
            break;
        case  STREAM_TYPE_VIDEO_MPEG4    :
            return "mpeg4";
            break;
        case  STREAM_TYPE_VIDEO_H264     :
            return "h264";
            break;
        case  STREAM_TYPE_VIDEO_CAVS     :
            return "cavs";
            break;
        case  STREAM_TYPE_VIDEO_VC1      :
            return "vc1";
            break;
        case  STREAM_TYPE_VIDEO_DIRAC    :
            return "dirac";
            break;
        case  STREAM_TYPE_AUDIO_AC3      :
            return "ac3";
            break;
        case  STREAM_TYPE_AUDIO_DTS      :
            return "dts";
            break;
        default:
            return "nil";
            break;
    }
}
