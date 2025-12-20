#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "timer.h"
#include "regex_utils.h"

const size_t MAX_LINE_LENGTH = 1024;

typedef struct Device {
    char label[4];
    struct Device **connected;
    size_t nr_connected;

    int cache_first;
    int cache_second[6];
} Device;

size_t read_devices(char *input_file_name, struct Device **devices) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    // First pass: count devices
    size_t nr_devices = 0;

    char line[MAX_LINE_LENGTH];
    while(fgets(line, sizeof(line), input_file) != NULL) {
        ++nr_devices;
    }

    // Second pass: create devices
    fseek(input_file, 0, SEEK_SET);
    *devices = malloc(nr_devices * sizeof(struct Device));
    size_t device_idx = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        size_t line_length = 0;
        while (line[line_length] != '\n') {
            ++line_length;
        }

        for (size_t i = 0; i < 3; ++i) {
            (*devices)[device_idx].label[i] = line[i];
        }
        (*devices)[device_idx].label[3] = '\0';

        (*devices)[device_idx].nr_connected = (line_length - 4) / 4;
        (*devices)[device_idx].connected = malloc((*devices)[device_idx].nr_connected * sizeof(struct Device *));

        (*devices)[device_idx].cache_first = -1;
        for (size_t k = 0; k < 6; ++k) {
            (*devices)[device_idx].cache_second[k] = -1;
        }

        ++device_idx;
    }

    // Third pass: connect devices
    fseek(input_file, 0, SEEK_SET);
    device_idx = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        size_t line_length = 0;
        while (line[line_length] != '\n') {
            ++line_length;
        }

        // Save links to the different devices connected
        for (size_t i = 0; i < (*devices)[device_idx].nr_connected; ++i) {
            bool is_out = true;
            char out_str[4] = "out\n";
            for (size_t k = 0; k < 3; ++k) {
                if (line[k + i*4 + 5] != out_str[k]) {
                    is_out = false;
                    break;
                }
            }
            if (is_out) {
                (*devices)[device_idx].connected[i] = NULL;
            }
            for (size_t j = 0; j < nr_devices; ++j) {
                bool are_connected = true;
                for (size_t k = 0; k < 3; ++k) {
                    if (line[k + i*4 + 5] != (*devices)[j].label[k]) {
                        are_connected = false;
                        break;
                    }
                }
                if (are_connected) {
                    (*devices)[device_idx].connected[i] = &(*devices)[j];
                }
            }
        }

        ++device_idx;
    }

    fclose(input_file);

    return nr_devices;
}

int count_paths_rec(Device *devices, size_t nr_devices, size_t nr_steps, Device *start_device) {
    if (nr_steps == nr_devices) {
        return -1;
    } else if (start_device == NULL) {
        return 1;
    }

    // Try to read from cache
    if (start_device->cache_first != -1) {
        return start_device->cache_first;
    }

    int nr_paths = 0;
    for (size_t i = 0; i < start_device->nr_connected; ++i) {
        int this_nr_paths = count_paths_rec(devices, nr_devices, nr_steps + 1, start_device->connected[i]);
        if (this_nr_paths > 0) {
            nr_paths += this_nr_paths;
        }
    }

    // Save to cache
    start_device->cache_first = nr_paths;

    return nr_paths;
}

int count_paths_to_out(Device *devices, size_t nr_devices) {
    // Find the starting device
    char you_str[4] = "you\0";
    Device *start_device = NULL;
    for (size_t i = 0; i < nr_devices; ++i) {
        bool is_you = true;
        for (size_t k = 0; k < 3; ++k) {
            if (devices[i].label[k] != you_str[k]) {
                is_you = false;
                break;
            }
        }
        if (is_you) {
            start_device = &(devices[i]);
            break;
        }
    }

    int nr_paths = count_paths_rec(devices, nr_devices, 0, start_device);

    return nr_paths;
}

void first_part(char *input_file_name) {
    struct Device *devices;
    size_t nr_devices = read_devices(input_file_name, &devices);

    int nr_paths_out = count_paths_to_out(devices, nr_devices);

    printf("Number of paths to out: %d\n", nr_paths_out);

    for (size_t i = 0; i < nr_devices; ++i) {
        free(devices[i].connected);
    }
    free(devices);
}

long count_paths_from_to(Device *devices, size_t nr_devices, size_t nr_steps, Device *start_device, Device *end_device,
                         size_t cache_idx) {
    if (nr_steps == nr_devices) {
        return -1;
    } else if (start_device == end_device) {
        return 1;
    } else if (start_device == NULL) {
        return -1;
    }

    // Try to read from cache
    if (start_device->cache_second[cache_idx] != -1) {
        return start_device->cache_second[cache_idx];
    }

    long nr_paths = 0;
    for (size_t i = 0; i < start_device->nr_connected; ++i) {
        long this_nr_paths = count_paths_from_to(devices, nr_devices, nr_steps + 1, start_device->connected[i],
                                                 end_device, cache_idx);
        if (this_nr_paths > 0) {
            nr_paths += this_nr_paths;
        }
    }

    // Save to cache
    start_device->cache_second[cache_idx] = nr_paths;

    return nr_paths;
}


long count_paths_to_out_through_points(Device *devices, size_t nr_devices, char start[4], char through_first[4],
                                      char through_second[4]) {
    // Find the different devices to go through
    Device *start_device = NULL;
    Device *through_first_device = NULL;
    Device *through_second_device = NULL;
    for (size_t i = 0; i < nr_devices; ++i) {
        bool is_start = true;
        bool is_first = true;
        bool is_second = true;
        for (size_t k = 0; k < 3; ++k) {
            if (devices[i].label[k] != start[k]) {
                is_start = false;
            }
            if (devices[i].label[k] != through_first[k]) {
                is_first = false;
            }
            if (devices[i].label[k] != through_second[k]) {
                is_second = false;
            }
        }
        if (is_start) {
            start_device = &(devices[i]);
        } else if (is_first) {
            through_first_device = &(devices[i]);
        } else if (is_second) {
            through_second_device = &(devices[i]);
        }
    }

    // Number of paths with the sequence start -> through_first -> through_second -> out
    long nr_paths_first = count_paths_from_to(devices, nr_devices, 0, start_device, through_first_device, 0) *
                         count_paths_from_to(devices, nr_devices, 0, through_first_device, through_second_device, 1) *
                         count_paths_from_to(devices, nr_devices, 0, through_second_device, NULL, 2);

    // Number of paths with the sequence start -> through_second -> through_first -> out
    long nr_paths_second = count_paths_from_to(devices, nr_devices, 0, start_device, through_second_device, 3) *
                         count_paths_from_to(devices, nr_devices, 0, through_second_device, through_first_device, 4) *
                         count_paths_from_to(devices, nr_devices, 0, through_first_device, NULL, 5);

    return nr_paths_first + nr_paths_second;
}

void second_part(char *input_file_name) {
    struct Device *devices;
    size_t nr_devices = read_devices(input_file_name, &devices);

    long nr_paths_out = count_paths_to_out_through_points(devices, nr_devices, "svr", "fft", "dac");

    printf("Number of paths to out through fft and dac: %ld\n", nr_paths_out);

    for (size_t i = 0; i < nr_devices; ++i) {
        free(devices[i].connected);
    }
    free(devices);
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
