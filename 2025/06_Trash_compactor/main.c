#include <stdio.h>
#include <stdlib.h>

#include "timer.h"
#include "regex_utils.h"

const size_t MAX_LINE_LENGTH = 8192;

enum Operation {
    SUM,
    PRODUCT
};

typedef struct {
    unsigned long long *numbers;
    size_t nr_numbers;
    enum Operation operation;
    unsigned long long result;
} Problem;

void get_problems(char *input_file_name, Problem **problems, size_t *nr_problems, size_t *nr_numbers) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    *nr_numbers = 0;
    *nr_problems = 0;

    char line[MAX_LINE_LENGTH];
    while(fgets(line, sizeof(line), input_file) != NULL) {
        // Remove trailing \n
        size_t line_len = strlen(line);
        if (line_len > 0 && line[line_len-1] == '\n') {
            line[line_len-1] = '\0';
        }

        if (*nr_numbers == 0) {
            char *token = strtok(line, " ");
            while (token != NULL) {
                (*nr_problems)++;

                token = strtok(NULL, " ");
            }
        }

        (*nr_numbers)++;
    }

    *nr_numbers -= 1;

    *problems = malloc(*nr_problems * sizeof(Problem));
    for (size_t i = 0; i < *nr_problems; ++i) {
        (*problems)[i].numbers = malloc(*nr_numbers * sizeof(unsigned long long));
    }

    fseek(input_file, 0, SEEK_SET);

    size_t curr_line = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        // Remove trailing \n
        size_t line_len = strlen(line);
        if (line_len > 0 && line[line_len-1] == '\n') {
            line[line_len-1] = '\0';
        }

        char *token = strtok(line, " ");
        size_t curr_problem = 0;
        while (token != NULL) {
            if (curr_line < *nr_numbers) {
                (*problems)[curr_problem].numbers[curr_line] = atoll(token);
            }
            else {
                if (token[0] == '+') {
                    (*problems)[curr_problem].operation = SUM;
                }
                else {
                    (*problems)[curr_problem].operation = PRODUCT;
                }
            }
            token = strtok(NULL, " ");
            curr_problem++;
        }
        curr_line++;
    }

    fclose(input_file);
}

void evaluate_results(Problem *problems, size_t nr_problems, size_t nr_numbers) {
    for (size_t i = 0; i < nr_problems; ++i) {
        problems[i].result = problems[i].numbers[0];
        for (size_t j = 1; j < nr_numbers; ++j) {
            if (problems[i].operation == SUM) {
                problems[i].result += problems[i].numbers[j];
            }
            else if (problems[i].operation == PRODUCT) {
                problems[i].result *= problems[i].numbers[j];
            }
        }
    }
}

void first_part(char *input_file_name) {
    Problem *problems;
    size_t nr_problems;
    size_t nr_numbers;

    get_problems(input_file_name, &problems, &nr_problems, &nr_numbers);

    evaluate_results(problems, nr_problems, nr_numbers);

    // printf("Number of problems %d\n", nr_problems);
    // printf("Number of numbers %d\n", nr_numbers);
    // for (size_t i = 0; i < nr_problems; ++i) {
    //     printf("Problem %d\n", i);
    //     printf("\tNumbers ");
    //     for (size_t j = 0; j < nr_numbers; ++j) {
    //         printf("%d , ", problems[i].numbers[j]);
    //     }
    //     printf("\n\tOperation %d\n", problems[i].operation);
    //     printf("\tResult %d\n", problems[i].result);
    // }

    unsigned long long total_results = 0;

    for (size_t i = 0; i < nr_problems; ++i) {
        total_results += problems[i].result;
    }

    printf("Sum of results %llu\n", total_results);

    for (size_t i = 0; i < nr_problems; ++i) {
        free(problems[i].numbers);
    }
    free(problems);
}


void get_problems_second(char *input_file_name, Problem **problems, size_t *nr_problems) {
    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == 0) {
        printf("Could not open the file %s\n", input_file_name);
        exit(1);
    }

    *nr_problems = 0;

    char line[MAX_LINE_LENGTH];
    size_t nr_lines = 0;
    size_t line_len;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        // Remove trailing \n
        line_len = strlen(line);
        if (line_len > 0 && line[line_len-1] == '\n') {
            line[line_len-1] = '\0';
        }
        line_len--;

        if (nr_lines == 0) {
            char *token = strtok(line, " ");
            while (token != NULL) {
                (*nr_problems)++;

                token = strtok(NULL, " ");
            }
        }

        nr_lines++;
    }

    char *lines = malloc(nr_lines * line_len * sizeof(char));

    fseek(input_file, 0, SEEK_SET);
    size_t curr_line = 0;
    while(fgets(line, sizeof(line), input_file) != NULL) {
        for (size_t i = 0; i < line_len; ++i) {
            lines[i + curr_line*line_len] = line[i];
        }
        curr_line++;
    }

    *problems = malloc(*nr_problems * sizeof(Problem));
    // size_t problem_idx = 0;
    size_t first_nr_idx = 0;
    size_t last_nr_idx = 1;
    for (size_t problem_idx = 0; problem_idx < *nr_problems; ++problem_idx) {
        // Find the index of the last problem number
        while(last_nr_idx < line_len - 1 && lines[(nr_lines-1)*line_len + last_nr_idx] == ' ') {
            last_nr_idx++;
        }
        if (last_nr_idx != line_len - 1) {
            last_nr_idx -= 2;
        }

        (*problems)[problem_idx].nr_numbers = last_nr_idx - first_nr_idx + 1;
        (*problems)[problem_idx].numbers = malloc((last_nr_idx - first_nr_idx + 1) * sizeof(unsigned long long));

        for (size_t nr_idx = 0; nr_idx < last_nr_idx - first_nr_idx + 1; ++nr_idx) {
            unsigned long long this_nr = 0;
            for (size_t i = 0; i < nr_lines - 1; ++i) {
                char this_digit = lines[i * line_len + nr_idx + first_nr_idx];
                if (this_digit != ' ') {
                    this_nr *= 10;
                    this_nr += this_digit - '0';
                }
            }
            (*problems)[problem_idx].numbers[nr_idx] = this_nr;
        }

        if (lines[(nr_lines-1)*line_len + first_nr_idx] == '+') {
            (*problems)[problem_idx].operation = SUM;
        }
        else {
            (*problems)[problem_idx].operation = PRODUCT;
        }

        first_nr_idx = last_nr_idx + 2;
        last_nr_idx = first_nr_idx + 1;
    }

    fclose(input_file);
}

void evaluate_results_second(Problem *problems, size_t nr_problems) {
    for (size_t i = 0; i < nr_problems; ++i) {
        problems[i].result = problems[i].numbers[0];
        for (size_t j = 1; j < problems[i].nr_numbers; ++j) {
            if (problems[i].operation == SUM) {
                problems[i].result += problems[i].numbers[j];
            }
            else if (problems[i].operation == PRODUCT) {
                problems[i].result *= problems[i].numbers[j];
            }
        }
    }
}

void second_part(char *input_file_name) {
    Problem *problems;
    size_t nr_problems;

    get_problems_second(input_file_name, &problems, &nr_problems);

    evaluate_results_second(problems, nr_problems);

    // printf("Number of problems %d\n", nr_problems);
    // for (size_t i = 0; i < nr_problems; ++i) {
    //     printf("Problem %d\n", i);
    //     printf("\tNumbers ");
    //     for (size_t j = 0; j < problems[i].nr_numbers; ++j) {
    //         printf("%d , ", problems[i].numbers[j]);
    //     }
    //     printf("\n\tOperation %d\n", problems[i].operation);
    //     printf("\tResult %d\n", problems[i].result);
    // }

    unsigned long long total_results = 0;

    for (size_t i = 0; i < nr_problems; ++i) {
        total_results += problems[i].result;
    }

    printf("Sum of results %llu\n", total_results);

    for (size_t i = 0; i < nr_problems; ++i) {
        free(problems[i].numbers);
    }
    free(problems);
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
