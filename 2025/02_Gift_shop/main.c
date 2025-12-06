#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include "timer.h"

const size_t MAX_LINE_LENGTH = 1024;
const size_t MAX_NR_CHARS = 12;

typedef struct {
    unsigned long start;
    unsigned long end;
} IdInterval;

size_t get_id_intervals(char *file_name, IdInterval **id_intervals) {
    FILE *input_file = fopen(file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", file_name);
        exit(1);
    }

    // Count the number of intervals in the file
    size_t nr_intervals = 1;
    char c;
    while ((c = fgetc(input_file)) != EOF && c != '\n') {
        if (c == ',') {
            nr_intervals++;
        }
    }

    // Malloc the list of ID ranges
    *id_intervals = malloc(nr_intervals * sizeof(IdInterval));

    // Go back to the beginning of the file
    fseek(input_file, 0, SEEK_SET);

    // Get the different intervals
    char this_nr[MAX_NR_CHARS];
    size_t this_nr_size = 0;
    bool begin_interval = true;
    size_t nr_interval = 0;
    do {
        c = fgetc(input_file);

        if (c == ',' || c == '-' || c == '\n') {
            this_nr[this_nr_size] = '\0';
            if (begin_interval) {
                (*id_intervals)[nr_interval].start = atol(this_nr);
            } else {
                (*id_intervals)[nr_interval].end = atol(this_nr);
            }

            this_nr[0] = '\0';
            this_nr_size = 0;
        }

        if (c == ',') {
            begin_interval = true;
            nr_interval++;
            continue;
        }
        else if (c == '-') {
            begin_interval = false;
            continue;
        }

        this_nr[this_nr_size++] = c;
    } while (c != '\n');

    fclose(input_file);

    return nr_intervals;
}

void first_part(char *input_file_name) {
    IdInterval *id_intervals;
    size_t nr_intervals = get_id_intervals(input_file_name, &id_intervals);

    int nr_invalid = 0;
    unsigned long long sum_invalid = 0;
    for (size_t i = 0; i < nr_intervals; ++i) {
        // Iterate over all numbers in the interval
        for (unsigned long nr = id_intervals[i].start; nr <= id_intervals[i].end; ++nr) {
            char nr_string[MAX_NR_CHARS];
            sprintf(nr_string, "%lu", nr);
            size_t len_str = 0;
            for (size_t j = 0; j < MAX_NR_CHARS; ++j) {
                if (nr_string[j] == '\0') {
                    len_str = j;
                    break;
                }
            }

            if (len_str % 2 != 0) {
                continue;
            }

            if (strncmp(nr_string, nr_string + len_str/2, len_str/2) == 0) {
                nr_invalid++;
                sum_invalid += atol(nr_string);
            }
        }
        // printf("Interval %lu - %lu\n", id_intervals[i].start, id_intervals[i].end);
        // printf("Numbers in interval %lu\n", id_intervals[i].end - id_intervals[i].start);
    }

    free(id_intervals);

    printf("Number of invalid IDs: %d\n", nr_invalid);
    printf("Sum of invalid IDs: %llu\n", sum_invalid);
}

bool check_id_invalid_second(char* nr_string, size_t len) {

    // Find numbers that the length is divisible by
    for (size_t sub_len = 1; sub_len <= len/2; ++sub_len) {
        bool this_sub_len_invalid = true;
        if (len % sub_len != 0) {
            continue;
        }

        size_t nr_substrs = len / sub_len;
        for (size_t i = 1; i < nr_substrs; ++i) {
            if (strncmp(nr_string, nr_string + i * sub_len, sub_len) != 0) {
                this_sub_len_invalid = false;
                break;
            }
        }
        if (this_sub_len_invalid) {
            // printf("Invalid %s -- %d\n", nr_string, sub_len);
            return true;
        }
    }

    return false;
}

void second_part(char *input_file_name) {
    IdInterval *id_intervals;
    size_t nr_intervals = get_id_intervals(input_file_name, &id_intervals);

    int nr_invalid = 0;
    unsigned long long sum_invalid = 0;
    for (size_t i = 0; i < nr_intervals; ++i) {
        // Iterate over all numbers in the interval
        for (unsigned long nr = id_intervals[i].start; nr <= id_intervals[i].end; ++nr) {
            char nr_string[MAX_NR_CHARS];
            sprintf(nr_string, "%lu", nr);
            size_t len_str = 0;
            for (size_t j = 0; j < MAX_NR_CHARS; ++j) {
                if (nr_string[j] == '\0') {
                    len_str = j;
                    break;
                }
            }

            if (check_id_invalid_second(nr_string, len_str)) {
                nr_invalid++;
                sum_invalid += atol(nr_string);
            }
        }
        // printf("Interval %lu - %lu\n", id_intervals[i].start, id_intervals[i].end);
        // printf("Numbers in interval %lu\n", id_intervals[i].end - id_intervals[i].start);
    }

    free(id_intervals);

    printf("Number of invalid IDs: %d\n", nr_invalid);
    printf("Sum of invalid IDs: %llu\n", sum_invalid);
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
