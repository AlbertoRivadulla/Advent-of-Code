#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "timer.h"
#include "regex_utils.h"

const size_t MAX_LINE_LENGTH = 1024;

typedef struct {
    int x;
    int y;
} Tile;

void get_tiles(char *input_file_name, Tile **tiles, size_t *nr_tiles) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    *nr_tiles = 0;

    char line[MAX_LINE_LENGTH];
    while(fgets(line, sizeof(line), input_file) != NULL) {
        (*nr_tiles)++;
    }

    *tiles = malloc((*nr_tiles) * sizeof(Tile));
    fseek(input_file, 0, SEEK_SET);

    size_t curr_coord = 0;

    while(fgets(line, sizeof(line), input_file) != NULL) {
        // Remove trailing \n
        size_t line_len = strlen(line);
        if (line_len > 0 && line[line_len-1] == '\n') {
            line[line_len-1] = '\0';
        }

        char *token = strtok(line, ",");
        while (token != NULL) {
            if (curr_coord % 2 == 0) {
                (*tiles)[curr_coord++ / 2].x = atoll(token);
            } else {
                (*tiles)[curr_coord++ / 2].y = atoll(token);
            }
            token = strtok(NULL, " ");
        }
    }

    fclose(input_file);
}

unsigned long long get_max_area(Tile *tiles, size_t nr_tiles) {
    unsigned long long max_area = 0;

    for (size_t i = 0; i < nr_tiles - 1; ++i) {
        for (size_t j = i + 1; j < nr_tiles; ++j) {
            unsigned long long this_area = (unsigned long long)abs(tiles[i].x - tiles[j].x + 1) *
                                           (unsigned long long)abs(tiles[i].y - tiles[j].y + 1);
            if (this_area > max_area) {
                max_area = this_area;
            }
        }
    }

    return max_area;
}

void first_part(char *input_file_name) {
    Tile *tiles;
    size_t nr_tiles;

    get_tiles(input_file_name, &tiles, &nr_tiles);

    unsigned long long max_area = get_max_area(tiles, nr_tiles);

    printf("Maximum area between tiles: %llu\n", max_area);

    free(tiles);
}

size_t min(size_t x1, size_t x2) {
    if (x1 < x2) {
        return x1;
    }
    return x2;
}

size_t max(size_t x1, size_t x2) {
    if (x1 > x2) {
        return x1;
    }
    return x2;
}

unsigned long long get_max_area_with_green_tiles(Tile *red_tiles, size_t nr_red_tiles) {
    unsigned long long max_area = 0;

    // Check if the rectangle between the two tiles that I am considering intersects any of the edges
    for (size_t i = 0; i < nr_red_tiles - 1; ++i) {
        for (size_t j = i + 1; j < nr_red_tiles; ++j) {
            bool is_valid = true;
            int xmin = min(red_tiles[i].x, red_tiles[j].x);
            int ymin = min(red_tiles[i].y, red_tiles[j].y);
            int xmax = max(red_tiles[i].x, red_tiles[j].x);
            int ymax = max(red_tiles[i].y, red_tiles[j].y);

            // Iterate over the edges
            for (size_t segm_start = 0; segm_start < nr_red_tiles; ++segm_start) {
                // Check if the edge intersects the rectangle
                size_t segm_end = (segm_start+1) % nr_red_tiles;
                if (segm_start == i && segm_end == j) {
                    continue;
                } 

                int xmin_segment = min(red_tiles[segm_start].x, red_tiles[segm_end].x);
                int ymin_segment = min(red_tiles[segm_start].y, red_tiles[segm_end].y);
                int xmax_segment = max(red_tiles[segm_start].x, red_tiles[segm_end].x);
                int ymax_segment = max(red_tiles[segm_start].y, red_tiles[segm_end].y);

                if (!(xmax <= xmin_segment ||
                        xmax_segment <= xmin ||
                        ymax <= ymin_segment ||
                        ymax_segment <= ymin)) {
                    is_valid = false;
                    break;
                }

                // Another way to check for an intersection
                // if (red_tiles[segm_start].x == red_tiles[segm_end].x) {
                //     // Vertical segment
                //     int x_segment = red_tiles[segm_start].x;
                //     int ymin_segment = min(red_tiles[segm_start].y, red_tiles[segm_end].y);
                //     int ymax_segment = max(red_tiles[segm_start].y, red_tiles[segm_end].y);
                //     if (xmin < x_segment && x_segment < xmax &&
                //         max(ymin_segment, ymin) < min(ymax_segment, ymax)) {
                //         is_valid = false;
                //         break;
                //     }
                // } else if (red_tiles[segm_start].y == red_tiles[segm_end].y) {
                //     // Horizontal segment
                //     int y_segment = red_tiles[segm_start].y;
                //     int xmin_segment = min(red_tiles[segm_start].x, red_tiles[segm_end].x);
                //     int xmax_segment = max(red_tiles[segm_start].x, red_tiles[segm_end].x);
                //     if (ymin < y_segment && y_segment < ymax &&
                //         max(xmin_segment, xmin) < min(xmax_segment, xmax)) {
                //         is_valid = false;
                //         break;
                //     }
                // }
            }

            if (is_valid) {
                unsigned long long this_area = (unsigned long long)(abs(red_tiles[i].x - red_tiles[j].x) + 1) *
                                               (unsigned long long)(abs(red_tiles[i].y - red_tiles[j].y) + 1);
                if (this_area > max_area) {
                    max_area = this_area;
                }
            }
        }
    }

    return max_area;
}

void second_part(char *input_file_name) {
    Tile *red_tiles;
    size_t nr_tiles;

    get_tiles(input_file_name, &red_tiles, &nr_tiles);

    unsigned long long max_area = get_max_area_with_green_tiles(red_tiles, nr_tiles);

    printf("Maximum area between tiles: %llu\n", max_area);

    free(red_tiles);
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
