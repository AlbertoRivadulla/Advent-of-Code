#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "timer.h"
#include "regex_utils.h"

const size_t MAX_LINE_LENGTH = 1024;

typedef struct {
    int target;
    size_t nr_lights;
    int *button_masks;
    size_t nr_buttons;
    int *joltages;
} Diagram;

size_t read_diagrams(char *input_file_name, Diagram **diagrams) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    char line[MAX_LINE_LENGTH];
    size_t nr_diagrams = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        ++nr_diagrams;
    }
    fseek(input_file, 0, SEEK_SET);

    *diagrams = malloc(nr_diagrams * sizeof(Diagram));

    regex_t regex_target;
    const char *pattern_target = "\\[([^]]+)\\]";
    if (regcomp(&regex_target, pattern_target, REG_EXTENDED)) {
        fprintf(stderr, "Could not compile regex pattern %s\n", pattern_target);
        exit(1);
    }
    regex_t regex_button;
    const char *pattern_button = "\\(([^\\)]+)\\)";
    if (regcomp(&regex_button, pattern_button, REG_EXTENDED)) {
        fprintf(stderr, "Could not compile regex pattern %s\n", pattern_button);
        exit(1);
    }
    regex_t regex_joltage;
    const char *pattern_joltage = "\\{([^\\}]+)\\}";
    if (regcomp(&regex_joltage, pattern_joltage, REG_EXTENDED)) {
        fprintf(stderr, "Could not compile regex pattern %s\n", pattern_joltage);
        exit(1);
    }

    const size_t max_groups = 10;
    regmatch_t group_array[max_groups];

    size_t diagram_idx = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        // Read the target
        char target_str[64];
        size_t nr_lights = 0;
        if (regexec(&regex_target, line, max_groups, group_array, 0) == 0) {
            extract_group(line, group_array[1], target_str, sizeof(target_str));
            nr_lights = group_array[1].rm_eo - group_array[1].rm_so;

            int target_val = 0;
            for (int i = nr_lights - 1; i >= 0; --i) {
                target_val = target_val << 1;
                if (target_str[i] == '#') {
                    target_val += 1;
                }
            }
            (*diagrams)[diagram_idx].target = target_val;
        }

        // Read the button schematics
        char *cursor = line;
        size_t nr_buttons = 0;
        while (regexec(&regex_button, cursor, max_groups, group_array, 0) == 0) {
            ++nr_buttons;
            cursor += group_array[0].rm_eo;
        }
        (*diagrams)[diagram_idx].nr_lights = nr_lights;
        (*diagrams)[diagram_idx].nr_buttons = nr_buttons;
        (*diagrams)[diagram_idx].button_masks = malloc(nr_buttons * sizeof(int));
        (*diagrams)[diagram_idx].joltages = malloc(nr_lights * sizeof(int));

        char button_str[256];
        size_t button_idx = 0;
        cursor = line;
        while (regexec(&regex_button, cursor, max_groups, group_array, 0) == 0) {
            extract_group(cursor, group_array[1], button_str, sizeof(button_str));

            int button_mask = 0;
            char *token = strtok(button_str, ",");
            while (token != NULL) {
                button_mask ^= (1 << atoi(token));
                token = strtok(NULL, ",");
            }

            (*diagrams)[diagram_idx].button_masks[button_idx++] = button_mask;
            cursor += group_array[0].rm_eo;
        }

        // Read the joltage values
        char joltage_str[256];
        if (regexec(&regex_joltage, line, max_groups, group_array, 0) == 0) {
            extract_group(line, group_array[1], joltage_str, sizeof(joltage_str));

            char *token = strtok(joltage_str, ",");
            size_t joltage_idx = 0;
            while (token != NULL) {
                (*diagrams)[diagram_idx].joltages[joltage_idx++] = atoi(token);

                token = strtok(NULL, ",");
            }
        }

        ++diagram_idx;
    }

    fclose(input_file);

    return nr_diagrams;
}

int press_buttons(int state, int nr_presses, int curr_min, size_t curr_button_idx, Diagram diagram) {
    if (state == diagram.target) {
        return nr_presses;
    } else if (curr_button_idx >= diagram.nr_buttons) {
        // return diagram.nr_buttons;
        return -1;
    }

    int min_presses = curr_min;
    // Press the current button and recursively press the rest
    int new_min = press_buttons(state ^ diagram.button_masks[curr_button_idx], nr_presses + 1, curr_min, curr_button_idx + 1, diagram);
    if (new_min > 0 && new_min < min_presses) {
        min_presses = new_min;
    }

    // Don't press the current button and recursively press the rest
    new_min = press_buttons(state, nr_presses, curr_min, curr_button_idx + 1, diagram);
    if (new_min > 0 && new_min < min_presses) {
        min_presses = new_min;
    }

    return min_presses;
}

int compute_min_button_presses(Diagram diagram) {
    return press_buttons(0, 0, diagram.nr_buttons, 0, diagram);
}

void first_part(char *input_file_name) {
    Diagram *diagrams;
    size_t nr_diagrams = read_diagrams(input_file_name, &diagrams);

    int min_button_presses = 0;
    for (size_t i = 0; i < nr_diagrams; ++i) {
        int this_min_button_presses = compute_min_button_presses(diagrams[i]);
        min_button_presses += this_min_button_presses;
    }

    printf("Minimum number of button presses: %d\n", min_button_presses);

    for (size_t i = 0; i < nr_diagrams; ++i) {
        free(diagrams[i].button_masks);
        free(diagrams[i].joltages);
    }
    free(diagrams);
}

const size_t MAX_NR_JOLTAGES = 16;
const size_t MAX_JOLTAGE_VALUE = 1000;

int press_buttons_with_joltages(const int *curr_joltages, int nr_presses, int curr_min, size_t curr_button_idx, Diagram diagram, int max_joltage) {
    // WARNING: This works for the example, but is too inefficient for the actual input
    bool reached_target = true;
    bool over_the_max = false;
    for (size_t i = 0; i < diagram.nr_lights; ++i) {
        if (curr_joltages[i] > diagram.joltages[i]) {
            over_the_max = true;
            reached_target = false;
            break;
        } else if (curr_joltages[i] != diagram.joltages[i]) {
            reached_target = false;
        }
    }

    if (over_the_max) {
        return -2;
    } else if (reached_target) {
        return nr_presses;
    } else if (curr_button_idx >= diagram.nr_buttons) {
        return -1;
    }

    int min_presses = curr_min;

    int joltages_after_press[MAX_NR_JOLTAGES];
    for (size_t i = 0; i < diagram.nr_lights; ++i) {
        joltages_after_press[i] = curr_joltages[i];
    }

    for (size_t j = 0; j < max_joltage; ++j) {
        if (j > 0) {
            // printf("Current button %d\n", diagram.button_masks[curr_button_idx]);
            for (size_t i = 0; i < diagram.nr_lights; ++i) {
                int this_mask = 0b1 << i;
                // printf("\tThis mask %d\n", this_mask);
                if (diagram.button_masks[curr_button_idx] & this_mask) {
                    // printf("\t\tPressing button %zu\n", i);
                    joltages_after_press[i] += 1;
                }
            }
        }
        // Press the current button and recursively press the rest
        int new_min = press_buttons_with_joltages(joltages_after_press, nr_presses + j, curr_min, curr_button_idx + 1, diagram, max_joltage);
        if (new_min > 0 && new_min < min_presses) {
            min_presses = new_min;
        }

        if (new_min == -2) {
            break;
        }
    }
    return min_presses;
}

const size_t MAX_COMBINATIONS = 2 << 4; // A value that I found to work correctly for the input

size_t get_button_combinations(Diagram diagram, const int state, int this_button_combination, int target, size_t button_idx, 
                               int *button_combinations, size_t nr_button_combinations) {
    if (state == target && button_idx != 0) {
        button_combinations[nr_button_combinations] = this_button_combination;
        return nr_button_combinations + 1;
    } else if (button_idx >= diagram.nr_buttons) {
        return nr_button_combinations;
    }

    // Try not pressing the current button
    nr_button_combinations = get_button_combinations(diagram, state, this_button_combination, target, 
                                                     button_idx + 1, button_combinations, nr_button_combinations);

    // Try pressing the current button
    nr_button_combinations = get_button_combinations(diagram, state ^ diagram.button_masks[button_idx], 
                                                     this_button_combination | (0b1 << button_idx), target, 
                                                     button_idx + 1, button_combinations, nr_button_combinations);

    return nr_button_combinations;
}

int compute_min_button_presses_with_joltajes(Diagram diagram, int nr_presses, int min_presses, int *target_joltage) {
    // NOTE: Based on https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/

    // TODO: Apply cache for the target joltages

    // Base case: the target joltages are all zero
    bool target_is_zero = true;
    for (size_t i = 0; i < diagram.nr_lights; ++i) {
        if (target_joltage[i] != 0) {
            target_is_zero = false;
            break;
        }
    }
    if (target_is_zero) {
        return 0;
    }

    // Get the combination of on/off that would remain, with on = even joltage and off = odd joltage
    int target = 0;
    for (int i = diagram.nr_lights - 1; i >= 0; --i) {
        target = target << 1;
        if (target_joltage[i] % 2 != 0) {
            target += 1;
        }
    }

    // Get the combinations of button presses that produce this result
    int button_combinations[MAX_COMBINATIONS] = {0};
    size_t nr_button_combinations = get_button_combinations(diagram, 0, 0, target, 0, button_combinations, 0);
    if (nr_button_combinations > MAX_COMBINATIONS) {
        printf("The number of button combination exceeds the maximum\n");
        exit(1);
    }

    for (size_t i = 0; i < nr_button_combinations; ++i) {
        int curr_nr_presses = 0;
        int joltage_after_presses[MAX_NR_JOLTAGES] = {0};
        for (size_t j = 0; j < diagram.nr_buttons; ++j) {
            if (button_combinations[i] & (0b1 << j)) {
                ++curr_nr_presses;

                // Compute the joltage produced by these button presses
                for (size_t k = 0; k < diagram.nr_lights; ++k) {
                    if (diagram.button_masks[j] & (0b1 << k)) {
                        joltage_after_presses[k]++;
                    }
                }
            }
        }

        // Compute the new target joltage
        int new_target_joltage[MAX_NR_JOLTAGES];

        // Get the target joltage after the current presses
        bool valid_joltage = true;
        for (size_t j = 0; j < diagram.nr_lights; ++j) {
            if (joltage_after_presses[j] > target_joltage[j]) {
                valid_joltage = false;
                break;
            }
            new_target_joltage[j] = (target_joltage[j] - joltage_after_presses[j]) / 2;
        }
        if (!valid_joltage) {
            continue;
        }

        // Compute the minimum with the next presses
        int min_with_new_target = compute_min_button_presses_with_joltajes(diagram, nr_presses + curr_nr_presses,
                                                                           min_presses, new_target_joltage);

        // Compute the current minimum
        int this_min_presses = curr_nr_presses + 2 * min_with_new_target;

        if (this_min_presses < min_presses) {
            min_presses = this_min_presses;
        }
    }

    return min_presses;
}

void second_part(char *input_file_name) {
    Diagram *diagrams;
    size_t nr_diagrams = read_diagrams(input_file_name, &diagrams);

    // FIXME:
    // Diagram 53 is not working because it is not able to find combinations that produce the target
    // But using the same target in the first part does find a target

    int min_button_presses = 0;
    for (size_t i = 0; i < nr_diagrams; ++i) {
    // for (size_t i = 53; i < 54; ++i) {
        // int this_min_button_presses = compute_min_button_presses_with_joltajes(diagrams[i]);
        int this_min_button_presses = compute_min_button_presses_with_joltajes(diagrams[i], 0, 1000000, diagrams[i].joltages);
        min_button_presses += this_min_button_presses;
        // printf("\n\n==================================================\n\n");

        // printf("diagram %zu, min_button_presses %d\n", i, this_min_button_presses);
        printf("Line %zu/156: answer %d\n", i + 1, this_min_button_presses);
    }

    printf("Minimum number of button presses: %d\n", min_button_presses);

    for (size_t i = 0; i < nr_diagrams; ++i) {
        free(diagrams[i].button_masks);
        free(diagrams[i].joltages);
    }
    free(diagrams);
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
