#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include "timer.h"

const size_t MAX_LINE_LENGTH = 1024;

typedef struct {
    unsigned long start;
    unsigned long end;
} IdRange;

void get_ranges_and_ids(char *input_file_name, IdRange **id_ranges, size_t *nr_id_ranges, unsigned long **ids, 
    size_t *nr_ids) {

    *nr_id_ranges = 0;
    *nr_ids = 0;

    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    char line[MAX_LINE_LENGTH];
    while(fgets(line, sizeof(line), input_file) != NULL) {
        size_t line_len = strlen(line);

        if (line_len == 1) {
            // Empty line
            continue;
        }

        // Identify lines with a range of IDs, and with a single ID
        for (size_t i = 0; i < line_len; ++i) {
            if (line[i] == '-') {
                (*nr_id_ranges)++;
                break;
            }
            if (i == line_len - 1) {
                (*nr_ids)++;
            }
        }
    }

    *id_ranges = malloc(*nr_id_ranges * sizeof(IdRange));
    *ids = malloc(*nr_ids * sizeof(unsigned long));

    fseek(input_file, 0, SEEK_SET);

    size_t range_idx = 0;
    size_t id_idx = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        // Remove trailing \n
        size_t line_len = strlen(line);
        if (line_len > 0 && line[line_len-1] == '\n') {
            line[line_len-1] = '\0';
        }

        if (line_len == 1) {
            continue;
        }

        char *token = strtok(line, "-");
        bool begin_range = true;
        while (token != NULL) {
            char *next_token = strtok(NULL, "-");

            if (next_token != NULL && begin_range) {
                (*id_ranges)[range_idx].start = atol(token);
                begin_range = false;
            } 
            else if (next_token == NULL) {
                if (begin_range) {
                    (*ids)[id_idx++] = atol(token);
                }
                else {
                    (*id_ranges)[range_idx].end = atol(token);
                    range_idx++;
                    begin_range = true;
                }
            }
            token = next_token;
        }
    }

    fclose(input_file);
}

int count_ids_in_ranges(IdRange *id_ranges, size_t nr_id_ranges, unsigned long *ids, size_t nr_ids) {
    int nr_in_ranges = 0;

    for (size_t i = 0; i < nr_ids; ++i) {
        for (size_t j = 0; j < nr_id_ranges; ++j) {
            if (ids[i] >= id_ranges[j].start && ids[i] <= id_ranges[j].end) {
                nr_in_ranges++;
                break;
            }
        }
    }

    return nr_in_ranges;
}

void first_part(char *input_file_name) {
    IdRange *id_ranges;
    size_t nr_id_ranges;
    unsigned long *ids;
    size_t nr_ids;

    get_ranges_and_ids(input_file_name, &id_ranges, &nr_id_ranges, &ids, &nr_ids);

    // printf("Number of ranges %d\n", nr_id_ranges);
    // printf("Number of IDs %d\n", nr_ids);
    //
    // for (size_t i = 0; i < nr_id_ranges; ++i) {
    //     printf("Range %lu - %lu\n", id_ranges[i].start, id_ranges[i].end);
    // }
    // for (size_t i = 0; i < nr_ids; ++i) {
    //     printf("ID %lu\n", ids[i]);
    // }

    int nr_fresh = count_ids_in_ranges(id_ranges, nr_id_ranges, ids, nr_ids);

    free(id_ranges);
    free(ids);

    printf("Number of fresh ingredients: %d\n", nr_fresh);
}

bool try_to_merge(IdRange *id_ranges, size_t i, size_t j) {
    // If they overlap, merge the two ranges in the first one
    if ((id_ranges[i].start <= id_ranges[j].start && id_ranges[i].end >= id_ranges[j].start) ||
        (id_ranges[i].start <= id_ranges[j].end && id_ranges[i].end >= id_ranges[j].end)) {
        unsigned long start = id_ranges[i].start <= id_ranges[j].start ? id_ranges[i].start : id_ranges[j].start;
        unsigned long end = id_ranges[i].end >= id_ranges[j].end ? id_ranges[i].end : id_ranges[j].end;
        id_ranges[i].start = start;
        id_ranges[i].end = end;
        return true;
    }

    return false;
}

unsigned long long count_total_ids_in_ranges(IdRange *id_ranges, size_t nr_id_ranges) {
    bool *merged = malloc(nr_id_ranges * sizeof(bool));
    for (size_t i = 0; i < nr_id_ranges; ++i) {
        merged[i] = false;
    }

    int nr_merged;
    do {
        nr_merged = 0;

        // Iterate over pairs of ranges, and try to merge them
        for (size_t i = 0; i < nr_id_ranges; ++i) {
            if (merged[i]) {
                continue;
            }
            for (size_t j = 0; j < nr_id_ranges; ++j) {
                if (merged[j] || i == j) {
                    continue;
                }
                if (try_to_merge(id_ranges, i, j)) {
                    merged[j] = true;
                    nr_merged++;
                }
            }
        }

    } while (nr_merged > 0);

    unsigned long long nr_ids_in_ranges = 0;
    for (size_t i = 0; i < nr_id_ranges; ++i) {
        if (merged[i]) {
            continue;
        }

        nr_ids_in_ranges += (unsigned long long)id_ranges[i].end - (unsigned long long)id_ranges[i].start + 1ull;
    }

    free(merged);

    return nr_ids_in_ranges;
}

void second_part(char *input_file_name) {
    IdRange *id_ranges;
    size_t nr_id_ranges;
    unsigned long *ids;
    size_t nr_ids;

    get_ranges_and_ids(input_file_name, &id_ranges, &nr_id_ranges, &ids, &nr_ids);
    
    // printf("Number of ranges %d\n", nr_id_ranges);
    // printf("Number of IDs %d\n", nr_ids);
    //
    // for (size_t i = 0; i < nr_id_ranges; ++i) {
    //     printf("Range %lu - %lu\n", id_ranges[i].start, id_ranges[i].end);
    // }
    // for (size_t i = 0; i < nr_ids; ++i) {
    //     printf("ID %lu\n", ids[i]);
    // }

    unsigned long long nr_fresh_ids = count_total_ids_in_ranges(id_ranges, nr_id_ranges);

    free(id_ranges);
    free(ids);

    printf("Total nr of IDs of fresh ingredients %llu\n", nr_fresh_ids);
}

int main(int argc, char **argv) {
    Timer timer;
    if (argc < 2) {
        printf("Usage: \n\t./main <input_file>\n");
        exit(1);
    }

    char *input_file_name = argv[1];

    timer_start(&timer, "First part");
    first_part(input_file_name);
    timer_stop(&timer);

    timer_start(&timer, "Second part");
    second_part(input_file_name);
    timer_stop(&timer);


    return 0;
}
