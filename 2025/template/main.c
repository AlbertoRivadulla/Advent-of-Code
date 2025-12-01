#include <stdio.h>
#include <stdlib.h>

#include "utils.h"

// int main(int argc, char* argv[]) {
int main() {
    printf("Hello from main\n");

    int* numbers = malloc(5 * sizeof(int));
    if (numbers == NULL) {
        fprintf(stderr, "Memory allocation failure\n");
        return 1;
    }

    for (int i = 0; i < 5; ++i) {
        numbers[i] = i * 5;
        do_something(i);
        do_something(numbers[i]);
    }

    free(numbers);
    return 0;
}
