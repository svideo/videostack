struct transport_packet_header * alloc_tph() {
    struct transport_packet_header * tph = calloc(1, sizeof(struct transport_packet_header));
    return tph;
}

void free_tph(struct transport_packet_header * tph) {
    free(tph);
}

struct unit * alloc_unit() {
    struct unit * unit = calloc(1, sizeof(struct unit) + 16 );
    unit->buffer = calloc(1, UNIT_BUF_SIZE);
    unit->buffer_offset = 0;
    unit->buffer_total_length = UNIT_BUF_SIZE;
    unit->pid = 0;
    return unit;
}

void reset_unit(struct unit * unit) {
    memset(unit->buffer, 0, unit->buffer_total_length);
    unit->buffer_offset = 0;
}

void free_unit(struct unit * unit) {
    free(unit->buffer);
    free(unit);
}

struct pid_table * alloc_pid_table() {
    struct pid_table * pid_table = calloc(1, sizeof(struct pid_table));
    pid_table->pid_pat = 0; // will not change
    pid_table->pid_cat = 1; // will not change
    pid_table->pid_pmt = 0; // will not change
    pid_table->pid_video = 0; // will not change
    pid_table->pid_audio = 0; // will not change
    return pid_table;
}

void free_pid_table(struct pid_table * pid_table) {
    free(pid_table);
}

struct program_association_table * alloc_pat() {
    struct program_association_table * pat = calloc(1, sizeof(struct program_association_table));
    memset(pat, 0, sizeof(struct program_association_table));
    return pat;
}

void free_pat(struct program_association_table * pat) {
    free(pat);
}

struct program_map_table * alloc_pmt() {
    struct program_map_table * pmt = calloc(1, sizeof(struct program_map_table));
    memset(pmt, 0, sizeof(struct program_map_table));
    return pmt;
}

void free_pmt(struct program_map_table * pmt) {
    free(pmt);
}

