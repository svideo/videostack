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

void debug_program_association_table( struct program_association_table * pat) {
    printf("table_id: %d\t", pat->table_id);
    printf("section_syntax_indicator: %d\t", pat->section_syntax_indicator);
    printf("section_length: %d\t", pat->section_length);
    printf("transport_stream_id: %d\t", pat->transport_stream_id);
    printf("version_number: %d\t", pat->version_number);
    printf("current_next_indicator: %d\t", pat->current_next_indicator);
    printf("section_number: %d\t", pat->section_number);
    printf("last_section_number: %d\t", pat->last_section_number);
    printf("crc_32: %d\t", pat->crc_32);
    printf("\n");
}
