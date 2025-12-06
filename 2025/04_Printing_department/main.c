#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "timer.h"
#include "regex_utils.h"

const size_t MAX_LINE_LENGTH = 256;

size_t get_map(char *input_file_name, char **map) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    char line[MAX_LINE_LENGTH];

    // Get the size of the map
    size_t map_size = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        map_size++;
    }

    *map = malloc(map_size * map_size * sizeof(char));

    // Go back to the beginning of the file
    fseek(input_file, 0, SEEK_SET);

    size_t line_nr = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        for (size_t i = 0; i < map_size; ++i) {
            if (line[i] == '.') {
                (*map)[i + line_nr * map_size] = 0;
            } else if (line[i] == '@') {
                 (*map)[i + line_nr * map_size] = 1;
            }
        }

        line_nr++;
    }

    fclose(input_file);

    return map_size;
}

bool is_accessible(const char* map, size_t map_size, int i, int j) {
    int nr_occupied_neighs = 0;

    for (int neigh_i = i - 1; neigh_i <= i + 1; ++neigh_i ) {
        if (neigh_i < 0 || neigh_i >= (int)map_size) {
            continue;
        }
        for (int neigh_j = j - 1; neigh_j <= j + 1; ++neigh_j ) {
            if (neigh_j < 0 || neigh_j >= (int)map_size || (neigh_i == i && neigh_j == j)) {
                continue;
            }

            if (map[neigh_i*map_size + neigh_j] != 0) {
                nr_occupied_neighs++;
                if (nr_occupied_neighs == 4) {
                    return false;
                }
            }
        }
    }

    return true;
}

void first_part(char *input_file_name) {
    char* map = NULL;
    size_t map_size = get_map(input_file_name, &map);

    int nr_accessible = 0;
    for (size_t i = 0; i < map_size; ++i) {
        for (size_t j = 0; j < map_size; ++j) {
            if (map[i*map_size + j] == 1 && is_accessible(map, map_size, i, j)) {
                nr_accessible += 1;
            }
        }
    }

    free(map);

    printf("Number of accessible rolls: %d\n", nr_accessible);
}

void second_part(char *input_file_name) {
    char* map = NULL;
    size_t map_size = get_map(input_file_name, &map);

    int nr_removed = 0;
    int nr_removed_now = 0;
    do {
        nr_removed_now = 0;
        for (size_t i = 0; i < map_size; ++i) {
            for (size_t j = 0; j < map_size; ++j) {
                if (map[i*map_size + j] == 1 && is_accessible(map, map_size, i, j)) {
                    nr_removed_now += 1;
                    map[i*map_size + j] = 0;
                }
            }
        }
        nr_removed += nr_removed_now;
    } while (nr_removed_now != 0);

    free(map);

    printf("Number of rolls removed: %d\n", nr_removed);
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
