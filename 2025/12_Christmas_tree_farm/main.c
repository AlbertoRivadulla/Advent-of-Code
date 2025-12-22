#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "timer.h"
#include "regex_utils.h"

const size_t MAX_LINE_LENGTH = 1024;

const size_t NR_SHAPES = 6;
const size_t MAX_DIMENSION = 50; // Considering the given input

typedef struct Region {
    int size_x;
    int size_y;
    size_t count_each_shape[NR_SHAPES];
} Region;

size_t read_input(char *input_file_name, char shapes[NR_SHAPES][9], struct Region **regions) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    regex_t regex_region;
    const char *pattern_region = "([0-9]+)x([0-9]+):";
    if (regcomp(&regex_region, pattern_region, REG_EXTENDED)) {
        fprintf(stderr, "Could not compile regex pattern %s\n", pattern_region);
        exit(1);
    }
    regex_t regex_count;
    const char *pattern_count = " ([0-9]+)";
    if (regcomp(&regex_count, pattern_count, REG_EXTENDED)) {
        fprintf(stderr, "Could not compile regex pattern %s\n", pattern_count);
        exit(1);
    }
    const size_t max_groups = 10;
    regmatch_t group_array[max_groups];


    char line[MAX_LINE_LENGTH];

    // Parse the different shapes
    for (size_t shape_idx = 0; shape_idx < NR_SHAPES; ++shape_idx) {
        // Skip the first line
        if (fgets(line, sizeof(line), input_file) == NULL) {
            printf("Error reading line\n");
            exit(1);
        }

        for (size_t j = 0; j < 3; ++j) {
            if (fgets(line, sizeof(line), input_file) == NULL) {
                printf("Error reading line\n");
                exit(1);
            }
            for (size_t k = 0; k < 3; ++k) {
                if (line[k] == '#') {
                    shapes[shape_idx][j * 3 + k] = 1;
                } else {
                    shapes[shape_idx][j * 3 + k] = 0;
                }
            }
        }

        // Skip the last line
        if (fgets(line, sizeof(line), input_file) == NULL) {
            printf("Error reading line\n");
            exit(1);
        }
    }

    // Read the present shapes and count the number of regions
    size_t nr_regions = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        if (regexec(&regex_region, line, max_groups, group_array, 0) == 0) {
            ++nr_regions;
        }
    }

    // Parse the different regions
    fseek(input_file, 0, SEEK_SET);
    *regions = malloc(nr_regions * sizeof(struct Region));
    size_t region_idx = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        if (regexec(&regex_region, line, max_groups, group_array, 0) == 0) {
            // Get the size of the group
            char target_str[16];
            extract_group(line, group_array[1], target_str, sizeof(target_str));
            (*regions)[region_idx].size_x = atoi(target_str);
            extract_group(line, group_array[2], target_str, sizeof(target_str));
            (*regions)[region_idx].size_y = atoi(target_str);

            // Get the different counts
            char *cursor = line;
            size_t count_idx = 0;
            while (regexec(&regex_count, cursor, max_groups, group_array, 0) == 0) {
                extract_group(cursor, group_array[1], target_str, sizeof(target_str));
                (*regions)[region_idx].count_each_shape[count_idx++] = atoi(target_str);
                cursor += group_array[0].rm_eo;
            }

            ++region_idx;
        }
    }

    fclose(input_file);

    return nr_regions;
}

// bool check_shapes_fit_rec(char shapes[NR_SHAPES][0], struct Region *region, char map[MAX_DIMENSION][MAX_DIMENSION]) {
//     // Make a copy of the map
// }

int count_regions_that_fit(char shapes[NR_SHAPES][9], struct Region *regions, size_t nr_regions) {
    int nr_fits = 0;

    // for (size_t i = 0; i < nr_regions; ++i) {
    //     // Construct the region map
    //     char map[MAX_DIMENSION][MAX_DIMENSION];
    //     for (size_t j = 0; j < MAX_DIMENSION; ++j) {
    //         for (size_t k = 0; k < MAX_DIMENSION; ++k) {
    //             map[j][k] = 0;
    //         }
    //     }
    //
    //     // Check if all shapes fit recursively
    //     if (check_shapes_fit_rec(shapes, regions[i], map)) {
    //         nr_fits += 1;
    //     }
    // }

    for (size_t i = 0; i < nr_regions; ++i) {
        // Area of the region
        int region_area = regions[i].size_x * regions[i].size_y;

        // Area needed if all shapes were 3x3 filled squares
        int needed_area = 0;
        for (size_t j = 0; j < NR_SHAPES; ++j) {
            needed_area += 3 * 3 * regions[i].count_each_shape[j];
        }

        nr_fits = region_area >= needed_area ? nr_fits + 1 : nr_fits;
        // if (region_area >= needed_area) {
        //     printf("Increase nr fits")
        //     ++nr_fits;
        // }
    }

    return nr_fits;
}

void first_part(char *input_file_name) {
    char shapes[NR_SHAPES][9];
    Region *regions;

    size_t nr_regions = read_input(input_file_name, shapes, &regions);

    for (size_t i = 0; i < NR_SHAPES; ++i) {
        printf("Shape %zu\n", i);
        for (size_t j = 0; j < 3; ++j) {
            for (size_t k = 0; k < 3; ++k) {
                if (shapes[i][j * 3 + k] == 1) {
                    printf("A");
                } else {
                    printf(".");
                }
            }
            printf("\n");
        }
        printf("\n");
    }

    printf("Number of regions %zu\n", nr_regions);
    for (size_t i = 0; i < nr_regions; ++i) {
        printf("\tregion %zu: %d x %d\n\t\t", i, regions[i].size_x, regions[i].size_y);
        for (size_t j = 0; j < NR_SHAPES; ++j) {
            printf("%zu ", regions[i].count_each_shape[j]);
        }
        printf("\n");
    }

    int nr_fits = count_regions_that_fit(shapes, regions, nr_regions);

    printf("Number of regions that fit all their packages: %d\n", nr_fits);

    free(regions);
}

void second_part(char *input_file_name) {
    // TODO:
    return;
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
