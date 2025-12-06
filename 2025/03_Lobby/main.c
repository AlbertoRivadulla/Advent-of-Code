#include <stdio.h>
#include <stdlib.h>

#include <time.h>

#include "timer.h"
#include "regex_utils.h"

const size_t MAX_LINE_LENGTH = 1024;

void first_part(char *input_file_name) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    int sum_of_max = 0;

    char line[MAX_LINE_LENGTH];
    while(fgets(line, sizeof(line), input_file) != NULL) {
        // Remove trailing \n
        size_t line_len = strlen(line);
        if (line_len > 0 && line[line_len-1] == '\n') {
            line[line_len-1] = '\0';
        }
        line_len = strlen(line);

        int digits[MAX_LINE_LENGTH];
        for (size_t i = 0; i < line_len; ++i) {
            digits[i] = line[i] - '0';
        }

        int this_max = 0;
        for (size_t i = 0; i < line_len - 1; ++i) {
            for (size_t j = i + 1; j < line_len; ++j) {
                int this_nr = digits[i] * 10 + digits[j];
                if (this_nr > this_max) {
                    this_max = this_nr;
                }
            }
        }

        sum_of_max += this_max;
    }

    fclose(input_file);

    printf("Sum of maximum values %d\n", sum_of_max);
}

void second_part(char *input_file_name) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    unsigned long long sum_of_max = 0;

    char line[MAX_LINE_LENGTH];
    while(fgets(line, sizeof(line), input_file) != NULL) {
        // Remove trailing \n
        size_t line_len = strlen(line);
        if (line_len > 0 && line[line_len-1] == '\n') {
            line[line_len-1] = '\0';
        }
        line_len = strlen(line);

        int digits[MAX_LINE_LENGTH];
        for (size_t i = 0; i < line_len; ++i) {
            digits[i] = line[i] - '0';
        }

        unsigned long long this_max = 0;
        size_t idx = 0;
        size_t nr_remaining_digits = 12;
        for (size_t i = 0; i < 12; ++i) {
            // Move to the right until I find a larger digit, but stop if there are no enough digits
            int this_digit = digits[idx];

            for (size_t j = idx + 1; j <= line_len - nr_remaining_digits; ++j) {
                // printf(".j %d.", j);
                if (digits[j] > this_digit) {
                    this_digit = digits[j];
                    idx = j;
                }
                if (this_digit == 9) {
                    break;
                }
            }
            this_max = this_max * 10 + this_digit;
            idx++;
            nr_remaining_digits--;
        }

        sum_of_max += this_max;
    }

    fclose(input_file);

    printf("Sum of maximum values %llu\n", sum_of_max);
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
