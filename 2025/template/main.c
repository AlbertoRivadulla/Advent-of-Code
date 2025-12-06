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

    char line[MAX_LINE_LENGTH];
    while(fgets(line, sizeof(line), input_file) != NULL) {
        // // Remove trailing \n
        // int line_len = strlen(line);
        // if (line_len > 0 && line[line_len-1] == '\n') {
        //     line[line_len-1] = '\0';
        // }

        // TODO:
    }

    fclose(input_file);
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
