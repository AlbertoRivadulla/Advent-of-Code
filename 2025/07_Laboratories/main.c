#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "timer.h"
#include "regex_utils.h"

const size_t MAX_LINE_LENGTH = 1024;

size_t read_map(char* input_file_name, char **map, size_t *nr_cols, size_t *nr_rows) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    char line[MAX_LINE_LENGTH];
    *nr_rows = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        *nr_cols = strlen(line) - 1;
        (*nr_rows)++;
    }

    *map = malloc((*nr_cols) * (*nr_rows) * sizeof(char));

    fseek(input_file, 0, SEEK_SET);

    size_t curr_line = 0;
    size_t start_col = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        for (size_t i = 0; i < *nr_cols; ++i) {
            if (line[i] == '.') {
                (*map)[i + curr_line * (*nr_cols)] = 0;
            } 
            else if (line[i] == '^') {
                (*map)[i + curr_line * (*nr_cols)] = 1;
            }
            else if (line[i] == 'S') {
                start_col = i;
            }
        }
        curr_line++;
    }

    fclose(input_file);

    return start_col;
}

int propagate_lasers(char* map, size_t nr_cols, size_t nr_rows, size_t start_col) {
    char *beams = malloc(nr_cols * sizeof(size_t));
    char *next_beams = malloc(nr_cols * sizeof(size_t));
    for (size_t i = 1; i < nr_cols; ++i) {
        beams[i] = 0;
        next_beams[i] = 0;
    }
    beams[start_col] = 1;

    int nr_splits = 0;
    for (size_t curr_row = 1; curr_row < nr_rows; ++curr_row) {
        for (size_t col = 0; col < nr_cols; ++col) {
            if (beams[col] == 0) {
                continue;
            }

            if (map[col + curr_row * nr_cols] == 1) {
                // A splitter was found
                nr_splits += 1;

                // Try to split this beam in two
                size_t left = col - 1;
                size_t right = col + 1;
                if (left >= 0) {
                    next_beams[left] = 1;
                }
                if (right < nr_cols) {
                    next_beams[right] = 1;
                }
            }
            else {
                next_beams[col] = 1;
            }
            beams[col] = 0;
        }

        char *temp = beams;
        beams = next_beams;
        next_beams = temp;
    }

    free(beams);
    free(next_beams);

    return nr_splits;
}

void first_part(char *input_file_name) {
    size_t nr_cols;
    size_t nr_rows;
    char* map;

    size_t start_col = read_map(input_file_name, &map, &nr_cols, &nr_rows);

    int nr_splits = propagate_lasers(map, nr_cols, nr_rows, start_col);

    printf("Number of splits %d\n", nr_splits);

    free(map);
}

long propagate_lasers_quantum(char* map, size_t nr_cols, size_t nr_rows, size_t start_col) {
    char *beams = malloc(nr_cols * sizeof(size_t));
    char *next_beams = malloc(nr_cols * sizeof(size_t));
    long *nr_splits_array = malloc(nr_cols * sizeof(long));
    long *next_nr_splits_array = malloc(nr_cols * sizeof(long));
    for (size_t i = 1; i < nr_cols; ++i) {
        beams[i] = 0;
        next_beams[i] = 0;
        nr_splits_array[i] = 0;
        next_nr_splits_array[i] = 0;
    }
    beams[start_col] = 1;
    nr_splits_array[start_col] = 1;

    for (size_t curr_row = 1; curr_row < nr_rows; ++curr_row) {
        // Iterate over all the beams
        for (size_t col = 0; col < nr_cols; ++col) {
            if (beams[col] == 0) {
                continue;
            }

            if (map[col + curr_row * nr_cols] == 1) {
                // Try to split this beam in two
                size_t left = col - 1;
                size_t right = col + 1;
                if (left >= 0) {
                    next_beams[left] = 1;
                    next_nr_splits_array[left] += nr_splits_array[col];
                }
                if (right < nr_cols) {
                    next_beams[right] = 1;
                    next_nr_splits_array[right] += nr_splits_array[col];
                }
            }
            else {
                next_beams[col] = 1;
                next_nr_splits_array[col] += nr_splits_array[col];
            }
            beams[col] = 0;
            nr_splits_array[col] = 0;
        }

        char *temp = beams;
        beams = next_beams;
        next_beams = temp;

        long *temp_splits = nr_splits_array;
        nr_splits_array = next_nr_splits_array;
        next_nr_splits_array = temp_splits;
    }

    long nr_splits = 0;
    for (size_t col = 0; col < nr_cols; ++col) {
        nr_splits += nr_splits_array[col];
    }

    free(beams);
    free(next_beams);
    free(nr_splits_array);
    free(next_nr_splits_array);

    return nr_splits;
}

void second_part(char *input_file_name) {
    size_t nr_cols;
    size_t nr_rows;
    char* map;

    size_t start_col = read_map(input_file_name, &map, &nr_cols, &nr_rows);

    long nr_splits = propagate_lasers_quantum(map, nr_cols, nr_rows, start_col);

    printf("Number of splits %lu\n", nr_splits);

    free(map);
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
