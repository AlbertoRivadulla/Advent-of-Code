#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "timer.h"
#include "regex_utils.h"

const size_t MAX_LINE_LENGTH = 1024;

typedef struct {
    size_t idx_1;
    size_t idx_2;
    unsigned long long distance_sq;
} Distance;

void read_coords(char *input_file_name, int **coords, size_t *nr_coords) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    char line[MAX_LINE_LENGTH];
    *nr_coords = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        (*nr_coords)++;
    }

    *coords = malloc((*nr_coords) * 3 * sizeof(int));
    fseek(input_file, 0, SEEK_SET);

    size_t coord_idx = 0;
    size_t this_coord_idx = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        char *token = strtok(line, ",");
        while (token != NULL) {
            (*coords)[coord_idx * 3 + this_coord_idx++] = atoi(token);

            token = strtok(NULL, ",");
        }

        this_coord_idx = 0;
        coord_idx++;
    }

    fclose(input_file);
}

Distance get_distance_sq(int *coords, size_t idx_1, size_t idx_2) {
    Distance dist;
    dist.idx_1 = idx_1;
    dist.idx_2 = idx_2;
    dist.distance_sq = 0;
    for (size_t i = 0; i < 3; ++i) {
        unsigned long long delta = coords[idx_1 * 3 + i] - coords[idx_2 * 3 + i];
        dist.distance_sq += delta * delta;
    }
    return dist;
}

void swap(Distance *a, Distance *b) {
    Distance temp = *a;
    *a = *b;
    *b = temp;
}

size_t find_partition_idx(Distance *distances, size_t low, size_t high) {
    unsigned long long pivot_dist = distances[low].distance_sq;
    size_t i = low;
    size_t j = high;

    while (i < j) {
        // Find the first element greater than the pivot from the beginning
        while (distances[i].distance_sq <= pivot_dist && i <= high - 1) {
            ++i;
        }

        // Find the first element smaller than the pivot from the end
        while (distances[j].distance_sq > pivot_dist && j >= low + 1) {
            j--;
        }

        if (i < j) {
            swap(&distances[i], &distances[j]);
        }
    }
    swap(&distances[low], &distances[j]);

    return j;
}

void sort_distances(Distance *distances, size_t low, size_t high) {
    if (low < high) {
        // Find the partition index
        size_t partition_idx = find_partition_idx(distances, low, high);

        sort_distances(distances, low, partition_idx);
        sort_distances(distances, partition_idx + 1, high);
    }
}

unsigned long long connect_and_multiply(int *coords, size_t nr_coords, size_t nr_connections, size_t nr_to_multiply) {
    // Compute all distances
    size_t nr_distances = nr_coords * (nr_coords - 1)/2;
    Distance *distances = malloc(nr_distances * sizeof(Distance));
    size_t this_idx = 0;
    for (size_t i = 0; i < nr_coords; ++i) {
        for (size_t j = i + 1; j < nr_coords; ++j) {
            distances[this_idx++] = get_distance_sq(coords, i, j);
        }
    }

    sort_distances(distances, 0, nr_distances - 1);

    // Make connections and create circuits
    int *circuit_assoc = malloc(nr_coords * sizeof(size_t));
    for (size_t i = 0; i < nr_coords; ++i) {
        circuit_assoc[i] = -1;
    }
    int last_circuit_id = -1;

    for (size_t i = 0; i < nr_connections; ++i) {
        int new_circuit_id;
        if (circuit_assoc[distances[i].idx_1] != -1) {
            new_circuit_id = circuit_assoc[distances[i].idx_1];
        } else if (circuit_assoc[distances[i].idx_2] != -1) {
            new_circuit_id = circuit_assoc[distances[i].idx_2];
        } else {
            new_circuit_id = ++last_circuit_id;
        }

        if (circuit_assoc[distances[i].idx_2] != -1) {
            // Set also the new circuit id for those associated with the second element
            for (size_t j = 0; j < nr_coords; ++j) {
                if (j == distances[i].idx_2) {
                    continue;
                }
                if (circuit_assoc[j] == circuit_assoc[distances[i].idx_2]) {
                    circuit_assoc[j] = new_circuit_id;
                }
            }
        }

        circuit_assoc[distances[i].idx_1] = new_circuit_id;
        circuit_assoc[distances[i].idx_2] = new_circuit_id;
    }

    // Get the sizes of the different circuits
    int* circuit_count = malloc(last_circuit_id * sizeof(int));
    for (size_t i = 0; i < nr_coords; ++i) {
        if (circuit_assoc[i] >= 0) {
            circuit_count[circuit_assoc[i]]++;
        }
    }

    // Multiply the sizes of the nr_to_multiply largest circuits
    unsigned long long product = 1;
    int *mask = malloc(last_circuit_id * sizeof(int));
    for (size_t i = 0; i < last_circuit_id; ++i) {
        mask[i] = 0;
    }

    for (size_t nr_circ = 0; nr_circ < nr_to_multiply; ++nr_circ) {
        int this_max = 0;
        size_t i_max = 0;
        for (size_t i = 0; i < last_circuit_id; ++i) {
            if (mask[i] == 1) {
                continue;
            }
            if (circuit_count[i] >= this_max) {
                this_max = circuit_count[i];
                i_max = i;
            }
        }
        mask[i_max] = 1;
        product *= this_max;
    }

    free(mask);
    free(circuit_count);
    free(circuit_assoc);
    free(distances);

    return product;
}

void first_part(char *input_file_name) {
    int *coords;
    size_t nr_coords;

    read_coords(input_file_name, &coords, &nr_coords);

    size_t nr_connections = 1000;
    size_t nr_to_multiply = 3;
    if (nr_coords == 20) {
        nr_connections = 10;
    }
    unsigned long long product = connect_and_multiply(coords, nr_coords, nr_connections, nr_to_multiply);

    free(coords);

    printf("Product of %lu largest circuit sizes: %llu\n", nr_to_multiply, product);
}

unsigned long long connect_all(int *coords, size_t nr_coords, size_t nr_connections, size_t nr_to_multiply) {
    // Compute all distances
    size_t nr_distances = nr_coords * (nr_coords - 1)/2;
    Distance *distances = malloc(nr_distances * sizeof(Distance));
    size_t this_idx = 0;
    for (size_t i = 0; i < nr_coords; ++i) {
        for (size_t j = i + 1; j < nr_coords; ++j) {
            distances[this_idx++] = get_distance_sq(coords, i, j);
        }
    }

    sort_distances(distances, 0, nr_distances - 1);

    // Make connections and create circuits
    int *circuit_assoc = malloc(nr_coords * sizeof(size_t));
    for (size_t i = 0; i < nr_coords; ++i) {
        circuit_assoc[i] = -1;
    }
    int last_circuit_id = -1;

    Distance last_distance;

    bool only_one = true;
    while (true) {
        for (size_t i = 0; i < nr_distances; ++i) {
            int new_circuit_id;
            if (circuit_assoc[distances[i].idx_1] != -1) {
                new_circuit_id = circuit_assoc[distances[i].idx_1];
            } else if (circuit_assoc[distances[i].idx_2] != -1) {
                new_circuit_id = circuit_assoc[distances[i].idx_2];
            } else {
                new_circuit_id = ++last_circuit_id;
            }

            if (circuit_assoc[distances[i].idx_2] != -1) {
                // Set also the new circuit id for those associated with the second element
                for (size_t j = 0; j < nr_coords; ++j) {
                    if (j == distances[i].idx_2) {
                        continue;
                    }
                    if (circuit_assoc[j] == circuit_assoc[distances[i].idx_2]) {
                        circuit_assoc[j] = new_circuit_id;
                    }
                }
            }

            circuit_assoc[distances[i].idx_1] = new_circuit_id;
            circuit_assoc[distances[i].idx_2] = new_circuit_id;

            last_distance.idx_1 = distances[i].idx_1;
            last_distance.idx_2 = distances[i].idx_2;


            // Check if there is only a single connection
            only_one = true;
            for (size_t i = 1; i < nr_coords; ++i) {
                if (circuit_assoc[i] != circuit_assoc[0]) {
                    only_one = false;
                    break;
                }
            }
            if (only_one) {
                break;
            }
        }

        if (only_one) {
            break;
        }
    }

    unsigned long long product = (unsigned long long)coords[last_distance.idx_1 * 3] 
                                 * (unsigned long long)coords[last_distance.idx_2 * 3];

    free(circuit_assoc);
    free(distances);

    return product;
}

void second_part(char *input_file_name) {
    int *coords;
    size_t nr_coords;

    read_coords(input_file_name, &coords, &nr_coords);

    size_t nr_connections = 1000;
    size_t nr_to_multiply = 3;
    if (nr_coords == 20) {
        nr_connections = 10;
    }
    unsigned long long product = connect_all(coords, nr_coords, nr_connections, nr_to_multiply);

    free(coords);

    printf("Product of last connections: %llu\n", product);
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
