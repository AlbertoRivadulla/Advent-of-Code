#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <regex.h>

#include "timer.h"
#include "regex_utils.h"

const size_t MAX_LINE_LENGTH = 1024;

void first_part(char *input_file_name) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    regex_t regex_compiled;
    const char *pattern = "^([RL])([0-9]+)";
    if (regcomp(&regex_compiled, pattern, REG_EXTENDED)) {
        fprintf(stderr, "Could not compile regex\n");
        exit(1);
    }
    size_t max_groups = 5;
    regmatch_t group_array[max_groups];

    int curr_pos = 50;
    int nr_zeroes = 0;

    char line[MAX_LINE_LENGTH];
    char direction[2];
    int sign = +1;
    char n_clicks_str[10];
    int n_clicks;

    while(fgets(line, sizeof(line), input_file) != NULL) {
        // // Remove trailing \n
        // int line_len = strlen(line);
        // if (line_len > 0 && line[line_len-1] == '\n') {
        //     line[line_len-1] = '\0';
        // }

        // Read the rotation direction and amount
        if (regexec(&regex_compiled, line, max_groups, group_array, 0) == 0) {
            // for (unsigned int g = 0; g < max_groups; ++g) {
            //     if (group_array[g].rm_so == - 1) {
            //         // The group did not match
            //         break;
            //     }
            // }
            extract_group(line, group_array[1], direction, sizeof(direction));
            extract_group(line, group_array[2], n_clicks_str, sizeof(n_clicks_str));
            n_clicks = atoi(n_clicks_str);

            if (direction[0] == 'L') {
                sign = -1;
            } else if (direction[0] == 'R') {
                sign = +1;
            }

            curr_pos = ((curr_pos + sign * n_clicks) % 100 + 100)%100;
            if (curr_pos == 0) {
                nr_zeroes++;
            }
        }
    }

    regfree(&regex_compiled);
    fclose(input_file);

    printf("Number of zeroes in the sequence: %d\n", nr_zeroes);
}

void second_part(char *input_file_name) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    regex_t regex_compiled;
    const char *pattern = "^([RL])([0-9]+)";
    if (regcomp(&regex_compiled, pattern, REG_EXTENDED)) {
        fprintf(stderr, "Could not compile regex\n");
        exit(1);
    }
    size_t max_groups = 5;
    regmatch_t group_array[max_groups];

    int curr_pos = 50;
    int nr_zeroes = 0;

    char line[MAX_LINE_LENGTH];
    char direction[2];
    int sign = +1;
    char n_clicks_str[10];
    int n_clicks;

    while(fgets(line, sizeof(line), input_file) != NULL) {
        // Read the rotation direction and amount
        if (regexec(&regex_compiled, line, max_groups, group_array, 0) == 0) {
            extract_group(line, group_array[1], direction, sizeof(direction));
            extract_group(line, group_array[2], n_clicks_str, sizeof(n_clicks_str));
            n_clicks = atoi(n_clicks_str);

            if (direction[0] == 'L') {
                sign = -1;
            } else if (direction[0] == 'R') {
                sign = +1;
            }

            int next_pos = curr_pos + sign * n_clicks ;

            nr_zeroes += sign * (next_pos / 100);
            if (next_pos <= 0 && curr_pos != 0) {
                nr_zeroes++;
            }

            curr_pos = (next_pos % 100 + 100)%100;
        }
    }

    regfree(&regex_compiled);
    fclose(input_file);

    printf("Number of times the dial points to zero: %d\n", nr_zeroes);
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
