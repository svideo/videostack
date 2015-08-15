void debug_transport_packet_header( struct transport_packet_header * tph) {
    printf("[Packet] ");
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

void debug_program_association_table( struct program_association_table * pat) {
    printf("[PAT] ");
    printf("table_id: %d\t", pat->table_id);
    printf("section_syntax_indicator: %d\t", pat->section_syntax_indicator);
    printf("section_length: %d\t", pat->section_length);
    printf("transport_stream_id: %d\t", pat->transport_stream_id);
    printf("version_number: %d\t", pat->version_number);
    printf("current_next_indicator: %d\t", pat->current_next_indicator);
    printf("section_number: %d\t", pat->section_number);
    printf("last_section_number: %d\t", pat->last_section_number);
    printf("program_number: %d\t", pat->program_number);
    printf("program_map_pid: %d\t", pat->program_map_pid);
    printf("crc_32: %d\t", pat->crc_32);
    printf("\n");
}

void debug_program_map_table( struct program_map_table * pmt) {
    printf("[PMT] ");
    printf("table_id: %d\t", pmt->table_id);
    printf("section_syntax_indicator: %d\t", pmt->section_syntax_indicator);
    printf("section_length: %d\t", pmt->section_length);
    printf("program_number: %d\t", pmt->program_number);
    printf("version_number: %d\t", pmt->version_number);
    printf("current_next_indicator: %d\t", pmt->current_next_indicator);
    printf("section_number: %d\t", pmt->section_number);
    printf("last_section_number: %d\t", pmt->last_section_number);
    printf("pcr_pid: %d\t", pmt->pcr_pid);
    printf("program_info_length: %d\t", pmt->program_info_length);
    printf("crc_32: %d\t", pmt->crc_32);
    printf("\n");
}

